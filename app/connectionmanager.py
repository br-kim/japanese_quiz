import json
from typing import Dict

import aioredis
from broadcaster import Broadcast
from fastapi import WebSocket

import osenv
from database import redis_connection


broadcast = Broadcast("redis://localhost:6379")

class ChattingRoom:
    def __init__(self):
        self.redis_connection = redis_connection

    async def add_chatting_room(self, user_name):
        await self.redis_connection.sadd("chatting_room", user_name)

    async def remove_chatting_room(self, user_name):
        await self.redis_connection.srem("chatting_room", user_name)

    async def get_chatting_room_users(self):
        return await self.redis_connection.smembers("chatting_room")

chatting_room = ChattingRoom()

# class ConnectionManager:
#     def __init__(self, redis_url):
#         self.redis_connection = aioredis.from_url(redis_url)
#         pass
#
#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         client_id = websocket.session['client_id']
#         if not await self.redis_connection.sismember("users", client_id.encode()):
#             await self.redis_connection.sadd('users', client_id)
#
#     async def disconnect(self, websocket: WebSocket):
#         client_id = websocket.session['client_id']
#         await self.redis_connection.srem('users', client_id)
#
#     async def send_personal_message(self, message: dict, websocket: WebSocket):
#         await websocket.send_json(message)
#
#     async def send_connections(self, websocket: WebSocket):
#         user_list = await self.redis_connection.smembers('users')
#         await websocket.send_json({'type': 'list', 'message': [i.decode() for i in user_list]})
#
#     async def broadcast(self, message: Dict):
#         await self.redis_connection.lpush('chat', json.dumps(message))
#         return
#
#
# manager = ConnectionManager(osenv.REDIS_URL)
