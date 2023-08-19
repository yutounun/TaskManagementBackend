import uuid
from fastapi import APIRouter
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session, sessionmaker
from starlette.requests import Request
from pydantic import BaseModel, Field
from db import Task
from datetime import datetime

# APIRouter creates path operations for item module
router = APIRouter(
    prefix="/task",
    tags=["Task"],
    responses={404: {"description": "Not found"}},
)


# Pydanticを用いたAPIに渡されるデータの定義 ValidationやDocumentationの機能が追加される
class TaskCreate(BaseModel):
    title: str = Field(..., example="Test Task")
    status: str = Field(..., example="pending")
    man_hour_min: int = Field(..., example=60)
    to_date: datetime = Field(..., example="2023-08-15T15:32:00Z")
    from_date: datetime = Field(..., example="2023-08-14T15:32:00Z")
    priority: int = Field(..., example=1)


class TaskEdit(BaseModel):
    title: str = Field(..., example="Test Task")
    status: str = Field(..., example="pending")
    man_hour_min: int = Field(..., example=60)
    to_date: datetime = Field(..., example="2023-08-15T15:32:00Z")
    from_date: datetime = Field(..., example="2023-08-14T15:32:00Z")
    priority: int = Field(..., example=1)


# 単一のtaskを取得するためのユーティリティ
def get_task(db_session: Session, task_id: str):
    return db_session.query(Task).filter(Task.id == task_id).first()


# DB接続のセッションを各エンドポイントの関数に渡す
def get_db(request: Request):
    return request.state.db


# このインスタンスをアノテーションに利用することでエンドポイントを定義できる
# app = FastAPI()


# taskの全取得
@router.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks


# 単一のtaskを取得
@router.get("/tasks/{task_id}")
def get_task(task_id: str, db: Session = Depends(get_db)):
    task = get_task(db, task_id)
    return task


# taskを登録
@router.post("/tasks/")
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
@router.put("/tasks/{task_id}")
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
@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str, db: Session = Depends(get_db)):
    task = get_task(db, task_id)
    db.delete(task)
    db.commit()