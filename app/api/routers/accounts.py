from fastapi import APIRouter,HTTPException,Request,Form
from app.services.template_services import templates
from app.database import db
from http import HTTPStatus
from app.services.user_security_services import verify_password,password_hash
from app.services.auth_services import get_token
from app.schemas.accounts_schemas import (
    Listusers,Credentials,PublicCredentials,AuthCredentials
)
from typing import Annotated
from fastapi.responses import HTMLResponse,RedirectResponse

app = APIRouter(tags=['accounts'],prefix='/accounts')

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

@app.post('/auth')
async def auth_router(data: Annotated[AuthCredentials,Form()],request:Request):
    user = await db.select_user_from_table(data.username)
    if not user:
        if "text/html" in request.headers.get("accept"):
            return templates.TemplateResponse('login.html',{
                    "request":request,
                    "exception":"Incorrect username or password!"
                }
            )
        raise HTTPException(
            detail="Incorrect username or password!", status_code=HTTPStatus.FORBIDDEN
        )
    if not verify_password(data.password,user['password']):
        if "text/html" in request.headers.get("accept"):
            return templates.TemplateResponse('login.html',{
                    "request":request,
                    "exception":"Incorrect username or password!"
                }
            )
        raise HTTPException(
            detail="Incorrect username or password!", status_code=HTTPStatus.FORBIDDEN
        )
    token = get_token(data={"username":user['username']})
    if "text/html" in request.headers.get("accept"):
        return RedirectResponse(url=f"/chat?token={token}")
    return {
        "access_token":token,
        "token_type":"bearer"
    }

@app.get('/auth')
def auth_router_page(request:Request):
    return templates.TemplateResponse("login.html",{"request":request})

@app.post('/register',status_code=HTTPStatus.CREATED,response_model=PublicCredentials)
async def create_account(request:Request,account: Annotated[Credentials,Form()]):
    user = await db.select_the_user_for_validation(account.username,account.email)
    if user:
        if account.username == user['username']:
            if "text/html" in request.headers.get("accept"):
                return templates.TemplateResponse("register.html",{
                            "request":request,
                            "exception":"This username already exists!"
                        }
                    )
            raise HTTPException(
                detail="This name already exists!",
                status_code=HTTPStatus.CONFLICT,
            )
        elif account.email == user['email']:
            if "text/html" in request.headers.get("accept"):
                return templates.TemplateResponse("register.html",{
                            "request":request,
                            "exception":"This email already exists!"
                        }
                    )
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
    if "text/html" in request.headers.get("accept"):
        return templates.TemplateResponse("register.html",{
                            "request":request,
                            "data": "user registered successfully"
                        }
                    )
    return {
        'id':user['id'],
        'username':user['username'],
        'email':user['email']
    }

@app.get('/register',response_class=HTMLResponse)
def register_router_page(request:Request):
    return templates.TemplateResponse("register.html",{"request":request})




