from sqlalchemy.orm import Session
from fastapi import Depends
from .db import SessionLocal

# Функция для получения сессии базы данных
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()