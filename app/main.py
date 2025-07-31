from fastapi import FastAPI
from app.api.routers.websocket import app as websock


app = FastAPI()

app.include_router(websock)