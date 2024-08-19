from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class Food_history(BaseModel):
    food_history_id: str
    food_id: str
    user_id: str
    calories: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator("updated_at", pre=True, always=True)
    def set_updated_at(cls, v):
        return v or datetime.utcnow()
    def save(self, update: bool = False):
        if update:
            self.updated_at = datetime.utcnow()


class FoodHistoryItem(BaseModel):
    datetime: datetime
    food_id: str
    calories: int

class UserFoodHistory(BaseModel):
    user_id: str
    food_history: list[FoodHistoryItem]