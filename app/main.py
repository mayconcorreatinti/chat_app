from fastapi import FastAPI
from app.api.routers.websocket import app as websock
from app.api.routers.users import app as users
from app.api.routers.auth import app as auth
from app.api.routers.register import app as register


app = FastAPI()

app.include_router(websock)
app.include_router(users)
app.include_router(auth)
app.include_router(register)