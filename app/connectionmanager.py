from typing import List

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        pass

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
