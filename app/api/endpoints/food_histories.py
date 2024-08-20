from fastapi import APIRouter, Depends, HTTPException, Request
from pymongo.collection import Collection
from typing import List
from app.core.config import connect_to_database
from app.db.models.user import User

# for the user auth middleware
from app.core.security import get_current_active_user

# import slowapi modules
from app.api.middleware.rate_limiter import limiter

# init the api router
router = APIRouter()

# Dependency to get the food history collection
db = connect_to_database() # connect to the database
# get the food histoiies collection
food_history_collection: Collection = db["food_recommendation_database"]["food_histories"] 

# Get the food history by user ID
@router.get("/get") # route init
@limiter.limit("5/minute") # rate limiting middleware
async def get_food_history(
    request: Request, # without this the limiter won't work
    current_user: User = Depends(get_current_active_user) # for current user active user
    ):
    # get all the food histories by user id
    food_histories = food_history_collection.find(
        {"user_id": str(current_user["_id"])}
    )
    # convert the dicts to list
    food_history_list = list(food_histories)
    # change ObjectId to string id
    for food in food_history_list:
        food["_id"] = str(food["_id"])
    # return the food histories list
    return {"response": "success", "data": food_history_list}
