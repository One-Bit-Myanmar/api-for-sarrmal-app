from fastapi import FastAPI, HTTPException, Depends, Request
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Callable
from fastapi.security import OAuth2PasswordBearer
import uvicorn

# get configured env values
from app.core.config import HOST_ID, PORT_ID, RELOAD_STATE
from app.db.mongodb import get_db

# include router here
from app.api.endpoints.users import router as UserRouter
from app.api.endpoints.chats import router as ChatRouter
from app.api.endpoints.foods import router as FoodRouter
from app.api.endpoints.food_histories import router as FoodHistoryRouter

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
# app.add_middleware(AuthMiddleware) # this is auth middleware 

# for routes from app.api.endpoints /// include the routes here
app.include_router(UserRouter, tags=["User"], prefix="/api/user") # user route
app.include_router(ChatRouter, tags=["Chat"], prefix="/api/ai") # chat route
app.include_router(FoodRouter, tags=["Food"], prefix="/api/food") # food router
app.include_router(FoodHistoryRouter, tags=["Food History"], prefix="/api/food-history") # food history route

# calling root directory
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to food recommendation app"}

# main method to run the application ///// run api with command
if __name__ == "__main__":
    uvicorn.run(app, host=HOST_ID, port=PORT_ID, reload=RELOAD_STATE)



