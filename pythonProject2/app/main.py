from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.backend.db_depends import SessionLocal
from app.backend.db import engine
from app.models.user import Base  # Убедитесь, что вы действительно импортируете Base из вашего файла с моделями


app = FastAPI()

# Create the database tables
models.Base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.CreateUser)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/tasks/", response_model=schemas.CreateTask)
def create_task(task: schemas.CreateTask, db: Session = Depends(get_db)):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task