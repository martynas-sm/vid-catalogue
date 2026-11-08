from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from auth.dependencies import get_current_user, get_owned_catalog, require_role
from database import get_db
from models import Annotation, Catalog, User, Video
from schemas.catalog import (
    CatalogCreate,
    CatalogDashboardResponse,
    CatalogListResponse,
    CatalogResponse,
    CatalogUpdate,
)
from schemas.common import make_pagination_links

router = APIRouter()


def make_catalog_links(catalog_id: int) -> dict[str, str]:
    return {
        "self": f"/catalogs/{catalog_id}",
        "videos": f"/catalogs/{catalog_id}/videos",
        "dashboard": f"/catalogs/{catalog_id}/dashboard",
    }


@router.get(
    "/catalogs",
    response_model=CatalogListResponse,
    summary="List catalogs with pagination and filtering",
)
def get_catalogs(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    name: str | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Catalog)
    if name:
        query = query.filter(Catalog.name.contains(name))
    total = query.count()
    catalogs = query.offset(offset).limit(limit).all()

    links = make_pagination_links(
        base_path="/catalogs",
        limit=limit,
        offset=offset,
        total=total,
        extra_params={"name": name} if name else None,
    )

    return {
        "catalogs": [
            {
                **c.to_dict(),
                "links": make_catalog_links(c.id),
            }
            for c in catalogs
        ],
        "pagination": {"limit": limit, "offset": offset, "total": total},
        "links": links,
    }


@router.post(
    "/catalogs",
    response_model=CatalogResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new catalog",
    responses={
        201: {
            "description": "Catalog created successfully",
            "headers": {
                "Location": {
                    "description": "URI of the created catalog resource",
                    "schema": {"type": "string"},
                }
            },
        },
        403: {"description": "Forbidden: Insufficient role permissions"},
    },
)
def create_catalog(
    payload: CatalogCreate,
    response: Response,
    current_user: User = Depends(require_role("admin", "creator")),
    db: Session = Depends(get_db),
):
    catalog_data = payload.model_dump()
    catalog_data["user_id"] = current_user.id
    catalog = Catalog(**catalog_data)
    db.add(catalog)
    db.commit()
    db.refresh(catalog)

    location = f"/catalogs/{catalog.id}"
    response.headers["Location"] = location

    return {
        **catalog.to_dict(),
        "links": make_catalog_links(catalog.id),
    }


@router.get(
    "/catalogs/{catalog_id}",
    response_model=CatalogResponse,
    summary="Get a catalog by ID",
    responses={404: {"description": "Catalog not found"}},
)
def get_catalog(catalog_id: int, db: Session = Depends(get_db)):
    catalog = db.get(Catalog, catalog_id)
    if catalog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Catalog with id {catalog_id} not found",
        )

    return {
        **catalog.to_dict(),
        "links": make_catalog_links(catalog.id),
    }


@router.put(
    "/catalogs/{catalog_id}",
    response_model=CatalogResponse,
    summary="Replace a catalog by ID",
    responses={
        403: {"description": "Forbidden: You do not own this catalog"},
        404: {"description": "Catalog not found"},
    },
)
def update_catalog(
    payload: CatalogUpdate,
    catalog: Catalog = Depends(get_owned_catalog),
    db: Session = Depends(get_db),
):
    catalog.name = payload.name
    catalog.description = payload.description
    catalog.is_public = payload.is_public

    db.commit()
    db.refresh(catalog)

    return {
        **catalog.to_dict(),
        "links": make_catalog_links(catalog.id),
    }


@router.delete(
    "/catalogs/{catalog_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a catalog by ID",
    responses={
        403: {"description": "Forbidden: You do not own this catalog"},
        404: {"description": "Catalog not found"},
    },
)
def delete_catalog(
    catalog: Catalog = Depends(get_owned_catalog),
    db: Session = Depends(get_db),
):
    db.delete(catalog)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/catalogs/{catalog_id}/dashboard",
    response_model=CatalogDashboardResponse,
    summary="Get composite catalog dashboard",
    responses={404: {"description": "Catalog not found"}},
)
def get_catalog_dashboard(catalog_id: int, db: Session = Depends(get_db)):
    catalog = db.get(Catalog, catalog_id)
    if catalog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Catalog with id {catalog_id} not found",
        )

    videos = (
        db.query(Video)
        .filter(Video.catalog_id == catalog_id)
        .order_by(Video.created_at.desc())
        .all()
    )
    video_ids = [v.id for v in videos]
    total_annotations = (
        db.query(Annotation).filter(Annotation.video_id.in_(video_ids)).count()
        if video_ids
        else 0
    )

    recent_videos = [
        {
            "id": v.id,
            "title": v.title,
            "duration": v.duration,
            "annotation_count": db.query(Annotation)
            .filter(Annotation.video_id == v.id)
            .count(),
            "links": {"self": f"/catalogs/{catalog_id}/videos/{v.id}"},
        }
        for v in videos[:5]
    ]

    return {
        "catalog": {
            **catalog.to_dict(),
            "links": make_catalog_links(catalog.id),
        },
        "stats": {
            "total_videos": len(videos),
            "total_annotations": total_annotations,
        },
        "recent_videos": recent_videos,
        "links": {
            "self": f"/catalogs/{catalog_id}/dashboard",
            "catalog": f"/catalogs/{catalog_id}",
        },
    }
