from __future__ import annotations
import os
from datetime import datetime
from sqlalchemy import (
    ForeignKey,
    DateTime,
    Column,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

# SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

engine = create_engine(SQLALCHEMY_DATABASE_URI)

Base = declarative_base()


# Each task can be related to only one project
class Task(Base):
    __tablename__ = "Task"
    id = Column(String(36), primary_key=True, index=True)
    title = Column(String(100))
    status = Column(String(20))
    type = Column(String(20))
    man_hour_min = Column(Integer)
    to_date = Column(DateTime, default=datetime.now(), nullable=False)
    from_date = Column(DateTime, default=datetime.now(), nullable=False)
    priority = Column(String(100))
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), nullable=False)
    project_id = Column(String(), ForeignKey("Project.id"))
    user_id = Column(String(), ForeignKey("User.id"))

    # relationship
    project = relationship("Project", back_populates="tasks")
    user = relationship("User", back_populates="tasks")


# Each project can have multiple tasks
class Project(Base):
    __tablename__ = "Project"
    id = Column(String(36), primary_key=True, index=True)
    title = Column(String(200))
    status = Column(String(100))
    to_date = Column(DateTime, default=datetime.now(), nullable=False)
    from_date = Column(DateTime, default=datetime.now(), nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), nullable=False)
    user_id = Column(String(), ForeignKey("User.id"))

    # relationship
    tasks = relationship("Task", back_populates="project")
    user = relationship("User", back_populates="projects")


# Each user can have multiple tasks and projects
class User(Base):
    __tablename__ = "User"
    id = Column(String(36), primary_key=True, index=True)
    username = Column(String(100), index=True)
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
