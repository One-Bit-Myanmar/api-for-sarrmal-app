from fastapi import APIRouter, Request, Depends, HTTPException, status, Header
from pymongo.collection import Collection
from app.core.security import Hash, create_access_token, verify_token, get_current_active_user
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.core.config import connect_to_database
from app.db.models.User import User, UserUpdateModel
from app.core.config import connect_to_database, SECRET_KEY, ALGORITHM
from bson import ObjectId


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
    request: Request, # without this limiter not work
    user_collection: Collection = Depends(get_user_collection), # get the user collection
    current_user: User = Depends(get_current_active_user) # for active user if not then it not work
    ):
    # get the user list
    users = list(user_collection.find({}))
    for item in users: # change the objectId to string so that we can get from json string
        item["_id"] = str(item["_id"])
    # return users as a json format
    return {"response": "success", "data": users}





# Get specific user by ID
@router.get('/get/{user_id}')
@limiter.limit("5/minute")
async def get_user(
    user_id: str, # user id from url
    request: Request, # without this the limiter won't work
    user_collection: Collection = Depends(get_user_collection), # get the user collection 
    current_user: User = Depends(get_current_active_user) # for active user if not then it won't work
    ):
    # find the user by user_id
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    # check user is exist or not
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # then we need to change from objecId to String data type
    user["_id"] = str(user["_id"])
    # return the requested user as a json or dict
    return {"response": "success" ,"data": user}



