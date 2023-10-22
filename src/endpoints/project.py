import uuid
from sqlalchemy import and_
from fastapi import APIRouter, Query
from fastapi import Depends, HTTPException
from starlette import status
from sqlalchemy.orm import Session, joinedload, aliased
from starlette.requests import Request
from db import Project, Task
from datetime import datetime
from src.endpoints.auth import get_current_user
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


# Return projects and related tasks. Called on Task list page
@router.get("/tasks", response_model=list[ProjectGetResponse])
def get_projects(
    title: str = Query(None, title="title"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Retrieves a list of projects based on the provided filters.

    Parameters:
        - title (str): The title of the projects to filter by. Defaults to None.
        - db (Session): The database session to use for querying projects.
        - current_user: The current user making the request.

    Returns:
        - list[ProjectGetResponse]: A list of projects that match the provided filters.
    """
    if title:
        # Create a Task aliased table.
        TaskAlias = aliased(Task)

        # Filter out porjects that don't match the title.
        projects = (
            db.query(Project)
            .join(TaskAlias, Project.tasks)
            .filter(
                and_(
                    TaskAlias.title.startswith(title),
                    Project.user_id == current_user["id"],
                )
            )
            .options(joinedload(Project.tasks))
            .all()
        )
        # Filter out tasks that don't match the title.
        for project in projects:
            project.tasks = [
                task for task in project.tasks if task.title.startswith(title)
            ]
    else:
        try:
            projects = (
                db.query(Project)
                .filter(Project.user_id == current_user["id"])
                .options(joinedload(Project.tasks))
                .all()
            )
        except AttributeError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
            )
    return projects


# Return only projects. Called on Project list page
@router.get("", response_model=list[ProjectGetResponse])
def get_projects(
    title: str = Query(None, title="title"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Retrieves a list of projects based on the provided filters.

    Parameters:
        - title (str): The title of the projects to filter by. Defaults to None.
        - db (Session): The database session to use for querying projects.
        - current_user: The current user making the request.

    Returns:
        - list[ProjectGetResponse]: A list of projects that match the provided filters.
    """
    if title:
        projects = (
            db.query(Project)
            .filter(
                and_(
                    Project.title.startswith(title),
                    Project.user_id == current_user["id"],
                )
            )
            .all()
        )
    else:
        print(
            "current_user",
            current_user,
            db.query(Project).options(joinedload(Project.tasks)).all(),
        )
        try:
            projects = (
                db.query(Project).filter(Project.user_id == current_user["id"]).all()
            )
        except AttributeError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
            )
    return projects


# 単一のprojectを取得
@router.get("/{project_id}", response_model=ProjectGetResponse)
def get_project_by_id(
    project_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    project = get_project(db, project_id).filter(Project.user_id == current_user["id"])
    return project


user_dependency = Annotated[dict, Depends(get_current_user)]


# projectを登録
@router.post("", response_model=ProjectGetResponse)
async def create_project(
    project_created: ProjectCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    now = datetime.now()
    print("current_user", current_user)

    project = Project(
        title=project_created.title,
        status=project_created.status,
        to_date=project_created.to_date,
        from_date=project_created.from_date,
    )
    project.user_id = current_user["id"]
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
    project.from_date = project_created.from_date
    project.to_date = project_created.to_date
    project.user_id = current_user["id"]

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
