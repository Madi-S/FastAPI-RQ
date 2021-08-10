import json
from typing import List
from datetime import timedelta
from fastapi import WebSocket

from worker import redis, queue, sleep_task

OPTIMAL_TASK_DELAY_TIME_IN_SECONDS = 7


class ChatRoom:
    def __init__(self, id):
        self.id = id

    def save_message(self, message: dict):
        '''Message must be a dictionary with text and author fields'''
        json_message = json.dumps(message)
        redis.lpush(self.id, json_message)

    def get_messages(self, start: int = 0, end: int = -1):
        raw_messages = reversed(redis.lrange(self.id, start, end))
        messages = [json.loads(raw_msg) for raw_msg in raw_messages]
        return messages

    def generate_random_messages(self):
        self.save_message({'author': 'Jackson', 'text': 'Hello chat'})
        self.save_message({'author': 'Adema', 'text': 'Hello Jacksiboi'})
        self.save_message({'author': 'Alina', 'text': 'Hello Jackson'})

    def clear(self):
        redis.delete(self.id)


class ChatRoomsRegistry():
    def __init__(self):
        self.chat_rooms = {}

    def register(self, id):
        chat_room = ChatRoom(id)
        self.chat_rooms[id] = chat_room

    def register_sample_rooms(self):
        self.register('Memes room')
        self.register('Tennis club')
        self.register('Chelsea fans')

    def get_all_endpoints(self):
        return list(self.chat_rooms.keys())

    def get_room_by_id(self, id):
        chat_room = self.chat_rooms.get(id)
        if chat_room:
            return chat_room
        raise KeyError(f'ChatRoom with id {id} is not registered')


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_text(self, message: str, author: str):
        for connection in self.active_connections:
            await connection.send_text(f'{author}:{message}')

    async def broadcast_json(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(json.dumps(message))


def create_n_tasks(n: int = 10):
    for _ in range(n):
        queue.enqueue(sleep_task, 3)


def clear_queue():
    queue.empty()
    