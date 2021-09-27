import json
from typing import Dict

import aioredis
from fastapi import WebSocket

import osenv
from database import redis_connection


class ConnectionManager:
    def __init__(self, redis_url):
        self.redis_connection = aioredis.from_url(redis_url)
        pass

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        client_id = websocket.session['client_id']
        if not await self.redis_connection.sismember("users", client_id.encode()):
            await self.redis_connection.sadd('users', client_id)

    async def disconnect(self, websocket: WebSocket):
        client_id = websocket.session['client_id']
        await self.redis_connection.srem('users', client_id)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

    async def send_connections(self, websocket: WebSocket):
        user_list = await self.redis_connection.smembers('users')
        await websocket.send_json({'type': 'list', 'message': [i.decode() for i in user_list]})

    async def broadcast(self, message: Dict):
        await self.redis_connection.lpush('chat', json.dumps(message))
        return


manager = ConnectionManager(osenv.REDIS_URL)
