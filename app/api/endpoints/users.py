from fastapi import APIRouter, Request, Depends, HTTPException, status
from pymongo.collection import Collection
from app.core.security import Hash, create_access_token, verify_token
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
from app.core.config import connect_to_database
from app.db.models.User import User, UserUpdateModel

# Dependency injection for database connection
def get_user_collection():
    db = connect_to_database()
    return db["food_recommendation_database"]["users"]

def get_session_collection():
    db = connect_to_database()
    return db["food_recommendation_database"]["sessions"]

router = APIRouter()

# Get users list
@router.get('/gets')
async def get_users(user_collection: Collection = Depends(get_user_collection)):
    users = list(user_collection.find({}))
    for item in users:
        item["_id"] = str(item["_id"])
    return {"response": users}

# Get specific user by ID
@router.get('/get/{user_id}')
async def get_user(user_id: str, user_collection: Collection = Depends(get_user_collection)):
    user = user_collection.find_one({"user_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["_id"] = str(user["_id"])
    return {"response": user}

# Register a new user
@router.post('/register')
async def register_user(user: User, user_collection: Collection = Depends(get_user_collection), session_collection: Collection = Depends(get_session_collection)):
    existing_user = user_collection.find_one({
        "$or": [
            {"email": user.email},
            {"user_id": user.user_id}
        ]
    })
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    user.password = Hash.bcrypt(user.password)
    access_token = create_access_token(data={"sub": user.email})
    
    user_collection.insert_one(user.dict(by_alias=True))
    
    session_doc = {
        "user_id": user.user_id,
        "access_token": access_token,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    session_collection.insert_one(session_doc)
    
    return {"access_token": access_token, "message": "User created successfully"}

# User login route
@router.post('/login')
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), user_collection: Collection = Depends(get_user_collection), session_collection: Collection = Depends(get_session_collection)):
    email = form_data.username
    password = form_data.password
    
    user = user_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not verify_password(user["email"], password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": email})
    
    session_exist = session_collection.find_one({"user_id": user["user_id"]})
    if session_exist:
        session_collection.update_one(
            {"user_id": user["user_id"]}, 
            {"$set": 
                {
                    "access_token": access_token,
                    "updated_at": datetime.utcnow()
                }
            }
        )
    else:
        session_doc = {
            "user_id": user["user_id"],
            "access_token": access_token,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        session_collection.insert_one(session_doc)
    
    return {"access_token": access_token, "token_type": "bearer"}

# Delete a user account
@router.delete('/delete/{user_id}')
async def delete_user(user_id: str, user_collection: Collection = Depends(get_user_collection), session_collection: Collection = Depends(get_session_collection)):
    user = user_collection.find_one({"user_id": user_id})
    if user:
        user_collection.delete_one({"user_id": user_id})
        session_collection.delete_one({"user_id": user_id})
        return {"status": "success", "message": "User deleted"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

# Sign out a user
@router.delete('/signout/{user_id}')
async def signout_user(user_id: str, user_collection: Collection = Depends(get_user_collection), session_collection: Collection = Depends(get_session_collection)):
    user = user_collection.find_one({"user_id": user_id})
    if user:
        session_collection.delete_one({"user_id": user_id})
        return {"status": "success", "message": "User signed out"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

# Update user information
@router.put('/update/{user_id}')
async def update_user(user_id: str, user_update: UserUpdateModel, user_collection: Collection = Depends(get_user_collection)):
    user = user_collection.find_one({"user_id": user_id})
    if user:
        update_data = user_update.dict(exclude_unset=True)
        result = user_collection.update_one(
            {"user_id": user_id},
            {"$set": update_data}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=500, detail="Update failed")
        return {"status": "success", "message": "User updated"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

# Verify password method
def verify_password(email: str, password: str, user_collection: Collection = Depends(get_user_collection)) -> bool:
    user = user_collection.find_one({"email": email})
    if not user:
        return False
    return Hash.verify(user["password"], password)
