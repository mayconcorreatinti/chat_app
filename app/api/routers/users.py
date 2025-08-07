from fastapi import APIRouter,HTTPException
from http import HTTPStatus
from schemas.users_schemas import Credentials,PublicCredentials,Listusers
from database import Mysqldb
from services.user_security_services import password_hash


app = APIRouter(tags=['users'],prefix='/users')
db = Mysqldb()

@app.post('/',status_code=HTTPStatus.CREATED,response_model=PublicCredentials)
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
            password_hash(account.password),
        )
    )
    return account

@app.get('/',response_model=Listusers)
def get_users():
    list_users = db.select_users_from_table()
    return {'users':list_users}
    
