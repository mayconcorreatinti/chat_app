from pydantic import BaseModel,EmailStr

class Credentials(BaseModel):
    username: str
    email: EmailStr
    password: str 

class PublicCredentials(BaseModel):
    id: int
    email: EmailStr
    username: str

class Listusers(BaseModel):
    users: list[PublicCredentials]