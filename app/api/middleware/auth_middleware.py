from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError, jwt
from app.core.security import verify_token
from app.db.mongodb import connect_to_database

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        authorization: str = request.headers.get("Authorization")
        
        if authorization:
            try:
                token_type, token = authorization.split()
                if token_type.lower() != "bearer":
                    raise credentials_exception
                
                email = verify_token(token, credentials_exception)
                user_collection = connect_to_database()
                user_collection = user_collection["food_recommendation_database"]["users"]
                user = user_collection.find_one({"email": email})
                
                if user:
                    request.state.user = user
                else:
                    raise credentials_exception

            except JWTError:
                raise credentials_exception
        else:
            request.state.user = None

        response = await call_next(request)
        return response
