from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from enum import Enum


class ProjectStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    owner: str = Field(..., min_length=1, max_length=255)
    status: ProjectStatus = ProjectStatus.ACTIVE


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    owner: str | None = Field(None, min_length=1, max_length=255)
    status: ProjectStatus | None = None


class ProjectResponse(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class ProjectListResponse(BaseModel):
    items: list[ProjectResponse]
    total: int
    page: int
    size: int
