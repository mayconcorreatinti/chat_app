from fastapi import WebSocket,APIRouter,WebSocketDisconnect,WebSocketException
from app.services.auth_services import get_current_user
from app.services.websocket_services import ConnectionManager


app = APIRouter()
ws_manager = ConnectionManager()

@app.websocket('/ws')
async def push_endpoint(token:str,websocket:WebSocket):
    await ws_manager.connect(websocket)
    try:
        user = get_current_user(token)
        await ws_manager.broadcast(f"{user['username']} entrou na sala!!")
        while True:
            data = await websocket.receive_text()
            await ws_manager.broadcast(f"{user['username']}: {data}")
    except WebSocketDisconnect:
        await ws_manager.disconnect(websocket)
        await ws_manager.broadcast(f"{user['username']} saiu da sala.")