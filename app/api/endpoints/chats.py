from fastapi import APIRouter, HTTPException, Request, Depends
from pymongo.collection import Collection
from datetime import datetime, timedelta
from app.core.config import connect_to_database
from typing import List
from bson import ObjectId

# import slowapi modules
from app.api.middleware.rate_limiter import limiter

# get the database 
from app.db.mongodb import get_db # get the database dependency
from app.db.models.chat import Chat, RequestModel, ResponseModel # import the user model
from app.db.models.user import User
from app.core.security import get_current_active_user

# add chat model
from app.models.chat_model import generate_response

# database connection setup
db = connect_to_database()
db = db["food_recommendation_database"] # database name
chat_collection: Collection = db["chats"] # chat table inside food_recommendation_database
user_collection: Collection = db["users"] # user table inside food_recommendation_database


router = APIRouter()

# chat with ai
@router.post("/chat") # init router 
@limiter.limit("50/minute") # rate limiting middleware
async def chat_ai(
    request: Request, # without this the limiter won't work
    req_msg: RequestModel, # request message model this only have partial field 
    current_user: User = Depends(get_current_active_user) # check for user auth if user is active or not
    ):
    # check user is exist or not
    user = user_collection.find_one({"_id": current_user["_id"]})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # # get response from open ai layer
    # response = "temp response from AI"
    response = generate_response(req_msg.message)
    # # create chat dict to save in database
    chat_dict = {
        "user_id": str(current_user["_id"]),
        "date": datetime.now(),
        "message": req_msg.message,
        "response": response,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    # # save to database
    if chat_collection.insert_one(chat_dict):
        # # return 
        return {"response": "success", "data": response}
    else:
        raise HTTPException(status_code=401, detail="Failed to save database")

# get the specific chat
@router.get("/chat/{chat_id}") # init router
@limiter.limit("50/minute") # rate limiting middleware
async def get_chat(
    request: Request, # without this the limiter won't work
    chat_id: str, # get the chat id
    current_user: User = Depends(get_current_active_user) # check for user auth if user is
    ):
    # get chat by chat id
    chat = chat_collection.find_one({"_id": ObjectId(chat_id)})
    # change objectId to string
    chat["_id"] = str(chat["_id"])
    # if chat not exist, then raise exception
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"response": "success", "data": chat}

# edit and update the user request
@router.put("/chat/{chat_id}") # init router
@limiter.limit("50/minute") # rate limiting middleware
async def update_chat(
    request: Request, # without this the limiter won't work
    chat_id: str, # get chat id
    request_msg: RequestModel, # partial attr of chat model
    current_user: User = Depends(get_current_active_user) # check for user auth if active or not
    ):
    # find the chat by chat id
    chat = chat_collection.find_one({"_id": ObjectId(chat_id)})
    # if not found raise the error
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    # get response from open ai api
    # response = "updated response"
    response = generate_response(request_msg.message)
    # update to database
    chat_collection.update_one(
        {"_id": ObjectId(chat_id)}, 
        {
            "$set": 
            {
                "message": request_msg.message,
                "response": response,
                "date": datetime.now(),
            }
        }
    )
    # return
    return {"response": "success", "data": response}

# get the chat history by current user
@router.get('/chat') # init route
@limiter.limit("50/minute") # rate limiting middleware
async def get_chat_history(
    request: Request, # without this the limiter won't work
    current_user: User = Depends(get_current_active_user) # for user auth check active or not
    ):
    # get the start fo day and end of day
    start_of_today = datetime.combine(datetime.today(), datetime.min.time())
    start_of_tomorrow = start_of_today + timedelta(days=1)
    
    #delete the old chats
    chat_collection.delete_many({
        "user_id": str(current_user["_id"]),
        "date": {"$lt": start_of_today}
    })
    
    # get the chats for today ( get as list )
    chats = list(chat_collection.find({
        "user_id": str(current_user["_id"]),
        "date": {"$gte": start_of_today, "$lt": start_of_tomorrow}
    }))
    print(start_of_today, start_of_tomorrow)
    # if chat not found then raise an error
    if not chats:
        return {"response": "failed", "data": chats}
    for item in chats: # change the objectId to string so that we can get from json string
        item["_id"] = str(item["_id"])
    # return chats data
    return {"response": "success", "data": chats}