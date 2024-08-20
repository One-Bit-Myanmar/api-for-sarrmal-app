from fastapi import APIRouter, HTTPException, Request, Depends, UploadFile, File
from pymongo.collection import Collection
from app.core.config import connect_to_database
from app.db.models.temp import TempFood
from app.db.models.user import User
from app.db.models.food import Food
from app.core.security import get_current_active_user
from bson.objectid import ObjectId
from app.api.middleware.rate_limiter import limiter
from io import BytesIO
from PIL import Image

# imoprt the trained model by api
from app.models.food_model import get_calories_from_img 

# Initialize the API router
router = APIRouter()

# Get database connection
db = connect_to_database()
db = db["food_recommendation_database"]
temp_collection: Collection = db["temp_foods"]
food_collection: Collection = db["foods"]


# select from temp food which is from ai
@router.post("/select/recommendation/{temp_food_id}")
async def select_food_recommendation(
    request: Request,
    temp_food_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Select a recommended food set, store it in the main collection, and delete the temp data."""
    try:
        temp_food = temp_collection.find_one({"_id": ObjectId(temp_food_id), "user_id": current_user.id})
        
        if not temp_food:
            raise HTTPException(status_code=404, detail="Temp food not found")

        new_food = {
            "user_id": current_user.id,
            "name": temp_food["name"],
            "category": temp_food["category"],
            "ingredients": temp_food["ingredients"],
            "calories": temp_food["calories"],
            "food_allergies": temp_food["food_allergies"],
            "url_to_how_to_cook": temp_food["url_to_how_to_cook"],
            "image": temp_food["image"],
            "best_time_to_eat": temp_food["best_time_to_eat"],
            "created_at": temp_food["created_at"],
            "updated_at": temp_food["updated_at"],
            "selected": True
        }
        food_collection.insert_one(new_food)

        temp_collection.delete_one({"_id": ObjectId(temp_food_id)})
        temp_collection.delete_many({"user_id": current_user.id})

        return {"message": "Selected food recommendation has been stored and temp data cleared."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# remove the foods if foods are confirmed
@router.delete("/clear/temp_data")
async def clear_temp_data(
    request: Request,
    current_user: User = Depends(get_current_active_user)
):
    """Clear all temporary food recommendations for the current user."""
    try:
        result = temp_collection.delete_many({"user_id": current_user.id})

        if result.deleted_count == 0:
            return {"message": "No temporary food data to clear."}

        return {"message": f"Cleared {result.deleted_count} temporary food items."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.post("/transfer/{temp_food_id}", response_model=Food)
@limiter.limit("5/minute")
async def transfer_temp_to_food(
    request: Request,
    temp_food_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Endpoint to transfer food from TempFood to Food and delete TempFood"""
    try:
        temp_food = temp_collection.find_one({"_id": ObjectId(temp_food_id)})
        if not temp_food:
            raise HTTPException(status_code=404, detail="TempFood not found")
        
        food_data = Food(
            name=temp_food["name"],
            category=temp_food["category"],
            ingredients=temp_food["ingredients"],
            calories=temp_food["calories"],
            food_allergies=temp_food["food_allergies"],
            url_to_how_to_cook=temp_food["url_to_how_to_cook"],
            image=temp_food["image"],
            best_time_to_eat=temp_food["best_time_to_eat"]
        )
        
        food_collection.insert_one(food_data.dict())
        temp_collection.delete_one({"_id": ObjectId(temp_food_id)})
        
        return food_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




# get the food calories from user input
@router.post("/get/calories", response_model=dict)
@limiter.limit("5/minute")
async def get_food_calories_from_image(
    request: Request, # without limiter not work
    file: UploadFile = File(...), # for upload file
    current_user: User = Depends(get_current_active_user) # for user auth
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
    
    
# tick the eaten food if user take the food
@router.put("/tick/{food_id}")
@limiter.limit("5/minute")
async def tick_taken_food(
    request: Request, # without this limiter not work
    food_id: str, # tick the food by food id
    current_user: User = Depends(get_current_active_user) # for active user
    ):
    
    """func to make a food item as eaten"""
    pass
