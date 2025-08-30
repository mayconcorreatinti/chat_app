from fastapi import APIRouter,HTTPException,Request
from http import HTTPStatus
from app.schemas.users_schemas import Credentials,PublicCredentials,Listusers
from app.database import Mysqldb
from app.services.user_security_services import password_hash
from fastapi.templating import Jinja2Templates


app = APIRouter(tags=['users'],prefix='/users')
db = Mysqldb()
templates = Jinja2Templates(directory='app/templates')

@app.post('/',status_code=HTTPStatus.CREATED,response_model=PublicCredentials)
async def create_account(request:Request,account:Credentials):
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
async def get_users(request:Request):
    list_users = await db.select_users_from_table()
    if "application/json" in request.headers.get("accept"):
        return {'users':list_users}
    return templates.TemplateResponse(
        'users.html',{
                "request":request,
                "users":list_users
            }
        )
