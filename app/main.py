from fastapi import FastAPI
from app.api.routers.websocket import app as websock
from app.api.routers.accounts import app as accounts


app = FastAPI()

app.include_router(websock)
app.include_router(accounts)