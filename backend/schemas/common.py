from pydantic import BaseModel, Field


class PaginationMeta(BaseModel):
    limit: int = Field(..., ge=1, description="Number of items returned")
    offset: int = Field(..., ge=0, description="Number of items skipped")
    total: int = Field(..., ge=0, description="Total number of items")
