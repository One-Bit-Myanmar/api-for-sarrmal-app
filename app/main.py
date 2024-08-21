from fastapi import FastAPI, HTTPException, Depends, Request
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from typing import Callable
import uvicorn
import requests, jwt


# get configured env values
from app.core.config import HOST_ID, PORT_ID, RELOAD_STATE, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI
from app.db.mongodb import get_db

# include router here
from app.api.endpoints.users import router as UserRouter
from app.api.endpoints.chats import router as ChatRouter
from app.api.endpoints.foods import router as FoodRouter
from app.api.endpoints.food_histories import router as FoodHistoryRouter
from app.api.endpoints.temp_end import router as TempFoodRouter

# include middleware are herer
from app.api.middleware.rate_limiter import add_rate_limit
# from app.api.middleware.auth_middleware import AuthMiddleware

app = FastAPI()

# get database config method is here
db = get_db()

# for cors middleware /// aka default middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# include the middleware here
add_rate_limit(app) # this is the api call rate limiting middlewaer

# for routes from app.api.endpoints /// include the routes here
app.include_router(UserRouter, tags=["User"], prefix="/api/user") # user route
app.include_router(ChatRouter, tags=["Chat"], prefix="/api/ai") # chat route
app.include_router(FoodRouter, tags=["Food"], prefix="/api/food") # food router
app.include_router(FoodHistoryRouter, tags=["Food History"], prefix="/api/food-history") # food history route
app.include_router(TempFoodRouter, tags=["Temporary Foods"], prefix="/api/temp/food") # temp food router

# calling root directory
@app.get("/", tags=["Root"])
async def read_root(code: str = None):
    if code:
        token_url = "https://accounts.google.com/o/oauth2/token"
        data = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        response = requests.post(token_url, data=data)
        print(response.text)
        print()
        access_token = response.json().get("access_token")
        global GOOGLE_ACCESS_TOKEN
        GOOGLE_ACCESS_TOKEN = response.json().get("access_token")
        user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
        return access_token
    return {"message": "Welcome to food recommendation app"}

@app.get("/login/google")
async def login_google():
    return {"abcd": 'abcd'}
    

# @app.get("/token")
# async def get_token(token: str = Depends(oauth2_scheme)):
#     return jwt.decode(token, GOOGLE_CLIENT_SECRET, algorithms=["HS256"])

# main method to run the application ///// run api with command
if __name__ == "__main__":
    uvicorn.run(app, host=HOST_ID, port=PORT_ID, reload=RELOAD_STATE)



