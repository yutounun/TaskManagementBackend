from __future__ import annotations
from sqlalchemy import (
    ForeignKey,
    DateTime,
    Column,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from typing import List
from sqlalchemy.orm import Mapped, mapped_column

# from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship

SQLALCHEMY_DATABASE_URI = "sqlite:///./test.db"
# SQLALCHEMY_DATABASE_URI = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}, echo=True
)

Base = declarative_base()


# Each task can be related to only one project
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
    project_key = Column(String(), ForeignKey("Project.id"))
    user_key = Column(String(), ForeignKey("User.id"))

    # relationship
    project = relationship("Project", back_populates="tasks")
    user = relationship("User", back_populates="tasks")


# Each project can have multiple tasks
class Project(Base):
    __tablename__ = "Project"
    id = Column(String(36), primary_key=True)
    title = Column(String(200))
    status = Column(String(10))
    total_man_hour_min = Column(Integer)
    to_date = Column(DateTime, default=datetime.now(), nullable=False)
    from_date = Column(DateTime, default=datetime.now(), nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), nullable=False)
    user_key = Column(String(), ForeignKey("User.id"))

    # relationship
    tasks = relationship("Task", back_populates="project")
    user = relationship("User", back_populates="projects")


# Each user can have multiple tasks and projects
class User(Base):
    __tablename__ = "User"
    id = Column(String(36), primary_key=True)
    username = Column(String(100))
    email = Column(String(100))
    password = Column(String(100))
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), nullable=False)

    # relationship
    tasks = relationship("Task", back_populates="user")
    projects = relationship("Project", back_populates="user")


# Clear all tables
# Base.metadata.drop_all(bind=engine)

# Create all tables
Base.metadata.create_all(bind=engine)
