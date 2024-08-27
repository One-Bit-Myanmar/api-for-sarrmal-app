from fastapi import APIRouter, HTTPException, Request, Depends
from pymongo.collection import Collection
from app.core.config import connect_to_database
from app.models.food_model import generate_food_suggestion
from typing import List
from datetime import datetime
from bson import ObjectId
# import subprocess
from app.services.food_image_searching_service import serach_for_food_image

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

# refresh the food
# get the food list by recommended by ai (refresh the foods)
@router.get("/get/recommended") # define route
@limiter.limit("50/minute") # rate limiting middleware
async def get_recommended(
    request: Request, # without this the limiter won't work
    current_user: User = Depends(get_current_active_user) # for active user like auth
    ):

    # generate the meal set
    is_generated = generate_and_insert_mealset(current_user)
    if is_generated:
        # get the inserted information
        inserted_foods = list(temp_food_collection.find({"user_id": str(current_user["_id"])}))
        # change objectId to string for id 
        for food in inserted_foods:
            food["_id"] = str(food["_id"])
        # finally return the getting recommended food set
        # data: recommend_food_sets is a list type
        return {"response": "success", "data": inserted_foods}
    else:
        return {"response": "failed", "message": "Failed to generate meal sets"}
    
# generate the foods but don't refresh it
@router.get("/get/temp_foods") # define route
@limiter.limit("50/minute") # rate limiting middleware
async def get_temp_foods(
    request: Request, # without this the limiter won't work
    current_user: User = Depends(get_current_active_user) # for active user like auth
    ):

    # if foods are already exist then don't insert new
    if temp_food_collection.count_documents({"user_id": str(current_user["_id"])}):
        # get the inserted information
        inserted_foods = list(temp_food_collection.find({"user_id": str(current_user["_id"])}))
        # change objectId to string for id
        for food in inserted_foods:
            food["_id"] = str(food["_id"])
            # finally return the getting recommended food set
        return {"response": "success", "data": inserted_foods}
    else:
    # generate the meal set
        is_generated = generate_and_insert_mealset(current_user)
        if is_generated:
            # get the inserted information
            inserted_foods = list(temp_food_collection.find({"user_id": str(current_user["_id"])}))
            # change objectId to string for id 
            for food in inserted_foods:
                food["_id"] = str(food["_id"])
            # finally return the getting recommended food set
            # data: recommend_food_sets is a list type
            return {"response": "success", "data": inserted_foods}
        else:
            return {"response": "failed", "message": "Failed to generate meal sets"}


# confirmed the food list if user like the meal set
# temp_food ------> food table
@router.post("/confirm") # define route
@limiter.limit("5/minute") # rate limiting middleware
async def confirm_food_lists(
    request: Request, # without this the limiter won't work
    current_user: User = Depends(get_current_active_user), # for active user
    ):
    # Get the start of today's date (00:00:00)
    start_of_today = datetime.combine(datetime.today(), datetime.min.time())
    # get temp food history from temp food table
    # find by user_id ---> will get 3 sets of meal
    temp_foods = temp_food_collection.find({
        "user_id": str(current_user["_id"]),
    })
    temp_foods_list = list(temp_foods)
    if not temp_foods_list:
        raise HTTPException(status_code=404, detail="No temporary foods found")
    else:
        # add created at and updated_at
        for food in temp_foods_list:
            food["created_at"] = datetime.utcnow()
            food["updated_at"] = datetime.utcnow()
            food["status"] = 0
        # remove the _id field from each
        for food in temp_foods_list:
            if "_id" in food:
                del food["_id"]
        # check today confirmed food list exist aspect to status = 0 and updated 
        food_list_of_today = food_collection.find({
            "user_id": str(current_user["_id"]),
            "status": 0,
            "updated_at": {"$gte": start_of_today}
        })
        # Convert the cursor to a list and count the items
        food_list_of_today = list(food_list_of_today)
        food_count_of_today = len(food_list_of_today)
        if food_list_of_today:
            # Use food_count_of_today to splice the temp_foods_list
            for i, food in enumerate(temp_foods_list[:food_count_of_today]):
                food_collection.update_one(
                    {
                        "user_id": str(current_user["_id"]),
                        "status": 0,
                        "updated_at": {"$gte": start_of_today}
                    },
                    {
                        "$set": {
                            "name": food["name"],
                            "calories": food["calories"],
                            "category": food["category"],
                            "meal_time": food["meal_time"],
                            "ingredients": food["ingredients"],
                            "how_to_cook": food["how_to_cook"],
                            "image_url": food["image_url"],
                            "updated_at": datetime.utcnow()
                        }
                    }
                )
        else:
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



