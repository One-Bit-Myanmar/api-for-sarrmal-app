from fastapi import APIRouter, HTTPException, Request
from pymongo.collection import Collection
from datetime import datetime, timedelta
from app.core.config import connect_to_database
from typing import List

# import slowapi modules
from app.api.middleware.rate_limiter import limiter

# get the database 
from app.db.mongodb import get_db # get the database dependency
from app.db.models.Chat import Chat, RequestModel # import the user model


# database connection setup
db = connect_to_database()
db = db["food_recommendation_database"] # database name
chat_collection: Collection = db["chats"] # chat table inside food_recommendation_database
user_collection: Collection = db["users"] # user table inside food_recommendation_database

router = APIRouter()


# chat with ai
@router.post("/chat", response_model=dict)
@limiter.limit("5/minute")
async def chat_ai(request: Request, chat: Chat, user_id: int):
    # check user is exist or not
    user = user_collection.find_one({"user_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # sent to open ai layer
    # get response from open ai layer
    
    # save to database
    chat_data = chat.dict()
    chat_data["datetime"] = datetime.utcnow()
    chat_collection.insert_one(chat_data)
    
    return {"message": "Chat created successfully", "response": chat_data}
    

# get the specific chat
@router.get("/chat/{chat_id}", response_model=dict)
@limiter.limit("5/minute")
async def get_chat(request: Request, chat_id: str):
    chat = chat_collection.find_one({"chat_id": chat_id})
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"response": chat}

    
    
# edit and update the user request
@router.put("/chat/{chat_id}", response_model=dict)
@limiter.limit("5/minute")
async def update_chat(request: Request, chat_id: str, request_msg: RequestModel):
    # find the chat
    chat = chat_collection.find_one({"chat_id": chat_id})
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    # request to open ai api again
    # get response from open ai api
    
    # update to database
    chat_collection.update_one(
        {"chat_id": chat_id}, 
        {
            "$set": 
            {
                "message": request_msg.message,
                # "response": # from response from open ai api key
                "date": datetime.utcnow(),
            }
        }
    )
    return {"message": "Chat updated successfully", "response": "ai response this"}
    


# get the chat history by user id
@router.get('/chat/history/{user_id}', response_model=dict)
@limiter.limit("5/minute")
async def get_chat_history(request: Request, user_id: int) -> list[Chat]:
    # get the start fo day and end of day
    start_of_today = datetime.combine(datetime.today(), datetime.min.time())
    start_of_tomorrow = start_of_today + timedelta(days=1)
    
    # get the chats for today
    chats = chat_collection.find({
            "user_id": user_id,
            "datetime": {
                "$gte": start_of_today,
                "$lt": start_of_tomorrow
            }
        })
    # convert the cursor to a list 
    chats_list = list(chats)
    
    if not chats_list:
        raise HTTPException(status_code=404, detail="No chats Found")
    
    return {"response": chats_list}