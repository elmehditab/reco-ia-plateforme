from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    id: int
    name: str
    email: EmailStr

class User(UserCreate):
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime