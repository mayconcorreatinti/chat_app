from fastapi import APIRouter,HTTPException
from http import HTTPStatus
from schemas.users_schemas import Credentials
from database import Mysqldb

app = APIRouter(tags=['users'],prefix='/users')
db = Mysqldb()

@app.post('/',status_code=HTTPStatus.CREATED)
def create_account(account:Credentials):
    list_users = db.select_user_from_table((account.username,account.email))
    for user in list_users:
        if account.username in user['name']:
            raise HTTPException(
                detail="This name already exists!",
                status_code=HTTPStatus.CONFLICT,
            )
        elif account.email in user['email']:
            raise HTTPException(
                detail="This email already exists!",
                status_code=HTTPStatus.CONFLICT,
            )
    db.insert_user_from_table(
        (
            account.username,
            account.email,
            account.password,
        )
    )
    return account
    
