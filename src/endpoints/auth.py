import uuid
import os
from fastapi import APIRouter
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from starlette.requests import Request
from starlette import status
from pydantic import BaseModel, Field
from db import User
from passlib.context import CryptContext
from dotenv import load_dotenv

# a library to read .env file
load_dotenv()

# APIRouter creates path operations for item module
router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)


# Read .env file
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")


class LoginRequest(BaseModel):
    username: str
    password: str


class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: str


class EditUserRequest(BaseModel):
    username: str = Field(..., example="Test user")
    email: str = Field(..., example="fefre@gmail.com")
    password: int = Field(..., example="32df3fq")


# 単一のuserを取得するためのユーティリティ
def get_user(db_session: Session, user_id: str):
    return db_session.query(User).filter(User.id == user_id).first()


def get_user_by_username(db_session: Session, username: str):
    return db_session.query(User).filter(User.username == username).first()


# DB接続のセッションを各エンドポイントの関数に渡す
def get_db(request: Request):
    return request.state.db


@router.post("/login", response_model=Token)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    # get current user and make sure entered password
    # and hashed password on DB are matched
    user = authenticate_user(request.username, request.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    # create access token from username and id
    token = create_access_token(
        user.username,
        user.id,
        user.email,
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": token, "token_type": "bearer", "user_id": user.id}


def authenticate_user(username: str, password: str, db: Session):
    # get current user
    user = get_user_by_username(db, username)

    if not user:
        return False
    # password is hashed and checked if match
    if not bcrypt_context.verify(password, user.password):
        return False

    return user


def create_access_token(
    username: str, user_id: str, email: str, expires_delta: timedelta
):
    # created token will be expired at current time + specified minutes
    expire = datetime.utcnow() + expires_delta
    encode = {"sub": username, "id": user_id, "email": email, "exp": expire}
    encoded_jwt = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# This func is called by all APIs
# to authenticate user and get current user info
async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        # transform access token to payload with username and id
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("id")
        email: str = payload.get("email")
        expire: datetime = payload.get("exp")
        transformedExpire = datetime.utcfromtimestamp(expire)

        if transformedExpire < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
            )

        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        return {"username": username, "id": user_id, "email": email}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


# userの全取得
@router.get("")
def get_users(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    users = db.query(User).all()
    return users


# 単一のuserを取得
@router.get("/{user_id}")
def get_user_by_id(
    user_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    user = get_user(db, user_id)
    return user


# userを登録
@router.post("")
async def create_user(user_created: CreateUserRequest, db: Session = Depends(get_db)):
    now = datetime.now()

    user = User(
        username=user_created.username,
        email=user_created.email,
        password=bcrypt_context.hash(user_created.password),  # hash password
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
    user_id: str,
    user_created: EditUserRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    now = datetime.now()

    user = get_user(db, user_id)

    if not user:
        return {"error": "user not found"}, 404

    user.username = user_created.username
    user.email = user_created.email
    user.password = bcrypt_context.hash(user_created.password)
    user.from_date = user_created.from_date
    user.to_date = user_created.to_date

    user.updated_at = now

    db.commit()
    # return user that is committed already
    user = get_user(db, user_id)
    return user


# userを削除
@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    user = get_user(db, user_id)

    if not user:
        return {"error": "user not found"}, 404

    db.delete(user)
    db.commit()
