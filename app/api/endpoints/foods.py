from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from pymongo.collection import Collection
from datetime import datetime
from app.core.config import connect_to_database
from io import BytesIO
from PIL import Image
import numpy as np
from typing import List

# import slowapi modules
from app.api.middleware.rate_limiter import limiter

# get the database 
from app.db.mongodb import get_db # get the database dependency
from app.db.models.Food import Food, FoodItem # import the user model


db = connect_to_database()
db = db["food_recommendation_database"] # database name
food_collection: Collection = db["foods"] # chat table inside food_recommendation_database
user_collection: Collection = db["users"] # user table inside food_recommendation_database

router = APIRouter()

# get 3 set of meals (breakfast, lunch, dinner) by user perferences 
@router.get("/get/recommendations/perferences", response_model=List[FoodItem])
@limiter.limit("5/minute")
async def get_recommended_foods(request: Request):
    """function to get recommended foods based on user perferences"""
    pass


# get 3 set of meals by user health
@router.get("/get/recommendations/health", response_model=List[FoodItem])
@limiter.limit("5/minute")
async def get_healthy_foods(request: Request):
    """func to get healthy foods based on user health"""
    pass


# get selected food detail
@router.get("/get/{food_id}", response_model=dict)
@limiter.limit("5/minute")
async def get_food_details(request: Request, food_id: str):
    """func to retrieve food details by id"""
    pass


# tick the eaten food
@router.put("/tick/{food_id}", response_model=dict)
@limiter.limit("5/minute")
async def tick_taken_food(request: Request, food_id: str):
    """func to make a food item as eaten"""
    pass


# get the food calores
@router.get("/get/calories", response_model=dict)
@limiter.limit("5/minute")
async def get_food_calories_from_image(request: Request, file: UploadFile = File(...)):
    """extract food calories from an uploaded image using a predict"""
    try:
        # Read the uploaded image file
        image = Image.open(BytesIO(await file.read()))
        
        # use model to predict the food ID from the image
        
        # return the food calories
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))