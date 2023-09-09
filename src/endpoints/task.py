import uuid
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette.requests import Request
from db import Task
from datetime import datetime
from starlette import status
from src.endpoints.auth import get_current_user
from src.types.task import (
    TaskCreateRequest,
    TaskGetResponse,
    TaskEditRequest,
    SimpleResponse,
)

# APIRouter creates path operations for item module
router = APIRouter(
    prefix="/tasks",
    tags=["Task"],
    responses={404: {"description": "Not found"}},
)


# utility func to get task by task_id
def get_task(db_session: Session, task_id: str):
    return db_session.query(Task).filter(Task.id == task_id).first()


# DB接続のセッションを各エンドポイントの関数に渡す
def get_db(request: Request):
    # this property is injected on main.py
    # the content of this property is the db session
    return request.state.db


# taskの全取得
@router.get("/", response_model=list[TaskGetResponse])
def get_tasks(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    tasks = db.query(Task).all()

    # project_idでProjectを検索

    return tasks


# 単一のtaskを取得
@router.get("/{task_id}", response_model=TaskGetResponse)
def get_task_by_id(
    task_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


# taskを登録
@router.post("/", response_model=TaskGetResponse)
async def create_task(
    task_created: TaskCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    now = datetime.now()

    task = Task(
        title=task_created.title,
        status=task_created.status,
        man_hour_min=task_created.man_hour_min,
        to_date=task_created.to_date,
        type=task_created.type,
        from_date=task_created.from_date,
        priority=task_created.priority,
        project_id=task_created.project_id,
        user_id=task_created.user_id,
    )
    task.id = str(uuid.uuid4())
    task.created_at = now
    task.updated_at = now

    db.add(task)
    db.commit()
    task = get_task(db, task.id)
    return task


# taskを更新
@router.put("/{task_id}", response_model=TaskGetResponse)
async def update_task(
    task_id: str,
    task_created: TaskEditRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    now = datetime.now()

    task = get_task(db, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    task.title = task_created.title
    task.status = task_created.status
    task.man_hour_min = task_created.man_hour_min
    task.from_date = task_created.from_date
    task.to_date = task_created.to_date
    task.priority = task_created.priority
    task.type = task_created.type
    task.project_id = task_created.project_id
    task.user_id = task_created.user_id

    task.updated_at = now

    db.commit()
    # return task that is committed already
    task = get_task(db, task_id)
    print("task", task)
    return task


# taskを削除
@router.delete("/{task_id}", response_model=SimpleResponse)
async def delete_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    task = get_task(db, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    db.delete(task)
    db.commit()
    return {"status": "OK"}
