from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from database import get_db
from models import Catalog, Video
from schemas.video import (
    VideoCreate,
    VideoListResponse,
    VideoResponse,
    VideoUpdate,
)

router = APIRouter()


def catalog_guard(catalog_id: int, db: Session):
    catalog = db.get(Catalog, catalog_id)
    if catalog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Catalog with id {catalog_id} not found",
        )
    return catalog


def make_video_links(catalog_id: int, video_id: int) -> dict[str, str]:
    return {
        "self": f"/catalogs/{catalog_id}/videos/{video_id}",
        "catalog": f"/catalogs/{catalog_id}",
        "annotations": f"/catalogs/{catalog_id}/videos/{video_id}/annotations",
    }


@router.get(
    "/catalogs/{catalog_id}/videos",
    response_model=VideoListResponse,
    summary="List videos in a catalog with pagination and filtering",
    responses={404: {"description": "Catalog not found"}},
)
def get_videos(
    catalog_id: int,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    title: str | None = None,
    db: Session = Depends(get_db),
):
    catalog_guard(catalog_id, db)

    query = db.query(Video).filter(Video.catalog_id == catalog_id)
    if title:
        query = query.filter(Video.title.contains(title))
    total = query.count()
    videos = query.offset(offset).limit(limit).all()

    self_url = f"/catalogs/{catalog_id}/videos?limit={limit}&offset={offset}"
    if title:
        self_url += f"&title={title}"

    return {
        "videos": [
            {
                **v.to_dict(),
                "links": make_video_links(catalog_id, v.id),
            }
            for v in videos
        ],
        "pagination": {"limit": limit, "offset": offset, "total": total},
        "links": {
            "self": self_url,
            "catalog": f"/catalogs/{catalog_id}",
        },
    }


@router.post(
    "/catalogs/{catalog_id}/videos",
    response_model=VideoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new video in a catalog",
    responses={
        201: {
            "description": "Video created successfully",
            "headers": {
                "Location": {
                    "description": "URI of the created video resource",
                    "schema": {"type": "string"},
                }
            },
        },
        404: {"description": "Catalog not found"},
    },
)
def create_video(
    catalog_id: int,
    payload: VideoCreate,
    response: Response,
    db: Session = Depends(get_db),
):
    catalog_guard(catalog_id, db)

    video = Video(
        catalog_id=catalog_id,
        **payload.model_dump(),
    )
    db.add(video)
    db.commit()
    db.refresh(video)

    location = f"/catalogs/{catalog_id}/videos/{video.id}"
    response.headers["Location"] = location

    return {
        **video.to_dict(),
        "links": make_video_links(catalog_id, video.id),
    }


@router.get(
    "/catalogs/{catalog_id}/videos/{video_id}",
    response_model=VideoResponse,
    summary="Get a video by ID within a catalog",
    responses={404: {"description": "Catalog or video not found"}},
)
def get_video(catalog_id: int, video_id: int, db: Session = Depends(get_db)):
    catalog_guard(catalog_id, db)

    video = db.get(Video, video_id)
    if video is None or video.catalog_id != catalog_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Video with id {video_id} not found in catalog {catalog_id}",
        )

    return {
        **video.to_dict(),
        "links": make_video_links(catalog_id, video.id),
    }


@router.put(
    "/catalogs/{catalog_id}/videos/{video_id}",
    response_model=VideoResponse,
    summary="Replace a video by ID within a catalog",
    responses={404: {"description": "Catalog or video not found"}},
)
def update_video(
    catalog_id: int,
    video_id: int,
    payload: VideoUpdate,
    db: Session = Depends(get_db),
):
    catalog_guard(catalog_id, db)

    video = db.get(Video, video_id)
    if video is None or video.catalog_id != catalog_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Video with id {video_id} not found in catalog {catalog_id}",
        )

    video.title = payload.title
    video.url = payload.url
    video.duration = payload.duration
    video.transcript = payload.transcript

    db.commit()
    db.refresh(video)

    return {
        **video.to_dict(),
        "links": make_video_links(catalog_id, video.id),
    }


@router.delete(
    "/catalogs/{catalog_id}/videos/{video_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a video by ID within a catalog",
    responses={404: {"description": "Catalog or video not found"}},
)
def delete_video(catalog_id: int, video_id: int, db: Session = Depends(get_db)):
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
