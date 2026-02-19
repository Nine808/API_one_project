from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./users.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)

Base.metadata.create_all(bind=engine)


app = FastAPI()
users = []
current_id = 1

@app.get("/")
def read_root():
    return {"message": "Привет, FastAPI!"}
@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Привет, {name}!"}

class User(BaseModel):
    name: str
    age: int

@app.post("/users/")
def create_user(user: User):
    db = SessionLocal()

    new_user = UserDB(name=user.name, age=user.age)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    db.close()

    return {
        "id": new_user.id,
        "name": new_user.name,
        "age": new_user.age
    }

@app.get("/users/")
def get_users():
    db = SessionLocal()
    users = db.query(UserDB).all()
    db.close()
    return users

@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: User):
    db = SessionLocal()

    user = db.query(UserDB).filter(UserDB.id == user_id).first()

    if not user:
        db.close()
        return {"error": "Пользователь не найден"}

    user.name = updated_user.name
    user.age = updated_user.age

    db.commit()
    db.refresh(user)
    db.close()

    return {
        "id": user.id,
        "name": user.name,
        "age": user.age
    }




