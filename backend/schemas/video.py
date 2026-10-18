from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from schemas.common import PaginationMeta


class VideoBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Video title",
        examples=["The determinant | Chapter 6, Essence of linear algebra"],
    )
    url: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Video URL",
        examples=["https://youtu.be/Ip3X9LOh2dk"],
    )
    duration: float = Field(
        default=0.0,
        ge=0.0,
        description="Video duration in seconds",
        examples=[620.0],
    )
    description: str | None = Field(
        default=None,
        description="Optional video description",
        examples=[
            "The determinant measures how much areas and volumes scale during a transformation."
        ],
    )


class VideoCreate(VideoBase):
    pass


class VideoUpdate(VideoBase):
    pass


class VideoResponse(VideoBase):
    id: int = Field(..., examples=[1])
    catalog_id: int = Field(..., examples=[1])
    created_at: datetime
    updated_at: datetime
    links: dict[str, str] = Field(
        default_factory=dict,
        description="HATEOAS hypermedia links",
        examples=[
            {
                "self": "/catalogs/1/videos/1",
                "catalog": "/catalogs/1",
                "annotations": "/catalogs/1/videos/1/annotations",
            }
        ],
    )

    model_config = ConfigDict(from_attributes=True)


class VideoListResponse(BaseModel):
    videos: list[VideoResponse]
    pagination: PaginationMeta
    links: dict[str, str] = Field(
        default_factory=dict,
        description="HATEOAS pagination links",
        examples=[
            {
                "self": "/catalogs/1/videos?limit=10&offset=0",
                "catalog": "/catalogs/1",
            }
        ],
    )
