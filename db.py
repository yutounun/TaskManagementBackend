from sqlalchemy import Boolean, DateTime, Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

SQLALCHEMY_DATABASE_URI = "sqlite:///./test.db"
# SQLALCHEMY_DATABASE_URI = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}, echo=True
)

Base = declarative_base()


# Taskテーブルの定義
class Task(Base):
    __tablename__ = "Task"
    id = Column(String(36), primary_key=True)
    title = Column(String(200))
    status = Column(String(10))
    man_hour_min = Column(Integer)
    to_date = Column(DateTime, default=datetime.now(), nullable=False)
    from_date = Column(DateTime, default=datetime.now(), nullable=False)
    priority = Column(Integer)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), nullable=False)


# テーブル削除
# Base.metadata.drop_all(bind=engine)

# テーブル作成
Base.metadata.create_all(bind=engine)
