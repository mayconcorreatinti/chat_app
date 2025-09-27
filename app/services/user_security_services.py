from pwdlib import PasswordHash


pwd_context = PasswordHash.recommended()

def password_hash(password):
    return pwd_context.hash(password)

def verify_password(password,hash_password) -> bool:
    return pwd_context.verify(password,hash_password)