from broadcaster import Broadcast

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
