from datetime import datetime,UTC,timedelta
import os
from fastapi import Depends,HTTPException
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
import jwt
from http import HTTPStatus
from jwt.exceptions import InvalidTokenError
from database import Mysqldb


load_dotenv()

db=Mysqldb()

#encode token
def get_token(data:dict) -> str:
    exp=datetime.now(UTC) + timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
    payload = {'sub':data['email'],'exp':exp}
    token = jwt.encode(
        payload=payload,
        key=os.getenv('SECRET_KEY'),
        algorithm=os.getenv('ALGORITHM')
        )
    return token

#decode token
def get_current_user(token:str):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(
            token,
            os.getenv('SECRET_KEY'),
            algorithms=[os.getenv('ALGORITHM')]
        )
        email = payload.get('sub')
        if not email:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    
    list_user = db.select_user_from_table(('',email))
    for user in list_user:
        if user == '':
            raise credentials_exception
        return user