from fastapi import APIRouter, HTTPException, Request, Depends, UploadFile, File
from fastapi.responses import JSONResponse
from pymongo.collection import Collection
from app.core.config import connect_to_database
from app.db.models.user import User
from app.db.models.food import Food
from app.core.security import get_current_active_user
from bson.objectid import ObjectId
from app.api.middleware.rate_limiter import limiter
from io import BytesIO
from PIL import Image
from datetime import datetime
from app.services.food_image_searching_service import serach_for_food_image

# imoprt the trained model by api
from app.models.food_model import get_calories_from_img 

# Initialize the API router
router = APIRouter()

# Get database connection
db = connect_to_database() # get connection
db = db["food_recommendation_database"] # get food_recommendation_database
temp_collection: Collection = db["temp_foods"] # temp food collection
food_collection: Collection = db["foods"] # food collection
food_histories_collection: Collection = db["food_histories"] # food histories collection


# init the list for storing the generated response temporarily
# after that the add_additional route will take the rest 
response_list = []

# get the food by the current active user
@router.get("/get/confirmed") # init the get route
@limiter.limit("50/minute") # rate limiting middleware
async def get_confirmed_food_list(
        request: Request, # without this the limiter won't work
        current_user: User = Depends(get_current_active_user) # get the current active user
    ):
    # Get the start of today's date (00:00:00)
    start_of_today = datetime.combine(datetime.today(), datetime.min.time())
    # get the food list by user id
    food_lists = food_collection.find({
        "user_id": str(current_user["_id"]),
        "created_at": {"$gte": start_of_today},
        "status": 0,
    })
    # change the food_lists into list
    food_lists = list(food_lists)
    # change ObjectId into String id so that we can return with json format
    for food in food_lists:
        food["_id"] = str(food["_id"])
    # return the filtered food_lists
    return {"response": "success", "data": food_lists}
    
# get the food by the food id
@router.get("/get/{food_id}") # init the get route
@limiter.limit("50/minute") # rate limiting middleware
async def get_confirmed_food_list(
        food_id: str,
        request: Request, # without this the limiter won't work
        current_user: User = Depends(get_current_active_user) # get the current active user
    ):
    # get the food list by user id
    get_food = food_collection.find_one({
        "user_id": str(current_user["_id"]),
        "food_id": str(food_id)
    })
    # change ObjectId into String id so that we can return with json format
    for food in get_food:
        food["_id"] = str(food["_id"])
    # return the filtered food_lists
    return {"response": "success", "data": get_food}



@router.post("/get/calories")
@limiter.limit("50/minute")
async def get_food_calories_from_image(
    request: Request,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    try:
        # Read the uploaded image file
        image = Image.open(BytesIO(await file.read()))
        # Use model to predict the food ID and calories from the image
        response = get_calories_from_img(image)

        # Check if the "message" attribute is not present or is None
        if response.get("message") is None:
            # Clean the temporary response list
            response_list.clear()
            # Add user id to response JSON list
            response["user_id"] = str(current_user["_id"])
            response["created_at"] = datetime.now() # add created at datetime
            response["updated_at"] = datetime.now() # add updated at datetime
            response["image_url"] = serach_for_food_image(response["name"])
            response["status"] = 0
            # Append the response to the temporary list for further use
            response_list.append(response)
        else:
            # If message is present, print it and return without saving
            print(f"Message present: {response['message']}")
        
        print(response_list)
        
        # Return the response
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    

# save the generated response to food collection with user id
@router.post("/add/generated_calories") # init the add generated_calories
@limiter.limit("50/minute") # rate limiting middleware
async def save_generated_response_from_image(
        request: Request, # without limiter not work
        current_user: User = Depends(get_current_active_user) # for user auth
    ):
    # check the list is empty or not
    if len(response_list) > 0:
        # add the food into food table from generated list
        if food_collection.insert_one(response_list[0]):
            # clear the list
            response_list.clear()
            # return response
            return {"message": "Food added successfully", "response": "success"}
        else:
            # return that failed to add food
            return {"message": "Failed to add food", "response": "success"}
    else:
        # return that there is no food in list
        return {"message": "No response to save", "response": "success"}
    

    
# tick the eaten food if user take the food
@router.put("/tick/{food_id}") # init the router
@limiter.limit("50/minute") # rate limiting middleware
async def tick_taken_food(
    request: Request, # without this limiter not work
    food_id: str, # tick the food by food id
    current_user: User = Depends(get_current_active_user) # for active user
    ):
    # check the food is exist or not
    food = food_collection.find({"_id": ObjectId(food_id)})
    # check food is exist or not
    if food:
        # update the food status to eaten
        result = food_collection.update_one(
            {"_id": ObjectId(food_id)}, 
            {"$set": 
                {
                    "status": 1 
                }
        })
        # if modified is correct then insert into food histories collection
        if result.modified_count > 0 :
            # insert into food history collection
            food_histories_collection.insert_one({
                "user_id": str(current_user["_id"]),
                "food_id": food_id,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            })
            # return the response
            return {"response": "success", "message": "Tick the food successfully"}
    else:
        # return the response
        return {"response": "failed", "message": "Food not found"}
