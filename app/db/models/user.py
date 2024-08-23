from pydantic import BaseModel, Field, validator
from typing import Optional, List
from bson import ObjectId
from datetime import datetime

class User(BaseModel):
    username: str
    email: str
    password: str
    weight: float  # in kilograms
    height: float  # in meters
    bmi: float = Field(default=0.0)
    age: int
    diseases: List[str]
    allergies: List[str]
    gender: int
    exercises: str
    goals: List[str]
    disabled: Optional[bool] = None
    preferred_foods: Optional[List[str]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator("updated_at", pre=True, always=True)
    def set_updated_at(cls, v):
        return v or datetime.utcnow()
    
    @validator("bmi", always=True)
    def calculate_bmi(cls, v, values):
        weight = values.get("weight")
        height_cm = values.get("height")
        if weight and height_cm:
            height_m = height_cm / 100  # Convert cm to meters
            return weight / (height_m ** 2)
        return 0.0
    
    def save(self, update: bool = False):
        if update:
            self.updated_at = datetime.utcnow()
        # Ensure BMI is calculated before saving
        self.bmi = self.calculate_bmi(self.bmi, self.dict())
        
    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}

            
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