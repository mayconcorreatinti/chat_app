from fastapi import APIRouter,HTTPException,Request,Form
from http import HTTPStatus
from app.schemas.users_schemas import Credentials,PublicCredentials
from app.database import db
from app.services.user_security_services import password_hash
from app.services.template_services import templates
from typing import Annotated
from fastapi.responses import HTMLResponse


app = APIRouter(tags=['register'],prefix='/register')

@app.post('/',status_code=HTTPStatus.CREATED,response_model=PublicCredentials)
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

@app.get('/',response_class=HTMLResponse)
def register_router_page(request:Request):
    return templates.TemplateResponse("register.html",{"request":request})

