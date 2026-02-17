from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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
    return {
        "name": user.name,
        "age": user.age,
        "status": "Пользователь создан"
    }