# function that will separate the dict and add to list and then return
def convert_to_list(foods: dict, user_id: str):
    food_list = []
    # get the breakfast
    breakfast_main_dish = foods['response']['breakfast']['main_dish']
    breakfast_side_dish = foods['response']['breakfast']['side_dish']
    b_main_dish_image = serach_for_food_image(str(breakfast_main_dish))
    b_side_dish_image = serach_for_food_image(str(breakfast_side_dish))
    # get the lunch
    lunch_main_dish = foods['response']['lunch']['main_dish']
    lunch_side_dish = foods['response']['lunch']['side_dish']
    l_main_dish_image = serach_for_food_image(str(lunch_main_dish))
    l_side_dish_image = serach_for_food_image(str(lunch_side_dish))
    # get the dinner
    dinner_main_dish = foods['response']['dinner']['main_dish']
    dinner_side_dish = foods['response']['dinner']['side_dish']
    d_main_dish_image = serach_for_food_image(str(dinner_main_dish))
    d_side_dish_image = serach_for_food_image(str(dinner_side_dish))
    # for breakfast image url importing
    breakfast_main_dish["image_url"] = b_main_dish_image
    breakfast_side_dish["image_url"] = b_side_dish_image
    breakfast_main_dish["user_id"] = user_id
    breakfast_side_dish["user_id"] = user_id
    # append to the list
    food_list.append(breakfast_main_dish)
    food_list.append(breakfast_side_dish)
    # for lunch image url importing
    lunch_main_dish["image_url"] = l_main_dish_image
    lunch_side_dish["image_url"] = l_side_dish_image
    lunch_main_dish["user_id"] = user_id
    lunch_side_dish["user_id"] = user_id
    # append to the list
    food_list.append(lunch_main_dish)
    food_list.append(lunch_side_dish)
    # for dinner image url importing
    dinner_main_dish["image_url"] = d_main_dish_image
    dinner_side_dish["image_url"] = d_side_dish_image
    dinner_main_dish["user_id"] = user_id
    dinner_side_dish["user_id"] = user_id
    # append to the list
    food_list.append(dinner_main_dish)
    food_list.append(dinner_side_dish)
    # return the food lists
    return food_list
    
    
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
  
  
# get recommended foods by ai
def generate_and_insert_mealset(user: User):
    #change current user info to put into AI
    ai_input = f"""{{
    "weight": {user['weight']},
    "height": {user['height']},
    "age": {user['age']},
    "diseases": [{user['diseases']}],
    "allergies": [{user['allergies']}],
    "gender": "{"Female" if user['gender'] == 0 else "Male"}",
    "exercise": "{user['exercises']}"
    }}"""
    # get_recommend food from ai generate
    recommend_food_sets = generate_food_suggestion(ai_input) 
    # splice the dicts into pieces and append to list and return it 
    recommend_food_lists = convert_to_list(recommend_food_sets, str(user["_id"]))
    # if foods set is not none
    if not recommend_food_lists:
        raise HTTPException(status_code=404, detail="Unable to fetch foods, check your internet connection")
    # insert into temp food table
    existing_foods = temp_food_collection.find({"user_id": str(user["_id"])})
    # before we need to check that the foods already exist by user id
    if existing_foods:
        # if foods exist, delete them
        if remove_temp_foods(str(user["_id"])):
            # will insert 3 meal set so that need to iterate it
            for food in recommend_food_lists:
                # add created at and updated at fields
                food["created_at"] = datetime.utcnow()
                food["updated_at"] = datetime.utcnow()
                # insert into temp food table
                temp_food_collection.insert_one(food)
        # say that the operation success
            return True
        else:
            # if not then raise unable to delete foods
            raise HTTPException(status_code=500, detail="Unable to delete foods")
    else:
        # else we only insert
        # will insert 3 meal set so that need to iterate it
        for food in recommend_food_lists:
                # add created at and updated at fields
                food["created_at"] = datetime.utcnow()
                food["updated_at"] = datetime.utcnow()
                # insert into temp food table
                temp_food_collection.insert_one(food)
        return True
    return False
      