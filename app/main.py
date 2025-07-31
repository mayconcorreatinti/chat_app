from fastapi import FastAPI
from api.routers.websocket import app as websock
from api.routers.users import app as users

app = FastAPI()

app.include_router(websock)
app.include_router(users)