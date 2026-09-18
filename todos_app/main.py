from fastapi import FastAPI, Form, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from sqlalchemy.orm import Session
import uvicorn

from database import engine, SessionLocal, Base
import models

# models에 정의한 모든 클래스, 연결한 DB엔진에 테이블로 생성
Base.metadata.create_all(bind=engine)

# FastAPI() 객체 생성
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        # 마지막에 무조건 닫음
        db.close()

abs_path = os.path.dirname(os.path.realpath(__file__))
print(abs_path)

# templates/ 폴더 식별 객체 변수
templates = Jinja2Templates(directory=f"{abs_path}/templates")

# static/ 폴더를 fastapi에서 인식할 수 있도록 마운트시킴
app.mount("/static", StaticFiles(directory=f"{abs_path}/static"), name="static")

# http://localhost:8000
@app.get("/")
def home(request: Request,
        db_ss: Session = Depends(get_db)
         ):
    # 테이블 조회
    todos_list = db_ss.query(models.Todo).order_by(models.Todo.id.desc()).all()
    # print(todos_list)
    # for todo in todos_list:
    #     print(f"{todo.id}, {todo.task}")
    return templates.TemplateResponse(
        request = request,
        name = "index.html",
        context={ "todos": todos_list}
    )

# todo 데이터를 받아서 db 테이블에 저장하기
# http://localhost:8000/add/
@app.post("/add")
def add(request: Request, 
        task: str = Form(...),
        db_ss: Session = Depends(get_db)
        ):
    print(task)
    # task 데이터를 받고, Todo클래스 토해서, 테이블과 연결된 객체생성
    todo = models.Todo(task=task)

    # todos 테이블에 task 추가
    db_ss.add(todo)

    # 테이블에 반영
    db_ss.commit()

    # 엔드포인트 함수 home으로 redirect 
    return RedirectResponse(url=app.url_path_for("home"),
                            status_code=status.HTTP_303_SEE_OTHER)


# todo 수정할 레코드 조회
@app.get("/edit/{todo_id}")
def edit(request: Request, 
         todo_id: int,
         db_ss: Session = Depends(get_db)):

    # 수정 요청 id로 todo 조회
    todo = db_ss.query(models.Todo).filter(models.Todo.id==todo_id).first()
    print(todo.task)

    # 예외처리
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    # 조회 결과 edit.html에 렌더링 해서 응답하기
    return templates.TemplateResponse(
        request=request,
        name = "edit.html",
        context = {"todo": todo}
    )

# todo 수정 내용 반영하기    
@app.post("/edit/{todo_id}")
def update(request: Request, 
           todo_id: int, 
           task: str = Form(...), 
           completed: bool = Form(False), 
           db: Session = Depends(get_db)):
    # todo_id로 조회
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    # task와 completed 테이블에 업데이트
    todo.task = task
    todo.completed = completed
    # 트렌젝션에서 변경내용 db에 최종 반영
    db.commit()
    return RedirectResponse(
        url=app.url_path_for("home"), 
        status_code=status.HTTP_303_SEE_OTHER)

# todo 삭제
# todo 수정할 레코드 조회
@app.get("/delete/{todo_id}")
def edit(request: Request, 
         todo_id: int,
         db_ss: Session = Depends(get_db)):
    
    # todo_id 조회
    todo = db_ss.query(models.Todo).filter(models.Todo.id==todo_id).first()
    # 삭제  
    db_ss.delete(todo)
    # 트렌젝션의 변경 내용을 db에 최종 반영
    db_ss.commit()

    return RedirectResponse(
        url=app.url_path_for("home"), 
        status_code=status.HTTP_303_SEE_OTHER)

# uv run fastapi dev
# uv run main.py
if __name__ == "__main__":
    # uvicorn.run("현재_파일이름:FastAPI객체_식별자", reload=True)
    # reload=True  : 개발자 모드
    uvicorn.run("main:app", reload=True)