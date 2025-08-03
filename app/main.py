from fastapi import FastAPI
from api.routers.websocket import app as websock
from api.routers.users import app as users
from api.routers.auth import app as auth

app = FastAPI()

app.include_router(websock)
app.include_router(users)
app.include_router(auth)