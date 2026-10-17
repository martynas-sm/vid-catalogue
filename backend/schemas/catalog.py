from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from schemas.common import PaginationMeta


class CatalogBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Catalog name")
    description: str | None = Field(default=None, description="Catalog description")
    is_public: bool = Field(default=True, description="Whether the catalog is public")


class CatalogCreate(CatalogBase):
    user_id: int | None = Field(default=None, description="Owner user ID (optional)")


class CatalogUpdate(CatalogBase):
    user_id: int | None = Field(default=None, description="Owner user ID (optional)")


class CatalogResponse(CatalogBase):
    id: int
    user_id: int | None = None
    created_at: datetime
    updated_at: datetime
    links: dict[str, str] = Field(default_factory=dict)

    model_config = ConfigDict(from_attributes=True)


class CatalogListResponse(BaseModel):
    catalogs: list[CatalogResponse]
    pagination: PaginationMeta
    links: dict[str, str] = Field(default_factory=dict)


class CatalogDashboardStats(BaseModel):
    total_videos: int
    total_annotations: int


class CatalogDashboardVideoItem(BaseModel):
    id: int
    title: str
    duration: float
    annotation_count: int
    links: dict[str, str] = Field(default_factory=dict)


class CatalogDashboardResponse(BaseModel):
    catalog: CatalogResponse
    stats: CatalogDashboardStats
    recent_videos: list[CatalogDashboardVideoItem]
    links: dict[str, str] = Field(default_factory=dict)
