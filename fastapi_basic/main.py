from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from typing import Optional

# FastAPI 객체 생성
app = FastAPI()

# DTO : 데이터 전송 객체
class UserCreate(BaseModel):
    username: str
    password: str
    avatar_url: Optional[HttpUrl] = None
    user_fullname: Optional[str] = None


# http://localhost:8000/
# http://127.0.0.1:8000/
@app.get("/")
async def read_root():
    # 비즈니스 로직
    data = "db에 데이터 읽어오기"
    return {"message": data}

# http://localhost:8000/items
@app.get("/items")
def read_item():
    item_id = 1
    q = "사과"
    return {"item_id": item_id, "q": q}

# http://localhost:8000/items/300?q=치킨
# http://localhost:8000/items/100?q=사과
# http://localhost:8000/items/200?q=배
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
# def read_item(item_id, q):
    # 비즈니스 로직 처리
    print(f"item_id: {item_id}, q: {q}")

    return {"item_id": item_id, "q": q}

@app.post("/user_info/")
def create_user(user: UserCreate):
    # 비즈니스 로직 처리
    print(f"username: {user.username}")
    print(f"avatar_url: {user.avatar_url}")
    print(f"user_fullname: {user.user_fullname}")

    return user
    # return {"user": user}


@app.post("/user_info/{user_id}")
def create_user(user_id: int, q: str | None = None):
    # 비즈니스 로직 처리
    print(f"user_id: {user_id}, q: {q}")

    return {"user_id": user_id, "q": q}