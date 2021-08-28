from typing import List

from fastapi import WebSocket

from redisconnection import redis_connection


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        pass

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        if websocket not in self.active_connections:
            self.active_connections.append(websocket)
            await redis_connection.sadd('users', websocket.session['client_id'])

    async def disconnect(self, websocket: WebSocket):
        await redis_connection.srem('users', websocket.session['client_id'])
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

    async def send_whisper(self, message: dict):
        for connection in self.active_connections:
            if connection.session['client_id'] == message['client_id']:
                await connection.send_json(message)

    async def send_connections(self, websocket: WebSocket):
        user_list = await redis_connection.smembers('users')
        await websocket.send_json({'type': 'list', 'message': [i.decode() for i in user_list]})


manager = ConnectionManager()
