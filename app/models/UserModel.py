from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class User(BaseModel):
    username: str
    email: str
    password: str
    # created_at: datetime = 
    
class Login(BaseModel):
    username: str
    password: str
    
class Token(BaseModel):
    access_token: str
    Token_type: str
    
class TokenData(BaseModel):
    username: Optional[str] = None