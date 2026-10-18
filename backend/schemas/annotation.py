from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from schemas.common import PaginationMeta


class AnnotationBase(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Annotation note",
        examples=["Understanding determinants as scaling factors"],
    )
    from_dur: float = Field(
        ...,
        ge=0.0,
        description="Start timestamp in seconds",
        examples=[0.0],
    )
    to_dur: float = Field(
        ...,
        ge=0.0,
        description="End timestamp in seconds",
        examples=[159.0],
    )

    @model_validator(mode="after")
    def check_interval(self):
        if self.from_dur > self.to_dur:
            raise ValueError("from_dur cannot be greater than to_dur")
        return self


class AnnotationCreate(AnnotationBase):
    pass


class AnnotationUpdate(AnnotationBase):
    pass


class AnnotationResponse(AnnotationBase):
    id: int = Field(..., examples=[1])
    video_id: int = Field(..., examples=[1])
    created_at: datetime
    updated_at: datetime
    links: dict[str, str] = Field(
        default_factory=dict,
        description="HATEOAS hypermedia links",
        examples=[
            {
                "self": "/catalogs/1/videos/1/annotations/1",
                "video": "/catalogs/1/videos/1",
                "catalog": "/catalogs/1",
            }
        ],
    )

    model_config = ConfigDict(from_attributes=True)


class AnnotationListResponse(BaseModel):
    annotations: list[AnnotationResponse]
    pagination: PaginationMeta
    links: dict[str, str] = Field(
        default_factory=dict,
        description="HATEOAS pagination links",
        examples=[
            {
                "self": "/catalogs/1/videos/1/annotations?limit=10&offset=0",
                "video": "/catalogs/1/videos/1",
                "catalog": "/catalogs/1",
            }
        ],
    )
