from datetime import datetime,UTC,timedelta
from fastapi import Depends,status,HTTPException
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from app.database import Mysqldb
from http import HTTPStatus
import jwt
import os


load_dotenv()

db=Mysqldb()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/accounts/auth")

#encode token'
def get_token(data:dict) -> str:
    exp=datetime.now(UTC) + timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
    payload = {'sub':data['username'],'exp':exp}
    token = jwt.encode(
        payload=payload,
        key=os.getenv('SECRET_KEY'),
        algorithm=os.getenv('ALGORITHM')
        )
    return token

#decode token
async def get_current_user(token = Depends(oauth2_scheme)):
    credentials_exception=HTTPException(
        detail="Unable to validate credentials!",
        status_code=HTTPStatus.UNAUTHORIZED
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
    user = await db.select_user_from_table(username)
    if not user:
        raise credentials_exception
    return user