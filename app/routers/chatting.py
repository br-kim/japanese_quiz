import json
from typing import Optional, List

import requests
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from dependencies import get_db
from dependencies import check_user

chatting_router = APIRouter(dependencies=[Depends(check_user)])
templates = Jinja2Templates(directory='templates')


class SingletonInstance:
    __instance = None

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **karg):
        cls.__instance = cls(*args, **karg)
        cls.instance = cls.__getInstance
        return cls.__instance


class ConnectionManager(SingletonInstance):
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

    async def send_whisper(self, message: dict):
        for connection in self.active_connections:
            if connection.session['client_id'] == message['client_id']:
                await connection.send_json(message)

    async def send_connections(self, websocket: WebSocket):
        connection_id_list = [i.session['client_id'] for i in self.active_connections]
        await websocket.send_json({'type': 'list', 'message': connection_id_list})


manager = ConnectionManager()


@chatting_router.get("/ws")
async def get(request: Request):
    return templates.TemplateResponse("chatting.html", {"request": request})


@chatting_router.websocket('/chatting/{client_id}')
async def websocket_chatting(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        res = requests.get("https://ipinfo.io?callback=callback")
        websocket.session['client_id'] = client_id
        await manager.send_connections(websocket)
        await manager.broadcast(
            {'type': 'alert', 'detail': 'enter', 'client_id': client_id, 'message': res.text})
        while True:
            data = await websocket.receive_json()
            if data.get('receiver'):
                await manager.send_whisper(
                    {'type': 'whisper', 'sender': client_id, 'client_id': data['receiver'], 'message': data['message']})
                await manager.send_personal_message(
                    {'type': 'message', 'sender': client_id, 'client_id': data['receiver'], 'message': data['message']},
                    websocket)
                continue
            if data.get('keepalive'):
                await manager.send_personal_message(
                    {'type': 'keepalive'},
                    websocket)
                continue
            await manager.broadcast({'type': 'message', 'client_id': client_id, 'message': data['message']})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(
            {'type': 'alert', 'detail': 'leave', 'client_id': client_id, 'message': "leave the chatting room."})
