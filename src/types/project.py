from pydantic import BaseModel, Field
from datetime import datetime


# Pydanticを用いたAPIに渡されるデータの定義 ValidationやDocumentationの機能が追加される
class ProjectCreateRequest(BaseModel):
    title: str = Field(..., example="Test project")
    status: str = Field(..., example="pending")
    total_man_hour_min: int = Field(..., example=60)
    to_date: datetime = Field(..., example="2023-08-15T15:32:00Z")
    from_date: datetime = Field(..., example="2023-08-14T15:32:00Z")
    user_key: str = Field(..., example="32ed23f32f2311")


class ProjectGetResponse(BaseModel):
    id: str = Field(..., example="32ed23f32f2311")
    title: str = Field(..., example="Test project")
    status: str = Field(..., example="pending")
    total_man_hour_min: int = Field(..., example=60)
    to_date: datetime = Field(..., example="2023-08-15T15:32:00Z")
    from_date: datetime = Field(..., example="2023-08-14T15:32:00Z")
    user_key: str = Field(..., example="32ed23f32f2311")
    created_at: datetime = Field(..., example="2023-08-14T15:32:00Z")
    updated_at: datetime = Field(..., example="2023-08-14T15:32:00Z")


class ProjectEditRequest(BaseModel):
    title: str = Field(..., example="Test project")
    status: str = Field(..., example="pending")
    total_man_hour_min: int = Field(..., example=60)
    to_date: datetime = Field(..., example="2023-08-15T15:32:00Z")
    from_date: datetime = Field(..., example="2023-08-14T15:32:00Z")


class SimpleResponse(BaseModel):
    status: str = Field(..., example="ok")
