import json
from datetime import datetime
from fastapi import APIRouter, Request, HTTPException, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from worker import redis

# TODO: Finish the HTML
# TODO: Test and enhance the HTML
# TODO: Store rooms and messages in redis (dictionaries or lists)
# TODO: Create default rooms (no possibility to create or delete a room)
# TODO: Implement socketio on client side
# TODO: Implement socketio on server side

CHAT_ROOMS = []


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
