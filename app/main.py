from fastapi import FastAPI
from app.api.routers.users import app as users


app = FastAPI()

@app.get('/')
def hello_world():
    return {'message':'hello world'} 

app.include_router(users)