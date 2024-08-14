from fastapi import APIRouter, Request, Depends, HTTPException, status
from pymongo.collection import Collection
from app.core.security import Hash, create_access_token, verify_token
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
from app.core.config import connect_to_database

# get the database 
from app.db.mongodb import get_db
from app.db.models.User import User, UserUpdateModel # import the user model

db = connect_to_database()
db = db["food_recommendation_database"] # database name
user_collection = db["users"] # users table inside food_recommendation_database
session_collection = db["sessions"] # session_table inside food_recommendation_database

# define router
router = APIRouter()

# get users list
@router.get('/gets')
def get_users():
    # get the users list --- which is collection including objectId()
    users = list(user_collection.find({}))
    # change objectId() to string
    for item in users:
        item["_id"] = str(item["_id"])
    # return users
    return {"response": users}

# get specific users
@router.get('/get/{user_id}')
def get_user(user_id: str):
    # get the user by id
    user = user_collection.find_one({"user_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["_id"] = str(user["_id"])  # Convert ObjectId to string
    return {"response": user}


# register user
@router.post('/register')
def register_user(user: User):
    # check email is duplicate or not
    existing_user = user_collection.find_one({
        "$or": [
            {"email": user.email},
            {"user_id": user.user_id}
        ]
    })
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    # hash the password
    user.password = Hash.bcrypt(user.password)
    # create access token
    access_token = create_access_token(data={"sub": user.email})
    # insert into database
    user_collection.insert_one(user.dict(by_alias=True))
    # insert into session db
    session_doc = {
        "user_id": user.user_id,
        "access_token": access_token,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    # insert into session collection
    session_collection.insert_one(session_doc)
    # return json
    return {"access_token": access_token, "message": "User created successfully"}
    
    
# user login route
@router.post('/login')
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    # get the form data
    email = form_data.username
    password = form_data.password
    # find the user 
    user = user_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # verify the password 
    if not verify_password(email, password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    # create access token
    access_token = create_access_token(data={"sub": email})
    # check user_id is included in session table
    session_exist = session_collection.find_one({"user_id": user["user_id"]})
    if session_exist:
        # update the access token in session table
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
        # insert into session db
        session_doc = {
            "user_id": user["user_id"],
            "access_token": access_token,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        # insert into session collection
        session_collection.insert_one(session_doc)
    # return json
    return {"access_token": access_token, "token_type": "bearer"}


# delete the user account
@router.delete('/delete/{user_id}')
def delete_user(user_id: str):
    # check the user is exist or not
    if user_collection.find_one({"user_id": user_id}):    
        # delete user from user database
        user_collection.delete_one({"user_id": user_id})
        # delete from session database
        session_collection.delete_one({"user_id": user_id})
    else:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "success", "message": "User deleted"}


# sign out the user account
@router.delete('/signout/{user_id}')
def signout_user(user_id: str):
    # check the user is exist or not
    if user_collection.find_one({"user_id": user_id}):
        # delete from session database
        session_collection.delete_one({"user_id": user_id})
    else:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "success", "message": "User signed out"}


# update user information
@router.put('/update/{user_id}')
def update_user(user_id: str, user_update: UserUpdateModel):
    # check the user is exist or not
    if user_collection.find_one({"user_id": user_id}):
        # update hte user infor
        update_user = user_update.dict(exclude_unset=True)
        # update the user information
        result = user_collection.update_one(
            {"user_id": user_id},
            {"$set": update_user}
        )
        # if not modified
        if result.modified_count == 0:
            raise HTTPException(status_code=500, detail="Update failed")
    else:
        raise HTTPException(status_code=404, detail="User not found")
    # return json
    return {"status": "success", "message": "User updated"}


# verify password method
def verify_password(email: str, password: str) -> bool:
    user = user_collection.find_one({"email": email})
    if not user:
        return False
    return Hash.verify(user["password"], password)  # Verify hashed password

