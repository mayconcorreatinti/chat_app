from fastapi import WebSocket,APIRouter,WebSocketDisconnect,Request
from app.services.auth_services import get_current_user
from app.services.websocket_services import ConnectionManager
from fastapi.responses import HTMLResponse
from app.services.template_services import templates


app = APIRouter()
ws_manager = ConnectionManager()

@app.websocket('/ws')
async def websocket_endpoint(websocket:WebSocket,token:str):
    await ws_manager.connect(websocket)
    try:
        user = await get_current_user(token)
        await ws_manager.broadcast(f"{user['username']} entrou na sala!!")
        while True:
            data = await websocket.receive_text()
            await ws_manager.broadcast(f"{user['username']}: {data}")
    except WebSocketDisconnect:
        await ws_manager.disconnect(websocket)
        await ws_manager.broadcast(f"{user['username']} saiu da sala.")

@app.post('/chat',response_class=HTMLResponse)
def ws_page(request:Request,token:str):
    return templates.TemplateResponse('chat.html',{
            'request':request,
            'token':token
        }
    )
