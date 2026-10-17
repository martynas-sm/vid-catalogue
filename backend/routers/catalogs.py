from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from database import get_db
from models import Annotation, Catalog, Video

router = APIRouter()


@router.get("/catalogs")
async def get_catalogs(
    limit: int = 10,
    offset: int = 0,
    name: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Catalog)
    if name:
        query = query.filter(Catalog.name.contains(name))
    total = query.count()
    catalogs = query.offset(offset).limit(limit).all()

    return {
        "catalogs": [
            {
                **c.to_dict(),
                "links": {
                    "self": f"/catalogs/{c.id}",
                    "videos": f"/catalogs/{c.id}/videos",
                    "dashboard": f"/catalogs/{c.id}/dashboard",
                },
            }
            for c in catalogs
        ],
        "pagination": {"limit": limit, "offset": offset, "total": total},
    }


@router.post("/catalogs", status_code=status.HTTP_201_CREATED)
async def create_catalog(payload: dict = {}, db: Session = Depends(get_db)):
    catalog = Catalog(
        user_id=payload.get("user_id"),
        name=payload.get("name", "New Catalog"),
        description=payload.get("description"),
        is_public=bool(payload.get("is_public", True)),
    )
    db.add(catalog)
    db.commit()
    db.refresh(catalog)

    result = catalog.to_dict()
    result["links"] = {
        "self": f"/catalogs/{catalog.id}",
        "videos": f"/catalogs/{catalog.id}/videos",
        "dashboard": f"/catalogs/{catalog.id}/dashboard",
    }
    return {"catalog": result}


@router.get("/catalogs/{catalog_id}")
async def get_catalog(catalog_id: int, db: Session = Depends(get_db)):
    catalog = db.get(Catalog, catalog_id)
    if catalog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Catalog with id {catalog_id} not found",
        )

    result = catalog.to_dict()
    result["links"] = {
        "self": f"/catalogs/{catalog.id}",
        "videos": f"/catalogs/{catalog.id}/videos",
        "dashboard": f"/catalogs/{catalog.id}/dashboard",
    }
    return {"catalog": result}


@router.put("/catalogs/{catalog_id}")
async def update_catalog(
    catalog_id: int, payload: dict = {}, db: Session = Depends(get_db)
):
    catalog = db.get(Catalog, catalog_id)
    if catalog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Catalog with id {catalog_id} not found",
        )

    if "name" in payload:
        catalog.name = payload["name"]
    if "description" in payload:
        catalog.description = payload["description"]
    if "is_public" in payload:
        catalog.is_public = bool(payload["is_public"])
    if "user_id" in payload:
        catalog.user_id = payload["user_id"]

    db.commit()
    db.refresh(catalog)

    result = catalog.to_dict()
    result["links"] = {
        "self": f"/catalogs/{catalog.id}",
        "videos": f"/catalogs/{catalog.id}/videos",
    }
    return {"catalog": result}


@router.delete("/catalogs/{catalog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_catalog(catalog_id: int, db: Session = Depends(get_db)):
    catalog = db.get(Catalog, catalog_id)
    if catalog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Catalog with id {catalog_id} not found",
        )
    db.delete(catalog)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/catalogs/{catalog_id}/dashboard")
async def get_catalog_dashboard(catalog_id: int, db: Session = Depends(get_db)):
    catalog = db.get(Catalog, catalog_id)
    if catalog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Catalog with id {catalog_id} not found",
        )

    videos = db.query(Video).filter(Video.catalog_id == catalog_id).all()
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
            "links": {"self": f"/catalogs/{catalog_id}"},
        },
        "stats": {
            "total_videos": len(videos),
            "total_annotations": total_annotations,
        },
        "recent_videos": recent_videos,
    }
