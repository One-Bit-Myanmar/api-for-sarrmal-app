from fastapi import APIRouter, UploadFile, File, HTTPException, Request, Depends
from pymongo.collection import Collection
from app.core.config import connect_to_database
from io import BytesIO
from PIL import Image
from typing import List

# imoprt the trained model by api
from app.models.food_model import get_calories_from_img 

# import slowapi modules
from app.api.middleware.rate_limiter import limiter

# get the database 
from app.db.mongodb import get_db # get the database dependency
from app.db.models.temp import TempFood, TempFoodItem # import the user model
from app.db.models.user import User # get the user model to use authentication with current active user

# add for auth middleware
from app.core.security import get_current_active_user

# get database connection
db = connect_to_database()
db = db["food_recommendation_database"] # database name
food_collection: Collection = db["foods"] # chat table inside food_recommendation_database
user_collection: Collection = db["users"] # user table inside food_recommendation_database

# init the api router
router = APIRouter()

# get 3 set of meals (breakfast, lunch, dinner) by user perferences 
@router.get("/get/recommended/breakfast")
@limiter.limit("5/minute") # rate limiting middleware
async def get_preference_foods(
    request: Request, # without this limiter not work
    current_user: User = Depends(get_current_active_user) # for active user
    ):
    """function to get recommended foods based on user perferences"""
    pass

# get 3 set of meals (breakfast, lunch, dinner) by user perferences 
@router.get("/get/recommended/lunch")
@limiter.limit("5/minute") # rate limiting middleware
async def get_preference_foods(
    request: Request, # without this limiter not work
    current_user: User = Depends(get_current_active_user) # for active user
    ):
    """function to get recommended foods based on user perferences"""
    pass

# get 3 set of meals by user health
@router.get("/get/recommended/dinner")
@limiter.limit("5/minute")
async def get_healthy_foods(
    request: Request, # without this limiter not work
    current_user: User = Depends(get_current_active_user) # for active user
    ):
    
    """func to get healthy foods based on user health"""
    pass

# get selected food detail
@router.get("/get/{food_id}", response_model=dict)
@limiter.limit("5/minute")
async def get_food_details(
    request: Request, # without this limiter not work
    food_id: str, # select the food by food_id
    current_user: User = Depends(get_current_active_user) # for active user
    ):
    
    """func to retrieve food details by id"""
    pass

# tick the eaten food
@router.put("/tick/{food_id}", response_model=dict)
@limiter.limit("5/minute")
async def tick_taken_food(
    request: Request, # without this limiter not work
    food_id: str, # tick the food by food id
    current_user: User = Depends(get_current_active_user) # for active user
    ):
    
    """func to make a food item as eaten"""
    pass

# get the food calores
@router.post("/get/calories", response_model=dict)
@limiter.limit("5/minute")
async def get_food_calories_from_image(
    request: Request, # without limiter not work
    file: UploadFile = File(...), # for upload file
    # current_user: User = Depends(get_current_active_user) # for user auth
    ):
    try:
        # Read the uploaded image file
        image = Image.open(BytesIO(await file.read()))
        # use model to predict the food ID from the image
        response = get_calories_from_img(image)
        # Convert the string to a Python dictionary
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))