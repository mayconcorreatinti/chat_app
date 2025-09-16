from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.api.routers.websocket import app as websock
from app.api.routers.accounts import app as accounts
from app.front.accounts_page import app as accounts_page
from app.front.websocket_page import app as websock_page


app = FastAPI(docs_url=None,redoc_url=None)

@app.get('/')
def root_page():
    return RedirectResponse(url='/accounts/auth')

app.include_router(websock)
app.include_router(accounts)
app.include_router(websock_page)
app.include_router(accounts_page)