from pydantic import BaseModel, Field
from datetime import datetime


# Pydanticを用いたAPIに渡されるデータの定義 ValidationやDocumentationの機能が追加される
# Class definition using BaseModel make models on swagger
class TaskCreateRequest(BaseModel):
    title: str = Field(..., example="Test Task")
    status: str = Field(..., example="pending")
    man_hour_min: int = Field(..., example=60)
    to_date: datetime = Field(..., example="2023-08-15T15:32:00Z")
    from_date: datetime = Field(..., example="2023-08-14T15:32:00Z")
    priority: int = Field(..., example=1)
    project_key: str = Field(..., example="32ed23f32f2311")
    user_key: str = Field(..., example="32ed23f32f2311")


class TaskGetResponse(BaseModel):
    id: str = Field(..., example="32ed23f32f2311")
    title: str = Field(..., example="Test Task")
    status: str = Field(..., example="pending")
    man_hour_min: int = Field(..., example=60)
    to_date: datetime = Field(..., example="2023-08-15T15:32:00Z")
    from_date: datetime = Field(..., example="2023-08-14T15:32:00Z")
    priority: int = Field(..., example=1)
    project_key: str = Field(..., example="32ed23f32f2311")
    user_key: str = Field(..., example="32ed23f32f2311")

    created_at: datetime
    updated_at: datetime


class TaskEditRequest(BaseModel):
    title: str = Field(..., example="Test Task")
    status: str = Field(..., example="pending")
    man_hour_min: int = Field(..., example=60)
    to_date: datetime = Field(..., example="2023-08-15T15:32:00Z")
    from_date: datetime = Field(..., example="2023-08-14T15:32:00Z")
    priority: int = Field(..., example=1)


class SimpleResponse(BaseModel):
    status: str = Field(..., example="ok")
