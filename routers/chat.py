from fastapi import APIRouter, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

chat = APIRouter(prefix='/chat')
chat.mount('/static/', StaticFiles(directory='../static'), name='static')
templates = Jinja2Templates(directory='../templates')

@chat.get('/rooms', response_class=HTMLResponse)
async def rooms(request: Request):
    chat_rooms = []
    return templates.TemplateResponse('rooms.html', {'request': request, 'chat_rooms': chat_rooms})

@chat.get('/rooms/{room_id}', response_class=HTMLResponse)
async def rooms(room_id: str, request: Request):
    return templates.TemplateResponse('room.html', {'request': request, 'room_id': room_id})
