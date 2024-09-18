from fastapi import FastAPI, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List

from app.models import User
from app.schemas import CreateUser, UpdateUser
from app.backend.db_depends import get_db  # Убедитесь, что у вас есть функция get_db

app = FastAPI()


# Создание нового пользователя
class UserDB:
    pass


@app.post("/user/", response_model=User)
async def create_user(user: CreateUser, db: Session = next(get_db())):
    # Проверяем, существует ли пользователь с таким именем
    existing_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    new_user = UserDB(firstname=user.firstname, lastname=user.lastname, age=user.age)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Обновление пользователя
@app.put("/user/{user_id}", response_model=User)
async def update_user(user_id: int, user: UpdateUser, db: Session = next(get_db())):
    existing_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    existing_user.firstname = user.firstname
    existing_user.lastname = user.lastname
    existing_user.age = user.age
    db.commit()
    db.refresh(existing_user)
    return existing_user

# Удаление пользователя
@app.delete("/user/{user_id}", response_model=User)
async def delete_user(user_id: int, db: Session = next(get_db())):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return user