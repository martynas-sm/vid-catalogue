from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from schemas.common import PaginationMeta


class CatalogBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Catalog name",
        examples=["Linear Algebra"],
    )
    description: str | None = Field(
        default=None,
        description="Catalog description",
        examples=["Essence of linear algebra and matrices."],
    )
    is_public: bool = Field(
        default=True,
        description="Whether the catalog is public",
        examples=[True],
    )


class CatalogCreate(CatalogBase):
    user_id: int | None = Field(
        default=None,
        description="Owner user ID (optional)",
        examples=[1],
    )


class CatalogUpdate(CatalogBase):
    user_id: int | None = Field(
        default=None,
        description="Owner user ID (optional)",
        examples=[1],
    )


class CatalogResponse(CatalogBase):
    id: int = Field(..., examples=[1])
    user_id: int | None = Field(default=None, examples=[1])
    created_at: datetime
    updated_at: datetime
    links: dict[str, str] = Field(
        default_factory=dict,
        description="HATEOAS hypermedia links",
        examples=[
            {
                "self": "/catalogs/1",
                "videos": "/catalogs/1/videos",
                "dashboard": "/catalogs/1/dashboard",
            }
        ],
    )

    model_config = ConfigDict(from_attributes=True)


class CatalogListResponse(BaseModel):
    catalogs: list[CatalogResponse]
    pagination: PaginationMeta
    links: dict[str, str] = Field(
        default_factory=dict,
        description="HATEOAS pagination links",
        examples=[
            {
                "self": "/catalogs?limit=10&offset=0",
                "next": "/catalogs?limit=10&offset=10",
            }
        ],
    )


class CatalogDashboardStats(BaseModel):
    total_videos: int = Field(..., examples=[3])
    total_annotations: int = Field(..., examples=[12])


class CatalogDashboardVideoItem(BaseModel):
    id: int = Field(..., examples=[1])
    title: str = Field(..., examples=["The determinant"])
    duration: float = Field(..., examples=[620.0])
    annotation_count: int = Field(..., examples=[4])
    links: dict[str, str] = Field(
        default_factory=dict,
        examples=[{"self": "/catalogs/1/videos/1"}],
    )


class CatalogDashboardResponse(BaseModel):
    catalog: CatalogResponse
    stats: CatalogDashboardStats
    recent_videos: list[CatalogDashboardVideoItem]
    links: dict[str, str] = Field(
        default_factory=dict,
        examples=[
            {
                "self": "/catalogs/1/dashboard",
                "catalog": "/catalogs/1",
            }
        ],
    )
