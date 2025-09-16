from fastapi.responses import HTMLResponse
from fastapi import Request,APIRouter
from app.services.template_services import templates
import os 


app=APIRouter()

@app.post('/chat',response_class=HTMLResponse)
def ws_page(request:Request,token:str):
    return templates.TemplateResponse('chat.html',{
            'request':request,
            'token':token,
            'ip_maquina':os.getenv('IP_MAQUINA'),
        }
    )
