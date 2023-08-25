import asyncio
import json

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Request, Query
from fastapi.templating import Jinja2Templates

import schemas
from dependencies import check_user_by_query
from connectionmanager import broadcast, chatting_room

chatting_router = APIRouter()
templates = Jinja2Templates(directory='templates')

CHANNEL = "CHAT"

async def receive_message(websocket: WebSocket, username=None):
    async with broadcast.subscribe(CHANNEL) as subscriber:
        async for event in subscriber:
            message_event = schemas.MessageEvent.parse_raw(event.message)
            if message_event.message_type == "whisper" and str(message_event.receiver) != str(username):
                continue
            await websocket.send_json(message_event.dict())


async def send_message(websocket: WebSocket):
    data = await websocket.receive_text()
    await broadcast.publish(channel=CHANNEL, message=data)
    await websocket.send_json(json.loads(data))

async def create_alert(websocket: WebSocket, message: str):
    websocket_message = schemas.MessageEvent(message=message, message_type="alert")
    await broadcast.publish(channel=CHANNEL, message=websocket_message.json())
    await websocket.send_json(websocket_message.dict())

async def get_chatting_room_users(websocket: WebSocket):
    user_list = await chatting_room.get_chatting_room_users()
    message = schemas.MessageEvent(message_type="list", message=[i.decode() for i in user_list])
    await broadcast.publish(channel=CHANNEL, message=message.model_dump_json())
    await websocket.send_json(message.model_dump())


async def add_chatting_room_users(websocket: WebSocket, username: str):
    await chatting_room.add_chatting_room(username)
    await create_alert(websocket, message=f"{username} 님이 채팅방에 입장하셨습니다.")


async def remove_chatting_room_users(websocket: WebSocket, username: str):
    await chatting_room.remove_chatting_room(username)
    await create_alert(websocket, message=f"{username} 님이 채팅방에서 나가셨습니다.")


@chatting_router.websocket("/ws-endpoint")
async def websocket_endpoint(websocket: WebSocket, user_id: int = Query(...,alias="user-id"), token=Depends(check_user_by_query)):
    await websocket.accept()
    # username = token.get("user_email")
    username = user_id
    await add_chatting_room_users(websocket, username)
    await get_chatting_room_users(websocket)
    try:
        while True:
            receive_message_task = asyncio.create_task(receive_message(websocket,username=username))
            send_message_task = asyncio.create_task(send_message(websocket))
            done, pending = await asyncio.wait(
                [receive_message_task, send_message_task],
                return_when=asyncio.FIRST_COMPLETED,
            )
            for task in pending:
                task.cancel()
            for task in done:
                task.result()
    except WebSocketDisconnect:
        await remove_chatting_room_users(websocket, username)
        await websocket.close()


@chatting_router.get("/ws")
async def get_chatting_page(request: Request):
    return templates.TemplateResponse("chatting.html", {"request": request})