# Register a new user
@router.post('/register')
@limiter.limit("5/minute")
async def register_user( 
    user: User, # User format that we will get
    request: Request, # without this the limiter won't work
    user_collection: Collection = Depends(get_user_collection),  # get the user collection
    session_collection: Collection = Depends(get_session_collection), # get the session collection
    ):
    # check user is exist or not by email or user_id 
    existing_user = user_collection.find_one({
        "$or": [
            {"email": user.email},
        ]
    })
    # if user is existed, then raise the Http error that user is already existed
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    # get the user password and hashed it and the create access token to make sure for auth
    user.password = Hash.bcrypt(user.password)
    # create access token expires for token expiration time
    access_token_expires = timedelta(hours=1)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    
    # then insert into user colllection of mongodb cluster
    user_collection.insert_one(user.dict(by_alias=True))
    # then we will need to create session dict to save into our session collection
    session_doc = {
        "email": user.email,
        "access_token": access_token,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    # insert into session collection of mongodb cluster
    session_collection.insert_one(session_doc)
    # finnally return the response that user is created successfully
    return {"response": "success", "access_token": access_token, "message": "User created successfully"}




# User login route
@router.post('/login')
@limiter.limit("5/minute")
async def login_user( 
    request: Request, # without this the limiter won't work
    form_data: OAuth2PasswordRequestForm = Depends(), # to form data input
    user_collection: Collection = Depends(get_user_collection), # for user collection from mongodb database
    session_collection: Collection = Depends(get_session_collection), # get session collection from mongodb database
    ):
    # first, we need to check if user is exist or not by user email 
    # assump that form_data.username as user email
    user = user_collection.find_one({"email": form_data.username})
    # if not found, then raise the Http Exception that user not found
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Call verify_password with the user_collection, email, and password
    if not verify_password(user_collection, form_data.username, form_data.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    # create access token expires for token expiration time
    access_token_expires = timedelta(hours=1)
    # after that create access token and assign to access_token variable
    access_token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
    
    # update the user database by setting disable disabled to False that user is logined in so the account is active
    user_collection.update_one(
        {"email": form_data.username}, 
        {"$set": 
            {
                "disabled": False
            }
    })
    # after that we also need to update our session database as access token is new due to repeat login
    session_exist = session_collection.find_one({"email": user["email"]})
    if session_exist: # check the session is exist or not by user_id 
        # if exist, then update that
        session_collection.update_one(
            {"email": user["email"]}, 
            {"$set": 
                {
                    "access_token": access_token,
                    "updated_at": datetime.utcnow()
                }
            }
        )
    else:
        # else create the session dict for saving into session collection of mongodb database
        session_doc = {
            "email": user["email"],
            "access_token": access_token,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        session_collection.insert_one(session_doc)
    # finally, we will return the access token that it was successfully login
    return {"access_token": access_token, "token_type": "bearer"}





# Delete a user account by someone
@router.delete('/delete/{user_id}')
@limiter.limit("5/minute")
async def delete_user(
    user_id: str, # that will get from url bar
    request: Request, # without this the limiter won't work
    user_collection: Collection = Depends(get_user_collection), # make sure the user collection is accessble if yes, then this func will work successfully
    session_collection: Collection = Depends(get_session_collection), # also make sure for the session collection
    current_user: User = Depends(get_current_active_user) # for user auth that the current user must be the active one
    ):
    # check the user is exist or not
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    if user: # if exist
        user_collection.delete_one({"_id": ObjectId(user_id)}) # delete that account
        session_collection.delete_one({"email": user["email"]}) # delete the session
        return {"response": "success", "message": "User deleted Successfully"} # repsone that the account was deleted successfully
    else:
        # else we will raise an error for that mistake
        raise HTTPException(status_code=404, detail="User not found")



# Delete a user account on my own
@router.delete('/delete')
@limiter.limit("5/minute")
async def delete_user(
    request: Request, # without this the limiter won't work
    user_collection: Collection = Depends(get_user_collection), # make sure the user collection is accessble if yes, then this func will work successfully
    session_collection: Collection = Depends(get_session_collection), # also make sure for the session collection
    current_user: User = Depends(get_current_active_user) # for user auth that the current user must be the active one
    ):
    # check the user is exist or not
    if current_user: # if exist
        user_collection.delete_one({"_id": current_user["_id"]}) # delete that account
        session_collection.delete_one({"email": current_user["email"]}) # delete the session
        return {"response": "success", "message": "User deleted Successfully"} # repsone that the account was deleted successfully
    else:
        # else we will raise an error for that mistake
        raise HTTPException(status_code=404, detail="User not found")


# Sign out a user
@router.put('/logout')
@limiter.limit("5/minute")
async def logout(  
    request: Request, # without this the limiter wonkl't work
    user_collection: Collection = Depends(get_user_collection), # to work func correctly make sure the db dependency is accessible
    session_collection: Collection = Depends(get_session_collection), # also for the session collection of mongodb cluster
    current_user: User = Depends(get_current_active_user) # for user auth, get the current active user
    ):
    # find the user is login or not /// exist or not
    user = user_collection.find_one({"_id": current_user["_id"]}) # user key["value"] as it is a dict
    if user:
        session_collection.delete_one({"email": current_user["email"]})
        # update the user database
        user_collection.update_one(
            {"email": user["email"]}, 
            {"$set": 
                {
                    "disabled": True
                }
        })
        # return that that account is logout successfully
        return {"response": "success", "message": "User signed out"}
    else:
        raise HTTPException(status_code=404, detail="User not found")





# Update user information by someone
@router.put('/update/{user_id}')
@limiter.limit("5/minute")
async def update_user( 
    user_id: str, # user id that we want to update
    request: Request, # without this limiter not work
    user_update: UserUpdateModel, # a Schemas model for partial updating
    user_collection: Collection = Depends(get_user_collection), # make sure user collection is accessible 
    current_user: User = Depends(get_current_active_user) # make sure current user is active 
    ):
    # find the user by user_id from collection of monogdb cluster
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    # if exist
    if user:
        # update the user with the format wit h UserUpdateModel
        update_data = user_update.dict(exclude_unset=True)
        result = user_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        # if modified not done, then raise the error
        if result.modified_count == 0:
            raise HTTPException(status_code=500, detail="Update failed")
        # finally if success, then response that user is updated successfully
        return {"response": "success", "message": "User updated"}
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
    
# Update user information on my own
@router.put('/update')
@limiter.limit("5/minute")
async def update_user( 
    request: Request, # user id that we want to update
    user_update: UserUpdateModel, # a Schemas model for partial updating
    user_collection: Collection = Depends(get_user_collection), # make sure user collection is accessible 
    current_user: User = Depends(get_current_active_user) # make sure current user is active 
    ):
    # find the user by user_id from collection of monogdb cluster
    user = user_collection.find_one({"_id": current_user["_id"]})
    # if exist
    if user:
        # update the user with the format wit h UserUpdateModel
        update_data = user_update.dict(exclude_unset=True)
        result = user_collection.update_one(
            {"_id": current_user["_id"]},
            {"$set": update_data}
        )
        # if modified not done, then raise the error
        if result.modified_count == 0:
            raise HTTPException(status_code=500, detail="Update failed")
        # finally if success, then response that user is updated successfully
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
    request: Request, # without this limiter not work
    current_user: User = Depends(get_current_active_user)
    ):
    current_user["_id"] = str(current_user["_id"])
    return current_user
