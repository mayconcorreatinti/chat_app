from fastapi import FastAPI
from app.api.routers.websocket import app as websock
from app.api.routers.users import app as users


app = FastAPI()

app.include_router(websock)
app.include_router(users)