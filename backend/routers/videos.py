from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from database import get_db
from models import Catalog, Video

router = APIRouter()


def catalog_guard(catalog_id: int, db: Session):
    catalog = db.get(Catalog, catalog_id)
    if catalog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Catalog with id {catalog_id} not found",
        )
    return catalog


@router.get("/catalogs/{catalog_id}/videos")
async def get_videos(
    catalog_id: int,
    limit: int = 10,
    offset: int = 0,
    title: str | None = None,
    db: Session = Depends(get_db),
):
    catalog_guard(catalog_id, db)

    query = db.query(Video).filter(Video.catalog_id == catalog_id)
    if title:
        query = query.filter(Video.title.contains(title))
    total = query.count()
    videos = query.offset(offset).limit(limit).all()

    return {
        "videos": [
            {
                **v.to_dict(),
                "links": {
                    "self": f"/catalogs/{catalog_id}/videos/{v.id}",
                    "catalog": f"/catalogs/{catalog_id}",
                    "annotations": f"/catalogs/{catalog_id}/videos/{v.id}/annotations",
                },
            }
            for v in videos
        ],
        "pagination": {"limit": limit, "offset": offset, "total": total},
    }


@router.post("/catalogs/{catalog_id}/videos", status_code=status.HTTP_201_CREATED)
async def create_video(
    catalog_id: int, payload: dict = {}, db: Session = Depends(get_db)
):
    catalog_guard(catalog_id, db)

    video = Video(
        catalog_id=catalog_id,
        title=payload.get("title", "New Video"),
        url=payload.get("url", "https://www.youtube.com/watch?v=example"),
        duration=float(payload.get("duration") or 0.0),
        transcript=payload.get("transcript"),
    )
    db.add(video)
    db.commit()
    db.refresh(video)

    result = video.to_dict()
    result["links"] = {
        "self": f"/catalogs/{catalog_id}/videos/{video.id}",
        "catalog": f"/catalogs/{catalog_id}",
        "annotations": f"/catalogs/{catalog_id}/videos/{video.id}/annotations",
    }
    return {"video": result}


@router.get("/catalogs/{catalog_id}/videos/{video_id}")
async def get_video(catalog_id: int, video_id: int, db: Session = Depends(get_db)):
    catalog_guard(catalog_id, db)

    video = db.get(Video, video_id)
    if video is None or video.catalog_id != catalog_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Video with id {video_id} not found in catalog {catalog_id}",
        )

    result = video.to_dict()
    result["links"] = {
        "self": f"/catalogs/{catalog_id}/videos/{video.id}",
        "catalog": f"/catalogs/{catalog_id}",
        "annotations": f"/catalogs/{catalog_id}/videos/{video.id}/annotations",
    }
    return {"video": result}


@router.put("/catalogs/{catalog_id}/videos/{video_id}")
async def update_video(
    catalog_id: int,
    video_id: int,
    payload: dict = {},
    db: Session = Depends(get_db),
):
    catalog_guard(catalog_id, db)

    video = db.get(Video, video_id)
    if video is None or video.catalog_id != catalog_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Video with id {video_id} not found in catalog {catalog_id}",
        )

    if "title" in payload:
        video.title = payload["title"]
    if "url" in payload:
        video.url = payload["url"]
    if "duration" in payload and payload["duration"] is not None:
        video.duration = float(payload["duration"])
    if "transcript" in payload:
        video.transcript = payload["transcript"]

    db.commit()
    db.refresh(video)

    result = video.to_dict()
    result["links"] = {
        "self": f"/catalogs/{catalog_id}/videos/{video.id}",
        "catalog": f"/catalogs/{catalog_id}",
        "annotations": f"/catalogs/{catalog_id}/videos/{video.id}/annotations",
    }
    return {"video": result}


@router.delete(
    "/catalogs/{catalog_id}/videos/{video_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_video(catalog_id: int, video_id: int, db: Session = Depends(get_db)):
    catalog_guard(catalog_id, db)

    video = db.get(Video, video_id)
    if video is None or video.catalog_id != catalog_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Video with id {video_id} not found in catalog {catalog_id}",
        )

    db.delete(video)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
