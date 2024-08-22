from fastapi import APIRouter, UploadFile, File, HTTPException, Request, Depends
from pymongo.collection import Collection
from app.core.config import connect_to_database
from app.models.food_model import generate_food_suggestion
from typing import List
from bson import ObjectId
import subprocess

# import slowapi modules
from app.api.middleware.rate_limiter import limiter

# get the database 
from app.db.mongodb import get_db # get the database dependency
from app.db.models.user import User # get the user model to use authentication with current active user
from app.db.models.temp import TempFood, TempFoodItem

# add for auth middleware
from app.core.security import get_current_active_user

# get database connection
db = connect_to_database()
db = db["food_recommendation_database"] # database name
food_collection: Collection = db["foods"] # chat table inside food_recommendation_database
user_collection: Collection = db["users"] # user table inside food_recommendation_database
temp_food_collection: Collection = db["temp_foods"] # temp food table inside of food_recommendation_database

# init the api router
router = APIRouter()

# get the food list by recommended by ai (refresh the foods)
@router.get("/get/recommended") # define route
@limiter.limit("5/minute") # rate limiting middleware
async def get_recommended(
    request: Request, # without this the limiter won't work
    current_user: User = Depends(get_current_active_user) # for active user like auth
    ):
    #change current user info to put into AI
    keys = ['weight', 'height', 'age', 'diseases', 'allergies', 'exercises']
    ai_input = {x: current_user[x] for x in keys}
    ai_input['gender'] = 'Female' if current_user['gender'] else 'Male'
    ai_input = str(ai_input)
    # get_recommend food from ai generate
    recommend_food_sets = generate_food_suggestion(ai_input) 
    # if foods set is not none
    if not recommend_food_sets:
        raise HTTPException(status_code=404, detail="Unable to fetch foods, check your internet connection")
    # insert into temp food table
    # existing_foods = temp_food_collection.find({"user_id": str(current_user["_id"])})
    # # before we need to check that the foods already exist by user id
    # if existing_foods:
    #     # if foods exist, delete them
    #     if remove_temp_foods(str(current_user["_id"])):
    #         # will insert 3 meal set so that need to iterate it
    #         temp_food_collection.insert_many(list(recommend_food_sets))
    #     else:
    #         # if not then raise unable to delete foods
    #         raise HTTPException(status_code=500, detail="Unable to delete foods")
    # else:
    #     # else we only insert
    #     # will insert 3 meal set so that need to iterate it
    #     temp_food_collection.insert_many(list(recommend_food_sets))
    # finally return the getting recommended food set
    # data: recommend_food_sets is a list type
    return {"response": "success", "data": recommend_food_sets}



# confirmed the food list if user like the meal set
# temp_food ------> food table
@router.post("/confirm") # define route
@limiter.limit("5/minute") # rate limiting middleware
async def confirm_food_lists(
    request: Request, # without this the limiter won't work
    current_user: User = Depends(get_current_active_user), # for active user
    ):
    # get temp food history from temp food table
    # find by user_id ---> will get 3 sets of meal
    temp_foods = temp_food_collection.find({
        "user_id": str(current_user["_id"]),
    })
    temp_foods_list = list(temp_foods)
    if not temp_foods_list:
        raise HTTPException(status_code=404, detail="No temporary foods found")
    else:
        # remove the _id field from each
        for food in temp_foods_list:
            if "_id" in food:
                del food["_id"]
        # iterate the temp foods and insert into food table
        food_collection.insert_many(temp_foods_list)
        # and delete the temp foods from temp food table
        temp_food_collection.delete_many({"user_id": str(current_user["_id"])})
    return {"response": "success", "message": "Foods confirmed and moved to food collection"}
    


# get selected food detail before confirming the foods
@router.get("/get/{food_id}")
@limiter.limit("5/minute")
async def get_food_details(
    request: Request, # without this limiter not work
    food_id: str, # select the food by food_id
    current_user: User = Depends(get_current_active_user) # for active user
    ):
    # get the selected temp_food_id with user_id
    selected_food = temp_food_collection.find_one({
        "user_id": str(current_user["_id"]),
        "_id": ObjectId(food_id) # need to change ObjectId as mongodb use id as object
    })
    # if selected food is exist then return it
    if selected_food:
        return {"response": "success", "data": selected_food}
    else:
        raise HTTPException(status_code=404, detail="Not Found")


# function to get the 3 set of meals 
# this function must return the json format
# make sure for json return format
def get_recommended_foods() -> list[TempFoodItem]:
    # this will generate by ai in here
    
    # get the response by ai
    
    # return the data
    return []



# function to delete the temporary foods
def remove_temp_foods(
    user_id: str # remove by user id
):
    # this is remove func of temp food if user confirm the foods set
    # from get_recommended_foods fun ----> to insert into food table
    # return true or false for check
    if temp_food_collection.delete_many({"user_id": user_id}):
        return True
    else:
        False
    