import uuid
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from starlette import status
from sqlalchemy.orm import Session
from starlette.requests import Request
from pydantic import BaseModel, Field
from db import Project
from datetime import datetime
from src.endpoints.auth import get_current_user
from sqlalchemy.orm import joinedload
from typing import Annotated
from src.types.project import (
    ProjectCreateRequest,
    ProjectEditRequest,
    ProjectGetResponse,
    SimpleResponse,
)

# APIRouter creates path operations for item module
router = APIRouter(
    prefix="/projects",
    tags=["Project"],
    responses={404: {"description": "Not found"}},
)


# 単一のprojectを取得するためのユーティリティ
def get_project(db_session: Session, project_id: str):
    return (
        db_session.query(Project)
        .options(joinedload(Project.tasks))
        .filter(Project.id == project_id)
        .first()
    )


# DB接続のセッションを各エンドポイントの関数に渡す
def get_db(request: Request):
    return request.state.db


# projectの全取得
@router.get("/", response_model=list[ProjectGetResponse])
def get_projects(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    projects = db.query(Project).options(joinedload(Project.tasks)).all()
    return projects


# 単一のprojectを取得
@router.get("/{project_id}", response_model=ProjectGetResponse)
def get_project_by_id(
    project_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    project = get_project(db, project_id)
    return project


user_dependency = Annotated[dict, Depends(get_current_user)]


# projectを登録
@router.post("/", response_model=ProjectGetResponse)
async def create_project(
    project_created: ProjectCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    now = datetime.now()

    project = Project(
        title=project_created.title,
        status=project_created.status,
        total_man_hour_min=project_created.total_man_hour_min,
        to_date=project_created.to_date,
        from_date=project_created.from_date,
        user_key=project_created.user_key,
    )
    project.id = str(uuid.uuid4())
    project.created_at = now
    project.updated_at = now

    db.add(project)
    db.commit()
    # project = get_project(db, project.id)
    return project


# projectを更新
@router.put("/{project_id}", response_model=ProjectGetResponse)
async def update_project(
    project_id: str,
    project_created: ProjectEditRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    now = datetime.now()

    project = get_project(db, project_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )

    project.title = project_created.title
    project.status = project_created.status
    project.total_man_hour_min = project_created.total_man_hour_min
    project.from_date = project_created.from_date
    project.to_date = project_created.to_date

    project.updated_at = now

    db.commit()
    # return project that is committed already
    # project = get_project(db, project_id)
    return project


# projectを削除
@router.delete("/{project_id}", response_model=SimpleResponse)
async def delete_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    project = get_project(db, project_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )

    db.delete(project)
    db.commit()
    return SimpleResponse(status="OK")
