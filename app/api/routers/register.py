from fastapi import APIRouter,HTTPException,Request
from http import HTTPStatus
from app.schemas.users_schemas import Credentials,PublicCredentials
from app.database import db
from app.services.user_security_services import password_hash
from app.services.template_services import templates


app = APIRouter(tags=['register'],prefix='/register')

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

@app.get('/')
def register_router_page(request:Request):
    return templates.TemplateResponse("register.html",{"request":request})