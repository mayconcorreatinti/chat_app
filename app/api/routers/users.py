from fastapi import APIRouter,HTTPException
from http import HTTPStatus
from app.schemas.users_schemas import Credentials,PublicCredentials,Listusers
from app.database import Mysqldb
from app.services.user_security_services import password_hash


app = APIRouter(tags=['users'],prefix='/users')
db = Mysqldb()

@app.post('/',status_code=HTTPStatus.CREATED,response_model=PublicCredentials)
async def create_account(account:Credentials):
    user = await db.select_user_from_table(account.username)
    if user:
        if account.username in user['username']:
            raise HTTPException(
                detail="This name already exists!",
                status_code=HTTPStatus.CONFLICT,
            )
        elif account.email in user['email']:
            raise HTTPException(
                detail="This email already exists!",
                status_code=HTTPStatus.CONFLICT,
            )
    await db.insert_user_from_table(
        (
            account.username,
            account.email,
            password_hash(account.password),
        )
    )
    user = await db.select_user_from_table(account.username)
    return {
        'id':user['id'],
        'username':user['username'],
        'email':user['email']
    }

@app.get('/',response_model=Listusers)
async def get_users():
    list_users = await db.select_users_from_table()
    return {'users':list_users}
    
