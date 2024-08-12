from pydantic import BaseModel, Field
from typing import List

class Answers(BaseModel):
    main_meal_time: List[str] = Field(..., example=["Breakfast", "Lunch", "Dinner"])
    good_breakfast: List[str] = Field(..., example=["Yes", "No", "Sometimes"])
    hunger_during_day: List[str] = Field(..., example=["Yes", "No", "Sometimes"])
    eat_meat: List[str] = Field(..., example=["Yes", "No", "Sometimes"])
    eat_vegetables: List[str] = Field(..., example=["Yes", "No", "Sometimes"])
    eat_fruit: List[str] = Field(..., example=["Yes", "No", "Sometimes"])
    eat_dairy: List[str] = Field(..., example=["Yes", "No", "Sometimes"])
    eat_sweets: List[str] = Field(..., example=["Yes", "No", "Sometimes"])
    main_meal_consist_of: List[str] = Field(..., example=["Protein", "Carbohydrates", "Vegetables", "..."])
    cholesterol_concerns: List[str] = Field(..., example=["High", "Medium", "Low", "None", "Unknown"])

class Frequencies(BaseModel):
    eating_times_per_day: int = Field(..., example=3)
    sweet_food_consumption: List[str] = Field(..., example=["Daily", "Weekly", "Monthly"])
    salty_food_consumption: List[str] = Field(..., example=["Daily", "Weekly", "Monthly"])
    fresh_fruit_consumption: List[str] = Field(..., example=["Daily", "Weekly", "Monthly"])
    fresh_vegetable_consumption: List[str] = Field(..., example=["Daily", "Weekly", "Monthly"])

class DietProportion(BaseModel):
    meat_products: List[str] = Field(..., example=["High", "Medium", "Low", "Very Low", "None"])
    vegetable_products: List[str] = Field(..., example=["High", "Medium", "Low", "Very Low", "None"])

class Survey(BaseModel):
    survey_id: int = Field(..., example=1)
    user_id: int = Field(..., example=1)
    answers: Answers
    frequencies: Frequencies
    diet_proportion: DietProportion
