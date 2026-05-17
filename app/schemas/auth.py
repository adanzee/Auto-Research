from pydantic import BaseModel, EmailStr
from typing import Optional


class LoginRequest(BaseModel):
    email: EmailStr
    password:str

class SignupRequest(BaseModel):
    username:str
    email:EmailStr
    password:str

class TokenResponse(BaseModel):
    access_token:str
    token_type:str = "bearer" 

class TokenData(BaseModel):
   email= Optional[EmailStr] = None