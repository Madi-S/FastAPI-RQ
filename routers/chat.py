import json
from typing import List
from datetime import datetime
from fastapi import APIRouter, Request, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from worker import redis


class ChatRoom:
    def __init__(self, id):
        self.id = id

    def save_message(self, text: str, author: str):
        message = ChatRoom.generate_message(text, author)
        json_message = json.dumps(message)
        redis.lpush(self.id, json_message)

    def get_messages(self, start: int = 0, end: int = -1):
        # return redis.lrange(self.id, start, end)
        return [
            {'text': 'Hello', 'author': 'Madi', 'datetime': datetime.now()},
            {'text': 'Hello', 'author': 'Madi', 'datetime': datetime.now()},
            {'text': 'Hello', 'author': 'Madi', 'datetime': datetime.now()},
            {'text': 'Hello', 'author': 'Madi', 'datetime': datetime.now()}
        ]

    @staticmethod
    def _generate_message(text: str, author: str) -> dict:
        return {
            'text': text,
            'user': author,
            'datetime': datetime.now()
        }


class ChatRoomsRegistry():
    def __init__(self):
        self.chat_rooms = {}

    def register(self, id):
        chat_room = ChatRoom(id)
        self.chat_rooms[id] = chat_room

    def get_all_endpoints(self):
        return list(self.chat_rooms.keys())

    def get_room_by_id(self, id):
        chat_room = self.chat_rooms.get(id)
        if chat_room:
            return chat_room
        raise KeyError(f'ChatRoom with id {id} is not registered')


chat_rooms_registry = ChatRoomsRegistry()
chat_rooms_registry.register('Room 666')
chat_rooms_registry.register('Room 228')
chat_rooms_registry.register('Room 322')

chat = APIRouter(prefix='/chat')
templates = Jinja2Templates(directory='templates')


@chat.get('/rooms', response_class=HTMLResponse)
async def rooms(request: Request):
    chat_rooms_endpoints = chat_rooms_registry.get_all_endpoints()

    return templates.TemplateResponse('rooms.html', {
        'request': request,
        'chat_rooms_endpoints': chat_rooms_endpoints
    })


@chat.get('/rooms/{room_id}', response_class=HTMLResponse)
async def room(room_id: str, request: Request):
    try:
        chat_room = chat_rooms_registry.get_room_by_id(room_id)
        messages = chat_room.get_messages()
    except KeyError:
        messages = []
        raise HTTPException(404, f'Room {room_id} not found')

    return templates.TemplateResponse('room.html', {
        'request': request,
        'room_id': room_id,
        'messages': messages
    })

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

    @ChatRoom.save_message
    async def broadcast_text(self, message: str, author: str):
        for connection in self.active_connections:
            await connection.send_text(f'{author}:{message}')

    @ChatRoom.save_message
    async def broadcast_json(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(json.dumps(message))


manager = ConnectionManager()


@chat.websocket('/ws/{room_id}/{client_id}')
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.broadcast_json({
        'author': 'System',
        'text': f'Client #{client_id} joined the chat'
    })
    await manager.connect(websocket)
    try:
        while True:
            print(dir(websocket))
            data_json = await websocket.receive_json()
            await manager.broadcast_json(data_json)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast_json({
            'author': 'System',
            'text': f'Client #{client_id} left the chat'
        })
