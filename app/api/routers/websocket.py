from fastapi import (
    WebSocket,APIRouter,WebSocketDisconnect,Depends
)
from asyncio import sleep
from services.auth_services import get_current_user
from services.websocket_services import ConnectionManager


app = APIRouter()
        
ws_manager = ConnectionManager()

app = APIRouter()

@app.websocket('/ws')
async def push_endpoint(websocket:WebSocket):
    await ws_manager.connect(websocket)
    token = await websocket.receive_text()
    user = get_current_user(token)
    await ws_manager.broadcast(f'{user['name']} entrou na sala!!')
    try:
        while True:
            data = await websocket.receive_text()
            await ws_manager.broadcast(f"{user['name']}: {data}")
    except WebSocketDisconnect:
        await ws_manager.disconnect(websocket)
        await ws_manager.broadcast(f"{user['name']} saiu da sala.")
