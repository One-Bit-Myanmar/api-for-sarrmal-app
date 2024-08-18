from fastapi import APIRouter, Request, Depends, HTTPException, status, Header
from pymongo.collection import Collection
from app.core.security import Hash, create_access_token, verify_token, get_current_active_user
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.core.config import connect_to_database
from app.db.models.User import User, UserUpdateModel
from app.core.config import connect_to_database, SECRET_KEY, ALGORITHM


# import slowapi modules
from app.api.middleware.rate_limiter import limiter

# Dependency injection for database connection
# get the user collection
def get_user_collection():
    db = connect_to_database()
    return db["food_recommendation_database"]["users"]

# get the session collection
def get_session_collection():
    db = connect_to_database()
    return db["food_recommendation_database"]["sessions"]

# init the api router
router = APIRouter()


# Get users list
@router.get('/get')
@limiter.limit("5/minute")
async def get_users(
    request: Request,
    user_collection: Collection = Depends(get_user_collection),
    current_user: User = Depends(get_current_active_user)
    ):
    
    users = list(user_collection.find({}))
    for item in users:
        item["_id"] = str(item["_id"])
    return {"response": "success", "data": users}





# Get specific user by ID
@router.get('/get/{user_id}')
@limiter.limit("5/minute")
async def get_user(
    user_id: str, 
    request: Request,
    user_collection: Collection = Depends(get_user_collection),
    current_user: User = Depends(get_current_active_user)
    ):
    
    user = user_collection.find_one({"user_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["_id"] = str(user["_id"])
    return {"response": "success" ,"data": user}



# Register a new user
@router.post('/register')
@limiter.limit("5/minute")
async def register_user( 
    user: User,
    request: Request,
    user_collection: Collection = Depends(get_user_collection), 
    session_collection: Collection = Depends(get_session_collection),
    ):
    
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
    
    return {"response": "success", "access_token": access_token, "message": "User created successfully"}




# User login route
@router.post('/login')
@limiter.limit("5/minute")
async def login_user( 
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_collection: Collection = Depends(get_user_collection),
    session_collection: Collection = Depends(get_session_collection),
    ):
    
    user = user_collection.find_one({"email": form_data.username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Call verify_password with the user_collection, email, and password
    if not verify_password(user_collection, form_data.username, form_data.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token_expires = timedelta(hours=1)
    access_token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
    
    # update the user database
    user_collection.update_one(
        {"email": form_data.username}, 
        {"$set": 
            {
                "disabled": False
            }
    })

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
@limiter.limit("5/minute")
async def delete_user(
    user_id: str, 
    request: Request,
    user_collection: Collection = Depends(get_user_collection),
    session_collection: Collection = Depends(get_session_collection),
    current_user: User = Depends(get_current_active_user)
    ):
    
    user = user_collection.find_one({"user_id": user_id})
    if user:
        user_collection.delete_one({"user_id": user_id})
        session_collection.delete_one({"user_id": user_id})
        return {"response": "success", "message": "User deleted Successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")




# Sign out a user
@router.put('/logout/{user_id}')
@limiter.limit("5/minute")
async def logout( 
    user_id: str, 
    request: Request,
    user_collection: Collection = Depends(get_user_collection), 
    session_collection: Collection = Depends(get_session_collection),
    current_user: User = Depends(get_current_active_user)
    ):
    
    user = user_collection.find_one({"user_id": user_id})
    if user:
        session_collection.delete_one({"user_id": user_id})
        # update the user database
        user_collection.update_one(
            {"email": user["email"]}, 
            {"$set": 
                {
                    "disabled": True
                }
        })
        return {"response": "success", "message": "User signed out"}
    else:
        raise HTTPException(status_code=404, detail="User not found")





# Update user information
@router.put('/update/{user_id}')
@limiter.limit("5/minute")
async def update_user( 
    user_id: str,
    request: Request,
    user_update: UserUpdateModel, 
    user_collection: Collection = Depends(get_user_collection),
    current_user: User = Depends(get_current_active_user)
    ):
    
    user = user_collection.find_one({"user_id": user_id})
    if user:
        update_data = user_update.dict(exclude_unset=True)
        result = user_collection.update_one(
            {"user_id": user_id},
            {"$set": update_data}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=500, detail="Update failed")
        return {"response": "success", "message": "User updated"}
    else:
        raise HTTPException(status_code=404, detail="User not found")




# Verify password method
def verify_password(user_collection: Collection, email: str, password: str) -> bool:
    user = user_collection.find_one({"email": email})
    if not user:
        return False
    return Hash.verify(user["password"], password)



# get the current active logined user
@router.get("/me", response_model=User)
@limiter.limit('5/minute')
async def read_users_me(
    request: Request,
    current_user: User = Depends(get_current_active_user)
    ):
    return current_user
