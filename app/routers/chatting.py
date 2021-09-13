import asyncio
import json
from typing import Optional

from pydantic import BaseModel
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates

from dependencies import check_user
from connectionmanager import manager
from redisconnection import redis_connection

chatting_router = APIRouter(dependencies=[Depends(check_user)])
templates = Jinja2Templates(directory='templates')


class WebSocketMessage(BaseModel):
    type: str
    detail: str
    message: str
    sender: str
    receiver: str


@chatting_router.get("/ws")
async def get(request: Request):
    return templates.TemplateResponse("chatting.html", {"request": request})


@chatting_router.websocket('/chatting/{client_id}/receive')
async def websocket_chatting_receive(websocket: WebSocket, client_id: str):
    before_len = 10000000
    websocket.session['client_id'] = client_id
    await manager.connect(websocket)
    try:
        await manager.send_connections(websocket)
        await redis_connection.lpush('chat', json.dumps(
            {'type': 'alert', 'detail': 'enter', 'sender': client_id, 'message': "enter the chatting room."}
        ))
        while True:
            if await redis_connection.sismember("users", client_id.encode()) is False:
                break
            msg_list = await redis_connection.lrange("chat", 0, -1)
            send_msg_list = msg_list[:len(msg_list) - before_len]
            if before_len != len(msg_list) and send_msg_list:
                for data in send_msg_list:
                    data = json.loads(data.decode())
                    if data.get('type') == 'whisper':
                        if data.get('receiver') == client_id:
                            await manager.send_personal_message({
                                'type': data.get('type'),
                                'sender': data.get('sender'),
                                'message': data.get('message'),
                                'receiver': data.get('receiver'),
                                'detail': data.get('detail')}, websocket)

                    elif data.get('type') == 'message' or data.get('type') == 'alert':
                        await manager.send_personal_message({
                            'type': data.get('type'),
                            'sender': data.get('sender'),
                            'message': data.get('message'),
                            'receiver': data.get('receiver'),
                            'detail': data.get('detail')}, websocket)
            await asyncio.sleep(0.01)
            before_len = len(msg_list)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        await redis_connection.lpush('chat', json.dumps({
            'type': 'alert',
            'detail': 'enter',
            'sender': client_id,
            'receiver': 'all',
            'message': "leave the chatting room."}))


@chatting_router.websocket('/chatting/{client_id}/send')
async def websocket_chatting_send(websocket: WebSocket, client_id: str):
    websocket.session['client_id'] = client_id
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if data.get('keepalive'):
                await manager.send_personal_message({'type': 'keepalive'}, websocket)
            if data.get('message') or data.get('whisper'):
                await redis_connection.lpush('chat', json.dumps({
                    "type": data.get('type'),
                    "sender": data.get('sender'),
                    "message": data.get('message'),
                    "receiver": data.get('receiver'),
                    "detail": data.get('detail')
                }))
            await asyncio.sleep(0.01)

    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        await redis_connection.lpush('chat', json.dumps(
            {'type': 'alert', 'detail': 'enter', 'sender': client_id, 'message': "leave the chatting room."}))
