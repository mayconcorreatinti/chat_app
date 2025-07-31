from fastapi import WebSocket,APIRouter

app = APIRouter()

@app.websocket('/ws')
async def websocket_endpoint(websocket:WebSocket):
    await websocket.accept()
    while True:
        mensagem = await websocket.receive_text()
        await websocket.send_text(f'Mensagem recebida: {mensagem}')

#www.aranacorp.com/pt/comunicacao-entre-servidor-e-cliente-websockets-com-python