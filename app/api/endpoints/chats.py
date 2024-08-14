from fastapi import APIRouter, Request, Depends, HTTPException, status
from pymongo.collection import Collection
from app.core.security import Hash, create_access_token, verify_token
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm
from app.core.config import connect_to_database

# get the database 
from app.db.mongodb import get_db
from app.db.models.Chat import Chat, RequestModel # import the user model

db = connect_to_database()
db = db["food_recommendation_database"] # database name
chat_collection = db["chats"] # chat table inside food_recommendation_database
user_collection = db["users"] # user table inside food_recommendation_database

router = APIRouter()

# chat with ai
@router.post("/chat")
def chat_ai(chat: Chat, user_id: int):
    # get current user id
    user_id = chat.user_id
    # check user is exist or not
    if user_collection.find_one({"user_id": user_id}):
        # sent to open ai layer
        
        # get response from open ai layer
        
        # save to database
        # chat_collection.insert_one(chat.dict())
        return {"message": "Chat created successfully"}
    else:
        return {"message": "User not found"}
    

# get the specific chat
@router.get("/chat/{chat_id}")
def get_chat(chat_id: str):
    chat = chat_collection.find_one({"chat_id": chat_id})
    return {"response": chat} if chat else {"message": "Chat not found"}

    
    
# edit and update the user request
@router.put("/chat/{chat_id}")
def update_chat(chat_id: str, request_msg: RequestModel):
    # find the chat
    if chat_collection.find_one({"chat_id": chat_id}):
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
    else:
        return {"message": "Chat not found"}
    return {"message": "Chat updated successfully", "response": "ai response this"}
    


# get the chat history by user id
@router.get('/chat/history/{user_id}')
def get_chat_history(user_id: int) -> list[Chat]:
    # get the start fo day
    start_of_today = datetime.combine(datetime.today(), datetime.min.time())
    # get the start of tomorrow(which is the end of today)
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
    return {"response": chats_list}