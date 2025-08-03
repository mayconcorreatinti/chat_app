from fastapi import APIRouter
from http import HTTPStatus
from schemas.users_schemas import Credentials


app = APIRouter(tags=['users'],prefix='/users')

@app.post('/',status_code=HTTPStatus.CREATED)
def create_account(account:Credentials):
    return {'user':account}

