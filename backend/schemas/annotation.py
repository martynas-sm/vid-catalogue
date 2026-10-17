from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from schemas.common import PaginationMeta


class AnnotationBase(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000, description="Annotation note")
    from_dur: float = Field(..., ge=0.0, description="Start timestamp in seconds")
    to_dur: float = Field(..., ge=0.0, description="End timestamp in seconds")

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
    id: int
    video_id: int
    created_at: datetime
    updated_at: datetime
    links: dict[str, str] = Field(
        default_factory=dict, description="HATEOAS hypermedia links"
    )

    model_config = ConfigDict(from_attributes=True)


class AnnotationListResponse(BaseModel):
    annotations: list[AnnotationResponse]
    pagination: PaginationMeta
    links: dict[str, str] = Field(default_factory=dict)
