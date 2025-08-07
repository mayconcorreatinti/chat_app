from pydantic import BaseModel,EmailStr

class Credentials(BaseModel):
    username: str
    email: EmailStr
    password: str 

class PublicCredentials(BaseModel):
    id: int
    username: str
    email: EmailStr

class Listusers(BaseModel):
    users: list[PublicCredentials]