from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from database import Mysqldb
from http import HTTPStatus
from services.user_security_services import verify_password
from services.auth_services import get_token


app = APIRouter(tags=['auth'],prefix='/auth')
db = Mysqldb()

@app.post('/')
def auth_router(data:OAuth2PasswordRequestForm = Depends()):
    response = db.select_user_from_table((data.username,''))

    for user in response:
        if user == '':
            raise HTTPException(
                detail="Incorrect username or password!", status_code=HTTPStatus.FORBIDDEN
            )
        if not verify_password(data.password,user['password']):
            raise HTTPException(
                detail="Incorrect username or password!", status_code=HTTPStatus.FORBIDDEN
            )

        token = get_token(data={"email":user['email']})

        return {
            "access_token":token,
            "token_type":"bearer"
        }


