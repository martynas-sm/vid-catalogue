from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from database import get_db
from models import Annotation, Catalog, Video
from schemas.annotation import (
    AnnotationCreate,
    AnnotationListResponse,
    AnnotationResponse,
    AnnotationUpdate,
)

router = APIRouter()


def catalog_and_video_guard(catalog_id: int, video_id: int, db: Session):
    catalog = db.get(Catalog, catalog_id)
    if catalog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Catalog with id {catalog_id} not found",
        )

    video = db.get(Video, video_id)
    if video is None or video.catalog_id != catalog_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Video with id {video_id} not found in catalog {catalog_id}",
        )
    return catalog, video


def make_annotation_links(
    catalog_id: int, video_id: int, annotation_id: int
) -> dict[str, str]:
    return {
        "self": f"/catalogs/{catalog_id}/videos/{video_id}/annotations/{annotation_id}",
        "video": f"/catalogs/{catalog_id}/videos/{video_id}",
        "catalog": f"/catalogs/{catalog_id}",
    }


@router.get(
    "/catalogs/{catalog_id}/videos/{video_id}/annotations",
    response_model=AnnotationListResponse,
    summary="List annotations for a video with pagination and filtering",
    responses={404: {"description": "Catalog or video not found"}},
)
def get_annotations(
    catalog_id: int,
    video_id: int,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    text: str | None = None,
    db: Session = Depends(get_db),
):
    catalog_and_video_guard(catalog_id, video_id, db)

    query = db.query(Annotation).filter(Annotation.video_id == video_id)
    if text:
        query = query.filter(Annotation.text.contains(text))

    total = query.count()
    annotations = query.offset(offset).limit(limit).all()

    self_url = f"/catalogs/{catalog_id}/videos/{video_id}/annotations?limit={limit}&offset={offset}"
    if text:
        self_url += f"&text={text}"

    return {
        "annotations": [
            {
                **a.to_dict(),
                "links": make_annotation_links(catalog_id, video_id, a.id),
            }
            for a in annotations
        ],
        "pagination": {"limit": limit, "offset": offset, "total": total},
        "links": {
            "self": self_url,
            "video": f"/catalogs/{catalog_id}/videos/{video_id}",
            "catalog": f"/catalogs/{catalog_id}",
        },
    }


@router.post(
    "/catalogs/{catalog_id}/videos/{video_id}/annotations",
    response_model=AnnotationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new annotation for a video",
    responses={
        201: {
            "description": "Annotation created successfully",
            "headers": {
                "Location": {
                    "description": "URI of the created annotation resource",
                    "schema": {"type": "string"},
                }
            },
        },
        404: {"description": "Catalog or video not found"},
    },
)
def create_annotation(
    catalog_id: int,
    video_id: int,
    payload: AnnotationCreate,
    response: Response,
    db: Session = Depends(get_db),
):
    catalog_and_video_guard(catalog_id, video_id, db)

    annotation = Annotation(
        video_id=video_id,
        **payload.model_dump(),
    )
    db.add(annotation)
    db.commit()
    db.refresh(annotation)

    location = f"/catalogs/{catalog_id}/videos/{video_id}/annotations/{annotation.id}"
    response.headers["Location"] = location

    return {
        **annotation.to_dict(),
        "links": make_annotation_links(catalog_id, video_id, annotation.id),
    }


@router.get(
    "/catalogs/{catalog_id}/videos/{video_id}/annotations/{annotation_id}",
    response_model=AnnotationResponse,
    summary="Get an annotation by ID",
    responses={404: {"description": "Annotation not found in scoped video"}},
)
def get_annotation(
    catalog_id: int,
    video_id: int,
    annotation_id: int,
    db: Session = Depends(get_db),
):
    catalog_and_video_guard(catalog_id, video_id, db)

    annotation = db.get(Annotation, annotation_id)
    if annotation is None or annotation.video_id != video_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Annotation with id {annotation_id} not found for video {video_id}",
        )

    return {
        **annotation.to_dict(),
        "links": make_annotation_links(catalog_id, video_id, annotation.id),
    }


@router.put(
    "/catalogs/{catalog_id}/videos/{video_id}/annotations/{annotation_id}",
    response_model=AnnotationResponse,
    summary="Replace an annotation by ID",
    responses={404: {"description": "Annotation not found in scoped video"}},
)
def update_annotation(
    catalog_id: int,
    video_id: int,
    annotation_id: int,
    payload: AnnotationUpdate,
    db: Session = Depends(get_db),
):
    catalog_and_video_guard(catalog_id, video_id, db)

    annotation = db.get(Annotation, annotation_id)
    if annotation is None or annotation.video_id != video_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Annotation with id {annotation_id} not found for video {video_id}",
        )

    annotation.text = payload.text
    annotation.from_dur = payload.from_dur
    annotation.to_dur = payload.to_dur

    db.commit()
    db.refresh(annotation)

    return {
        **annotation.to_dict(),
        "links": make_annotation_links(catalog_id, video_id, annotation.id),
    }


@router.delete(
    "/catalogs/{catalog_id}/videos/{video_id}/annotations/{annotation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an annotation by ID",
    responses={404: {"description": "Annotation not found in scoped video"}},
)
def delete_annotation(
    catalog_id: int,
    video_id: int,
    annotation_id: int,
    db: Session = Depends(get_db),
):
    catalog_and_video_guard(catalog_id, video_id, db)

    annotation = db.get(Annotation, annotation_id)
    if annotation is None or annotation.video_id != video_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Annotation with id {annotation_id} not found for video {video_id}",
        )

    db.delete(annotation)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
