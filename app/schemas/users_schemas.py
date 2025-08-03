from pydantic import BaseModel,EmailStr

class Credentials(BaseModel):
    username: str
    email: EmailStr
    password: str 