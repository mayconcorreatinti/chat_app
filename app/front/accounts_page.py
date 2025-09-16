from fastapi.responses import HTMLResponse
from app.services.template_services import templates
from fastapi import Request,APIRouter


app=APIRouter(prefix='/accounts')

@app.get('/register',response_class=HTMLResponse)
def register_router_page(request:Request):
    return templates.TemplateResponse("register.html",{"request":request})

@app.get('/auth')
def auth_router_page(request:Request):
    return templates.TemplateResponse("login.html",{"request":request})
