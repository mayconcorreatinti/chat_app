from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.api.routers.websocket import app as websock
from app.api.routers.accounts import app as accounts


app = FastAPI()
@app.get('/')
def root_page():
    return RedirectResponse(url='/accounts/auth')

app.include_router(websock)
app.include_router(accounts)