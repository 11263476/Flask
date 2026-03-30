from pydantic import BaseModel, EmailStr, Field  # Import Pydantic base classes
from typing import Optional  # Import Optional type

# --- User Schema: For data validation during registration ---
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50) # Username must be 3-50 chars
    email: str = Field(..., description="Valid email address") # Email validation
    password: str = Field(..., min_length=6) # Minimum 6 chars for security
    
# --- Login Schema: To validate user credentials ---
class UserLogin(BaseModel):
    username: str
    password: str

# --- Response Schema: What we send back (omits the password) ---
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True # Allow Pydantic to work with SQLAlchemy models
