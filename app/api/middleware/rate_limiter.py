from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

# Initialize SlowAPI Limiter
limiter = Limiter(key_func=get_remote_address)

# Define the rate limit exception handler
def rate_limit_error_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Try again later."}
    )

# Function to set up the rate limiter on your app
def add_rate_limit(app: FastAPI):
    # Register the exception handler globally
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_error_handler)
