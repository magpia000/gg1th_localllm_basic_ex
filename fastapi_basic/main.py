from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from typing import Optional
import uvicorn   # fastapi 내장 웹서버

# FastAPI 객체 생성
app = FastAPI()

# DTO : 데이터 전송 객체
class UserCreate(BaseModel):
    username: str
    password: str
    avatar_url: Optional[HttpUrl] = None
    user_fullname: Optional[str] = None

# DTO : 응답 전송 객체
class UserResponse(BaseModel):
    username: str
    avatar_url: HttpUrl

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

@app.post("/user_info/", response_model=UserResponse)
def create_user(user: UserCreate):
    # 비즈니스 로직 처리
    print(f"username: {user.username}")
    print(f"avatar_url: {user.avatar_url}")
    print(f"user_fullname: {user.user_fullname}")

    user_info = UserResponse(
        username = user.username,
        avatar_url = user.avatar_url
    )
    return user_info
    # return {"user": user}


@app.post("/user_info/{user_id}")
def create_user(user_id: int, q: str | None = None):
    # 비즈니스 로직 처리
    print(f"user_id: {user_id}, q: {q}")

    return {"user_id": user_id, "q": q}

# uv run fastapi dev
# uv run main.py
if __name__ == "__main__":
    # uvicorn.run("현재_파일이름:FastAPI객체_식별자", reload=True)
    # reload=True  : 개발자 모드
    uvicorn.run("main:app", reload=True)