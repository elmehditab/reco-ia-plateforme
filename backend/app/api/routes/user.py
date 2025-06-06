from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List

from app.models.user import User, UserCreate, UserUpdate

router = APIRouter()
fake_users_db = []
user_id_counter = 1 

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.get("/users", response_model=List[User])
async def get_users():
    return fake_users_db

@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    for user in fake_users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/users", response_model=User)
async def create_user(user_data: UserCreate):
    global user_id_counter
    now = datetime.utcnow()
    user = User(
        id=user_id_counter,
        name=user_data.name,
        email=user_data.email,
        is_active=True,
        is_verified=False,
        created_at=now,
        updated_at=now
    )
    fake_users_db.append(user)
    user_id_counter += 1
    return user

@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, updates: UserUpdate):
    for i, user in enumerate(fake_users_db):
        if user.id == user_id:
            updated_data = user.dict()
            update_fields = updates.dict(exclude_unset=True)

            updated_data.update(update_fields)
            updated_data["updated_at"] = datetime.utcnow()

            updated_user = User(**updated_data)
            fake_users_db[i] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    for i, user in enumerate(fake_users_db):
        if user.id == user_id:
            fake_users_db.pop(i)
            return {"message": f"User {user_id} deleted"}
    raise HTTPException(status_code=404, detail="User not found")
