
from app.util.oauth import get_current_user
from app.util.jwttoken import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from app.util.hashing import Hash
from app.models.UserModel import User

# Replace this with the actual way you access the database
from app.db.mongodb import connectToDatabase
from pymongo.collection import Collection

from fastapi import APIRouter, Request, Body, Depends, HTTPException, status
from app.models.UserModel import User
from bson import ObjectId

router = APIRouter()

# Assume `get_db` is a dependency that returns the database connection
client = connectToDatabase()
db = client['Cluster0']
users_collection = db["users"]

# get all user
@router.get("/get")
def get_user(request: Request) -> list[User]:
    db = request.app.users
    response = list(db.find({}))
    for item in response:
        item["_id"] = str(item["_id"])
    return response

@router.post('/register')
async def register_user(user: User):
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_password = Hash.bcrypt(user.password)
    user_document = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
    }
    
    users_collection.insert_one(user_document)
    return {"message": "User created successfully"}



# User login
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password 

    if not verify_password(username, password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": username})

    return {"access_token": access_token, "token_type": "bearer"}




def verify_password(username: str, password: str) -> bool:
    user = users_collection.find_one({"username": username})
    print(user)
    if not user:
        return False
    return Hash.verify(user["password"], password)  # Verify hashed password


