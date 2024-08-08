
from app.util.oauth import get_current_user
from app.util.jwttoken import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from app.util.hashing import Hash
from app.models.UserModel import User

from fastapi import APIRouter, Request, Body, Depends, HTTPException, status
from app.models.UserModel import User
from bson import ObjectId

router = APIRouter()



# register user
@router.post('/register')
def create_user(request: Request, user: User = Body(...)):
    db = request.app.users
    hashed_pass = Hash.bcrypt(user.password)
    user.password = hashed_pass
    response = db.insert_one(user.model_dump())
    return {"id": str(response.inserted_id)}

# login user
@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends()):
    db = request.app.users
    user = db.find_one({"username": request.username})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not Hash.verify(user["password"],request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    access_token = create_access_token(data={"sub": user["username"] })
    return {"access_token": access_token, "token_type": "bearer"}
