from fastapi import APIRouter, UploadFile, File, HTTPException, Request, Depends
from pymongo.collection import Collection
from app.core.config import connect_to_database
from app.db.models.temp import TempFood
from app.db.models.user import User
from app.db.models.food import Food
from app.core.security import get_current_active_user
from bson.objectid import ObjectId

# import slowapi modules
from app.api.middleware.rate_limiter import limiter

# get database connection
db = connect_to_database()
db = db["food_recommendation_database"]  # database name
temp_collection: Collection = db["temp_foods"]  # temp foods table
food_collection: Collection = db["foods"]  # foods table

# init the api router
router = APIRouter()

@router.post("/select/recommendation/{temp_food_id}")
async def select_food_recommendation(
    request: Request,
    temp_food_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Select a recommended food set, store it in the main collection, and delete the temp data."""
    try:
        # Find the selected temp food by ID
        temp_food = temp_collection.find_one({"_id": ObjectId(temp_food_id), "user_id": current_user.id})
        
        if not temp_food:
            raise HTTPException(status_code=404, detail="Temp food not found")

        # Store the selected food in the main food collection
        new_food = {
            "user_id": current_user.id,
            "meals": temp_food["meals"],  # assuming temp_food contains meals or relevant data
            "created_at": temp_food["created_at"],
            "calories": temp_food["calories"],  # Assuming you store calories
            "selected": True  # mark this as a selected recommendation
        }
        food_collection.insert_one(new_food)

        # Delete the selected temp food data from the temp collection
        temp_collection.delete_one({"_id": ObjectId(temp_food_id)})

        # Optionally, delete other temp data if the selected one is chosen
        temp_collection.delete_many({"user_id": current_user.id})

        return {"message": "Selected food recommendation has been stored and temp data cleared."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
    current_user: User = Depends(get_current_active_user),
    temp_collection: Collection = Depends(db), # TempFood collection
    food_collection: Collection = Depends(db)  # Food collection
):
    """Endpoint to transfer food from TempFood to Food and delete TempFood"""
    try:
        # Fetch the TempFood document by temp_food_id
        temp_food = await temp_collection["temp_foods"].find_one({"temp_food_id": temp_food_id})
        if not temp_food:
            raise HTTPException(status_code=404, detail="TempFood not found")
        
        # Create a Food model instance from the TempFood data
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
        
        # Insert the Food document into the Food collection
        await food_collection["foods"].insert_one(food_data.dict())
        
        # Delete the TempFood document from the TempFood collection
        await temp_collection["temp_foods"].delete_one({"temp_food_id": temp_food_id})
        
        return food_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
