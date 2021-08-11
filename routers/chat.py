from fastapi import APIRouter, Request, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from main import logger
from utils import ChatRoomsRegistry, ConnectionManager


conn_manager = ConnectionManager()
chat_rooms_registry = ChatRoomsRegistry()
chat_rooms_registry.register_sample_rooms()

chat = APIRouter(prefix='/chat')
templates = Jinja2Templates(directory='templates')


@chat.get('/rooms', response_class=HTMLResponse, tags=['chat'])
@logger.catch
async def rooms(request: Request):
    chat_rooms_endpoints = chat_rooms_registry.get_all_endpoints()

    return templates.TemplateResponse('rooms.html', {
        'request': request,
        'chat_rooms_endpoints': chat_rooms_endpoints
    })


@chat.get('/rooms/{room_id}', response_class=HTMLResponse, tags=['chat'])
@logger.catch
async def room(room_id: str, request: Request):
    chat_room = get_chat_room_or_raise_404(room_id)
    messages = chat_room.get_messages()

    return templates.TemplateResponse('room.html', {
        'request': request,
        'room_id': room_id,
        'messages': messages
    })


@chat.websocket('/ws/{room_id}/{client_id}')
@logger.catch
async def websocket_endpoint(websocket: WebSocket, room_id: str, client_id: str):
    logger.debug('New websocket connection {} to a room {}', websocket.__repr__(), room_id)
    chat_room = get_chat_room_or_raise_404(room_id)

    await conn_manager.broadcast_json({
        'author': 'System',
        'text': f'Client #{client_id} joined the chat'
    })
    await conn_manager.connect(websocket)

    try:
        while True:
            data_json = await websocket.receive_json()
            chat_room.save_message(data_json)
            await conn_manager.broadcast_json(data_json)

    except WebSocketDisconnect:
        conn_manager.disconnect(websocket)
        await conn_manager.broadcast_json({
            'author': 'System',
            'text': f'Client #{client_id} left the chat'
        })


def get_chat_room_or_raise_404(room_id: str):
    try:
        return chat_rooms_registry.get_room_by_id(room_id)
    except KeyError:
        raise HTTPException(404, f'Room {room_id} not found')
