from typing import List

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates

from dependencies import check_user
from connectionmanager import manager

chatting_router = APIRouter(dependencies=[Depends(check_user)])
templates = Jinja2Templates(directory='templates')


@chatting_router.get("/ws")
async def get(request: Request):
    return templates.TemplateResponse("chatting.html", {"request": request})


@chatting_router.websocket('/chatting/{client_id}')
async def websocket_chatting(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        websocket.session['client_id'] = client_id
        await manager.send_connections(websocket)
        await manager.broadcast(
            {'type': 'alert', 'detail': 'enter', 'client_id': client_id, 'message': "enter the chatting room"})
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
