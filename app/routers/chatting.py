from typing import Optional, List

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from dependencies import get_db
from dependencies import check_user

chatting_router = APIRouter(dependencies=[Depends(check_user)])
templates = Jinja2Templates(directory='templates')


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

    async def send_whisper(self, message: dict):
        for connection in self.active_connections:
            if connection.session['client_id'] == message['client_id']:
                await connection.send_json(message)


manager = ConnectionManager()


@chatting_router.get("/ws")
async def get(request: Request):
    return templates.TemplateResponse("chatting.html", {"request": request})


@chatting_router.websocket('/chatting/{client_id}')
async def websocket_chatting(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        websocket.session['client_id'] = client_id
        await manager.broadcast({'type': 'alert', 'client_id': client_id, 'message': "enter the chatting room."})
        while True:
            data = await websocket.receive_json()
            if data['receiver']:
                await manager.send_whisper({'type': 'whisper','sender': client_id, 'client_id': data['receiver'], 'message': data['message']})
            else:
                await manager.broadcast({'type': 'message', 'client_id': client_id, 'message': data['message']})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast({'type': 'alert', 'client_id': client_id, 'message': "leave the chatting room."})
