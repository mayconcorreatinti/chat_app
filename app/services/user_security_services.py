from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer


pwd_context = CryptContext(schemes=['bcrypt'],deprecated = 'auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def password_hash(password):
    return pwd_context.hash(password)

def verify_password(password,hash_password) -> bool:
    return pwd_context.verify(password,hash_password)