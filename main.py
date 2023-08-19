import uuid
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session, sessionmaker
from starlette.requests import Request
from pydantic import BaseModel
from db import Task, engine

from datetime import datetime

# DB接続用のセッションクラス インスタンスが作成されると接続する
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Pydanticを用いたAPIに渡されるデータの定義 ValidationやDocumentationの機能が追加される
class TaskCreate(BaseModel):
    title: str
    status: str
    man_hour_min: int
    to_date: datetime
    from_date: datetime
    priority: int


class TaskEdit(BaseModel):
    title: str
    status: str
    man_hour_min: int
    to_date: datetime
    from_date: datetime
    priority: int


# 単一のtaskを取得するためのユーティリティ
def get_task(db_session: Session, task_id: str):
    return db_session.query(Task).filter(Task.id == task_id).first()


# DB接続のセッションを各エンドポイントの関数に渡す
def get_db(request: Request):
    return request.state.db


# このインスタンスをアノテーションに利用することでエンドポイントを定義できる
app = FastAPI()


# taskの全取得
@app.get("/tasks")
def read_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks


# 単一のtaskを取得
@app.get("/tasks/{task_id}")
def read_task(task_id: str, db: Session = Depends(get_db)):
    task = get_task(db, task_id)
    return task


# taskを登録
@app.post("/tasks/")
async def create_task(task_created: TaskCreate, db: Session = Depends(get_db)):
    now = datetime.now()

    task = Task(
        title=task_created.title,
        status=task_created.status,
        man_hour_min=task_created.man_hour_min,
        to_date=task_created.to_date,
        from_date=task_created.from_date,
        priority=task_created.priority,
    )
    task.id = str(uuid.uuid4())
    task.created_at = now
    task.updated_at = now

    db.add(task)
    db.commit()
    task = get_task(db, task.id)
    return task


# taskを更新
@app.put("/tasks/{task_id}")
async def update_task(
    task_id: str, task_created: TaskEdit, db: Session = Depends(get_db)
):
    now = datetime.now()

    task = get_task(db, task_id)
    task.title = task_created.title
    task.status = task_created.status
    task.man_hour_min = task_created.man_hour_min
    task.from_date = task_created.from_date
    task.to_date = task_created.to_date
    task.priority = task_created.priority

    task.updated_at = now

    db.commit()
    # return task that is committed already
    task = get_task(db, task_id)
    return task


# taskを削除
@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str, db: Session = Depends(get_db)):
    task = get_task(db, task_id)
    db.delete(task)
    db.commit()


# リクエストの度に呼ばれるミドルウェア DB接続用のセッションインスタンスを作成
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response
