from fastapi import (
    WebSocket,APIRouter,WebSocketDisconnect,Depends
)
from services.auth_services import get_current_user
from services.websocket_services import ConnectionManager


app = APIRouter()
        
ws_manager = ConnectionManager()

@app.websocket('/ws')
async def push_endpoint(token:str,websocket:WebSocket):
    await ws_manager.connect(websocket)
    user = get_current_user(token)
    try:
        await ws_manager.broadcast(f"{user['name']} entrou na sala!!")
        while True:
            data = await websocket.receive_text()
            await ws_manager.broadcast(f"{user['name']}: {data}")
    except WebSocketDisconnect:
        await ws_manager.disconnect(websocket)
        await ws_manager.broadcast(f"{user['name']} saiu da sala.")