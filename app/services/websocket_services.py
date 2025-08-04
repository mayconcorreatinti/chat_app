from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.connections:list[WebSocket] = []

    async def connect(self,websocket):
        await websocket.accept()
        self.connections.append(websocket)

    async def disconnect(self,websocket):
        self.connections.remove(websocket)

    async def broadcast(self,message):
        for con in self.connections:
            await con.send_text(message)
        