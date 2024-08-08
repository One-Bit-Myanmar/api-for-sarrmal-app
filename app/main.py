from fastapi import FastAPI, HTTPException, Depends, Request, status
from contextlib import asynccontextmanager
from app.db.mongodb import connectToDatabase
from app.middleware.logging_middleware import LoggingMiddleware

# for cors middleware
from fastapi.middleware.cors import CORSMiddleware

# routers
from app.server.routes.player_route import router as PlayerRouter
from app.server.routes.user_route import router as UserRouter


origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    dbHost = connectToDatabase()
    app.players = dbHost.tournament.players # get the player table from tournament db
    app.users = dbHost.tournament.users
    print("startup has begun!!")
    yield
    print("shutdown has begun!!")

# create the application
app = FastAPI(lifespan=lifespan)

# include the middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include all the router
app.include_router(PlayerRouter, tags=['Player'], prefix="/player") # player route
app.include_router(UserRouter, tags=['User'], prefix="/user") # user route

# Root Dir Route
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}


# Main method to run
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000, reload=True)