from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class User(BaseModel):
    username: str
    email: str
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator("updated_at", pre=True, always=True)
    def set_updated_at(cls, v):
        return v or datetime.utcnow()

    def save(self, update: bool = False):
        if update:
            self.updated_at = datetime.utcnow()
        # Perform save operation to the database
        # For example: db.insert_one(self.dict(by_alias=True))
    
class Login(BaseModel):
    username: str
    password: str
    
class Token(BaseModel):
    access_token: str
    Token_type: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator("updated_at", pre=True, always=True)
    def set_updated_at(cls, v):
        return v or datetime.utcnow()

    def save(self, update: bool = False):
        if update:
            self.updated_at = datetime.utcnow()
        # Perform save operation to the database
        # For example: db.insert_one(self.dict(by_alias=True))
    
class TokenData(BaseModel):
    username: Optional[str] = None
    