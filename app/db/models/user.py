from pydantic import BaseModel, Field, validator
from typing import Optional
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
    exercise: str
    goals: list[str]
    preferred_foods: list[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator("updated_at", pre=True, always=True)
    def set_updated_at(cls, v):
        return v or datetime.utcnow()
    def save(self, update: bool = False):
        if update:
            self.updated_at = datetime.utcnow()