from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class Food(BaseModel):
    name: str
    category: str
    ingredients: list[str]
    calories: int
    food_allergies: list[str]
    url_to_how_to_cook: str
    image: str
    best_time_to_eat: list[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator("updated_at", pre=True, always=True)
    def set_updated_at(cls, v):
        return v or datetime.utcnow()
    def save(self, update: bool = False):
        if update:
            self.updated_at = datetime.utcnow()
    
class FoodItem(BaseModel):
    name: str
    category: str
    ingredients: list[str]
    calories: int
    food_allergies: list[str]
    url_to_how_to_cook: str
    image: str
    best_time_to_eat: list[str]
