from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

# create a Limiter instance
limiter = Limiter(key_func=get_remote_address)

