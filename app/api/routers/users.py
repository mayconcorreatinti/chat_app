from fastapi import APIRouter,Depends

app =APIRouter(tags=['users'],prefix='/users')

@app.get('/')
def get_users():
    ...