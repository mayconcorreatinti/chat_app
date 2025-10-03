from fastapi import APIRouter,HTTPException,Depends
from http import HTTPStatus
from app.schemas import Credentials,PublicCredentials,Listusers,message,token
from app.database import db
from app.services.user_security_services import password_hash,verify_password
from app.services.auth_services import get_token
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth_services import get_current_user
from mysql.connector import IntegrityError


app = APIRouter(tags=['users'],prefix='/api/users')

@app.get('/',response_model=Listusers)
async def get_users():
    list_users = await db.select_users_from_table()
    return {'users':list_users}
    
@app.post('/',status_code=HTTPStatus.CREATED,response_model=PublicCredentials)
async def create_account(account:Credentials):
    user = await db.select_user_from_table(account.username,account.email)
    if user:
        if account.username == user['username']:
            raise HTTPException(
                detail='This name already exists!',
                status_code=HTTPStatus.CONFLICT,
            )
        elif account.email == user['email']:
            raise HTTPException(
                detail='This email already exists!',
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

@app.post('/auth',response_model=token)
async def auth_router(data:OAuth2PasswordRequestForm = Depends()):
    user = await db.select_user_from_table(data.username)
    if not user or not verify_password(data.password,user['password']):
        raise HTTPException(
            detail='Incorrect username or password!',
            status_code=HTTPStatus.UNAUTHORIZED
        )
    token = get_token(data={'username':user['username']})
    return {
        'access_token':token,
        'token_type':'Bearer'
    }

@app.delete('/{id}',response_model=message)
async def delete_account(id:int,current_user = Depends(get_current_user)):
    if id != current_user['id']:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='unauthorized request'
        )
    await db.delete_user_from_table((id,))
    return {'message':'user successfully removed'}

@app.put('/{id}',response_model=message)
async def update_account(id:int,account:Credentials,current_user = Depends(get_current_user)):
    if id != current_user['id']:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='unauthorized request'
        )
    try:
        await db.update_user_from_table(
            (
                account.username,
                account.email,
                password_hash(account.password),
                id
            )
        )
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or email already exists!'
        )
    return {'message':'credentials updated successfully'}