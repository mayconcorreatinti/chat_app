from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.database import Mysqldb
from http import HTTPStatus
from app.services.user_security_services import verify_password
from app.services.auth_services import get_token


app = APIRouter(tags=['auth'],prefix='/token')
db = Mysqldb()

@app.post('/')
def auth_router(data:OAuth2PasswordRequestForm = Depends()):
    user = db.select_user_from_table(data.username)
    if not user:
        raise HTTPException(
            detail="Incorrect username or password!", status_code=HTTPStatus.FORBIDDEN
        )
    if not verify_password(data.password,user['password']):
        raise HTTPException(
            detail="Incorrect username or password!", status_code=HTTPStatus.FORBIDDEN
        )
    token = get_token(data={"username":user['username']})
    return {
        "access_token":token,
        "token_type":"bearer"
    }


