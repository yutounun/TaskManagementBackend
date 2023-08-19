import uuid
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from pydantic import BaseModel, Field
from db import User, Task
from datetime import datetime
from sqlalchemy.orm import joinedload

# APIRouter creates path operations for item module
router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


# Pydanticを用いたAPIに渡されるデータの定義 ValidationやDocumentationの機能が追加される
class UserCreate(BaseModel):
    name: str = Field(..., example="Test user")
    email: str = Field(..., example="fefre@gmail.com")
    password: str = Field(..., example="ferwfwe")


class UserEdit(BaseModel):
    name: str = Field(..., example="Test user")
    email: str = Field(..., example="fefre@gmail.com")
    password: int = Field(..., example="32df3fq")


# 単一のuserを取得するためのユーティリティ
def get_user(db_session: Session, user_id: str):
    return db_session.query(User).filter(User.id == user_id).first()


# DB接続のセッションを各エンドポイントの関数に渡す
def get_db(request: Request):
    return request.state.db


# userの全取得
@router.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


# 単一のuserを取得
@router.get("/{user_id}")
def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    return user


# userを登録
@router.post("/")
async def create_user(user_created: UserCreate, db: Session = Depends(get_db)):
    now = datetime.now()

    user = User(
        name=user_created.name,
        email=user_created.email,
        password=user_created.password,
    )
    user.id = str(uuid.uuid4())
    user.created_at = now
    user.updated_at = now

    db.add(user)
    db.commit()
    user = get_user(db, user.id)
    return user


# userを更新
@router.put("/{user_id}")
async def update_user(
    user_id: str, user_created: UserEdit, db: Session = Depends(get_db)
):
    now = datetime.now()

    user = get_user(db, user_id)

    if not user:
        return {"error": "user not found"}, 404

    user.name = user_created.name
    user.email = user_created.email
    user.password = user_created.password
    user.from_date = user_created.from_date
    user.to_date = user_created.to_date

    user.updated_at = now

    db.commit()
    # return user that is committed already
    user = get_user(db, user_id)
    return user


# userを削除
@router.delete("/{user_id}")
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    user = get_user(db, user_id)

    if not user:
        return {"error": "user not found"}, 404

    db.delete(user)
    db.commit()
