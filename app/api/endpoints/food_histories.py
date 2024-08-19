from fastapi import APIRouter, Depends, HTTPException, Request
from pymongo.collection import Collection
from datetime import datetime, timedelta
from typing import List
from app.core.config import connect_to_database
from app.db.mongodb import get_db
from app.db.models.food_history import FoodHistoryItem, UserFoodHistory

# import slowapi modules
from app.api.middleware.rate_limiter import limiter

router = APIRouter()

# Dependency to get the food history collection
def get_food_history_collection(db=Depends(get_db)) -> Collection:
    return db["food_history"]

# Get the food history by user ID
@router.get("/get/{user_id}", response_model=List[FoodHistoryItem])
@limiter.limit("5/minute")
async def get_food_history(request: Request, user_id: str, food_history_collection: Collection = Depends(get_food_history_collection)):
    # food_history = list(food_history_collection.find({"user_id": user_id}))
    # if not food_history:
    #     raise HTTPException(status_code=404, detail="Food history not found for user")
    # return [FoodHistoryItem(**item) for item in food_history]
    pass
