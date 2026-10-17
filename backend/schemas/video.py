from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from schemas.common import PaginationMeta


class VideoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Video title")
    url: str = Field(..., min_length=1, max_length=500, description="Video URL")
    duration: float = Field(
        default=0.0, ge=0.0, description="Video duration in seconds"
    )
    transcript: str | None = Field(default=None, description="Optional text transcript")


class VideoCreate(VideoBase):
    pass


class VideoUpdate(VideoBase):
    pass


class VideoResponse(VideoBase):
    id: int
    catalog_id: int
    created_at: datetime
    updated_at: datetime
    links: dict[str, str] = Field(default_factory=dict)

    model_config = ConfigDict(from_attributes=True)


class VideoListResponse(BaseModel):
    videos: list[VideoResponse]
    pagination: PaginationMeta
    links: dict[str, str] = Field(default_factory=dict)
