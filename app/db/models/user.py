from pydantic import BaseModel, Field, validator
from typing import Optional, List
from bson import ObjectId
from datetime import datetime


class User(BaseModel):
    user_id: str
    username: str
    email: str
    password: str
    weight: float
    height: float
    bmi: float
    age: int
    diseases: list[str]
    allergies: list[str]
    gender: int
    exercises: str
    goals: list[str]
    disabled: Optional[bool] = None
    preferred_foods: Optional[List[str]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator("updated_at", pre=True, always=True)
    def set_updated_at(cls, v):
        return v or datetime.utcnow()
    
    def save(self, update: bool = False):
        if update:
            self.updated_at = datetime.utcnow()
            
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str  # To handle ObjectId serialization
        }
            
class UserUpdateModel(BaseModel):
    username: Optional[str]
    weight: float
    height: float
    age: int 
    diseases: list[str]    
    allergies: list[str]
    gender: int
    exercises: str
    goals: list[str]
    preferred_foods: Optional[List[str]] = Field(default_factory=list)

    

class HistoryItem(BaseModel):
    request: str
    response: str
    date_times: list[datetime]

class FoodRequest(BaseModel):
    id: str
    user_id: str
    history: list[HistoryItem]
    
class LoginRequest(BaseModel):
    email: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    email: str
    

class UserInDB(User):
    password: str