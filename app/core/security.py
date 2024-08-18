from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.core.config import SECRET_KEY, ALGORITHM
from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.db.models.User import Token, TokenData, UserInDB, User
import jwt
from jose import JWTError
from app.db.mongodb import connect_to_database # connect to data fun will get db connection


pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto") # encode decode format
SECRET_KEY = SECRET_KEY # secrect key for encryption
ALGORITHM = ALGORITHM # type of algorithm used in secret key generation
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # only about 30 mins each token

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")


# Password hashing class
class Hash():
    # static method to use in other py file
    # bcrypt method to hash the password
    @staticmethod
    def bcrypt(password: str):
        return pwd_cxt.hash(password)
    
    # verify the hashed password with user input password
    @staticmethod
    def verify(hashed, normal):
        return pwd_cxt.verify(normal, hashed)
    
    
# create access token when user login or sign implementing along with expiration time
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy() # get the data dict as a copy to encode
    if expires_delta:
        expire = datetime.utcnow() + expires_delta # for the first time creation
    else:
        expire = datetime.utcnow() + timedelta(hours=1) # for the further creating of token
    to_encode.update({"exp": expire}) # update the token's time expiration
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # finally encode by jwt encoder
    return encoded_jwt # return that encoded key


# verify token function to check token is correct or not
def verify_token(token: str) -> dict:
    try:
        # so what i need to do is to decode that secret key
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # return the secret key
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    

# get the current user func to check the token if user is auth or not
# the next step we will create to get actually current active user
async def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    # credentail exception for incorrect token validation
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    try:
        print(f"Received token: {token}")  # Debug: Print received token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # to decode the token
        print(f"Decoded payload: {payload}")  # Debug: Print decoded payload
        # the key is "sub" which have been encoded while user login
        # then save to variable --> email as a String and save to Token data Model
        email: str = payload.get("sub")
        if payload is None:
            print("No email in token payload")  # Debug: Check if email is in payload
            raise credential_exception
        # token data is a TokenData model which has the email attri 
        token_data = TokenData(email=email)
    except JWTError as e:
        raise credential_exception 
    
    # get the users collection from mongodb
    db = connect_to_database()["food_recommendation_database"]["users"]
    # find the token_data email is exsit in database or not
    user = db.find_one({"email": token_data.email})
    # if none then raise the exception
    if user is None:
        print("User not found in database")  # Debug: User not found in DB
        raise credential_exception
    # else return that user
    return user


# get the current active user
async def get_current_active_user(
    user: User = Depends(get_current_user) # this para is depend on user, <<< get_current_user is ok, then get_current_active_user ok
):
    # check if user is disabled or not
    if user["disabled"] == False:
        # return that user
        return user
    else:
        # else return http exception
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
