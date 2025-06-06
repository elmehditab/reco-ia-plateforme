from fastapi import FastAPI
from app.models.user import User, UserCreate
from datetime import datetime


app = FastAPI()
fake_users_db = [] 

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify that the service is running.
    """
    return {"status": "ok"}

@app.get("/users")
async def get_users():
    return fake_users_db

@app.post("/users")
async def create_user(user_data: UserCreate):
    now = datetime.utcnow()
    user = User(
        **user_data.dict(),
        is_active=True,
        is_verified=False,
        created_at=now,
        updated_at=now
    )
    fake_users_db.append(user)
    return {"message": "User created successfully", "user": user}