from datetime import datetime,UTC,timedelta
import os
from fastapi import Depends,HTTPException,WebSocketException,status
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
import jwt
from http import HTTPStatus
from jwt.exceptions import InvalidTokenError
from app.database import Mysqldb


load_dotenv()

db=Mysqldb()

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

'''encode token'''
def get_token(data:dict) -> str:
    exp=datetime.now(UTC) + timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
    payload = {'sub':data['username'],'exp':exp}
    token = jwt.encode(
        payload=payload,
        key=os.getenv('SECRET_KEY'),
        algorithm=os.getenv('ALGORITHM')
        )
    return token

'''decode token'''
def get_current_user(token:str):
    credentials_exception=WebSocketException(
        code=status.WS_1007_INVALID_FRAME_PAYLOAD_DATA
    )
    try:
        payload = jwt.decode(
            token,
            os.getenv('SECRET_KEY'),
            algorithms=[os.getenv('ALGORITHM')]
        )
        username = payload.get('sub')
        if not username:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = db.select_user_from_table(username)
    if not user:
        raise credentials_exception
    return user