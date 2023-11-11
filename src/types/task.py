from pydantic import BaseModel, Field
from datetime import datetime


# Pydanticを用いたAPIに渡されるデータの定義 ValidationやDocumentationの機能が追加される
# Class definition using BaseModel make models on swagger
class TaskCreateRequest(BaseModel):
    title: str = Field(..., example="Test Task")
    status: str = Field(..., example="pending")
    type: str = Field(None, example="mtg")
    man_hour_min: int = Field(None, example=60)
    to_date: datetime = Field(..., example="2023-08-15T15:32:00Z")
    from_date: datetime = Field(..., example="2023-08-14T15:32:00Z")
    priority: str = Field(..., example="critical")
    project_id: str = Field(..., example="32ed23f32f2311")
    user_id: str = Field(None, example="32ed23f32f2311")


class TaskGetResponse(BaseModel):
    id: str = Field(..., example="32ed23f32f2311")
    title: str = Field(..., example="Test Task")
    status: str = Field(..., example="pending")
    type: str = Field(None, example="mtg")
    man_hour_min: int = Field(None, example=60)
    to_date: datetime = Field(..., example="2023-08-15T15:32:00Z")
    from_date: datetime = Field(..., example="2023-08-14T15:32:00Z")
    priority: str = Field(..., example="critical")
    project_id: str = Field(..., example="32ed23f32f2311")

    created_at: datetime
    updated_at: datetime


class TaskEditRequest(BaseModel):
    title: str = Field(..., example="Test Task")
    type: str = Field(..., example="mtg")
    status: str = Field(..., example="pending")
    man_hour_min: int = Field(..., example=60)
    to_date: datetime = Field(..., example="2023-08-15T15:32:00Z")
    from_date: datetime = Field(..., example="2023-08-14T15:32:00Z")
    priority: str = Field(..., example="critical")
    project_id: str = Field(..., example="32ed23f32f2311")
    user_id: str = Field(..., example="32ed23f32f2311")


class SimpleResponse(BaseModel):
    status: str = Field(..., example="ok")
