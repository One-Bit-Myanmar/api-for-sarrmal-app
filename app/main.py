from fastapi import FastAPI, HTTPException, Depends, Request
from contextlib import asynccontextmanager
import uvicorn

# get configured env values
from app.core.config import HOST_ID, PORT_ID, RELOAD_STATE
from app.db.mongodb import get_db

# from middleware modules
from app.api.middleware.SlowAPIRateLimiting import limiter, _rate_limit_exceeded_handler

# include router here
from app.api.endpoints.users import router as UserRouter
from app.api.endpoints.chats import router as ChatRouter

app = FastAPI()

# get database config method is here
db = get_db()

# for cors middleware /// aka default middleware

# rate limiting middleware
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

# include the middleware here

# for routes from app.api.endpoints /// include the routes here
app.include_router(UserRouter, tags=["User"], prefix="/api/user") # user route
app.include_router(ChatRouter, tags=["Chat"], prefix="/api/chat")


# calling root directory
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to food recommendation app"}

# main method to run the application ///// run api with command
if __name__ == "__main__":
    uvicorn.run(app, host=HOST_ID, port=PORT_ID, reload=RELOAD_STATE)



