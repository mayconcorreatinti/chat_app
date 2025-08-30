from fastapi import APIRouter,Request
from app.schemas.users_schemas import Listusers
from app.database import db
from app.services.user_security_services import password_hash
from app.services.template_services import templates


app = APIRouter(tags=['users'],prefix='/users')

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

