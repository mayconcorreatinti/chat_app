from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm


app = APIRouter(tags=['auth'],prefix='/auth')

@app.post('/')
def auth_router(user:OAuth2PasswordRequestForm):
    ...