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

class message(BaseModel):
    message: str

class token(BaseModel):
    access_token: str
    token_type: str