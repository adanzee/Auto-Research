import secrets

from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta 
from app.core.config import settings
from jose import jwt, JWTError
from config import SECRET_KEY, ALGORITHM

def plain_password(password:str) -> str:
    return password

def hash_password(password:str) -> str:
    pwd_context = CryptContext(schemes=["bcrypt"], depreciated= "auto")
    return pwd_context.hash(password)

def verify_password (hashed_password:str, plain_password:str) -> bool:
    pwd_context = CryptContext(schemes=["bcrypt"], depreciated= "auto")
    return pwd_context.verify(plain_password, hashed_password)
    

def create_access_token(data:dict, expires_data: int = 15):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_data)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token:str):
