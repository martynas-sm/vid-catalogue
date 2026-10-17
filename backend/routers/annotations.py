from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from database import get_db
from models import Annotation, Catalog, Video

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


@router.get("/catalogs/{catalog_id}/videos/{video_id}/annotations")
async def get_annotations(
    catalog_id: int,
    video_id: int,
    limit: int = 10,
    offset: int = 0,
    text: str | None = None,
    db: Session = Depends(get_db),
):
    catalog_and_video_guard(catalog_id, video_id, db)

    query = db.query(Annotation).filter(Annotation.video_id == video_id)
    if text:
        query = query.filter(Annotation.text.contains(text))

    total = query.count()
    annotations = query.offset(offset).limit(limit).all()

    return {
        "annotations": [a.to_dict() for a in annotations],
        "pagination": {"limit": limit, "offset": offset, "total": total},
        "links": {
            "self": f"/catalogs/{catalog_id}/videos/{video_id}/annotations?limit={limit}&offset={offset}&text={text or ''}",
            "video": f"/catalogs/{catalog_id}/videos/{video_id}",
            "catalog": f"/catalogs/{catalog_id}",
        },
    }


@router.post(
    "/catalogs/{catalog_id}/videos/{video_id}/annotations",
    status_code=status.HTTP_201_CREATED,
)
async def create_annotation(
    catalog_id: int,
    video_id: int,
    payload: dict = {},
    db: Session = Depends(get_db),
):
    catalog_and_video_guard(catalog_id, video_id, db)

    annotation = Annotation(
        video_id=video_id,
        text=payload.get("text", "New Annotation"),
        from_dur=float(payload.get("from_dur") or 0.0),
        to_dur=float(payload.get("to_dur") or 10.0),
    )
    db.add(annotation)
    db.commit()
    db.refresh(annotation)

    result = annotation.to_dict()
    result["links"] = {
        "self": f"/catalogs/{catalog_id}/videos/{video_id}/annotations/{annotation.id}",
        "video": f"/catalogs/{catalog_id}/videos/{video_id}",
        "catalog": f"/catalogs/{catalog_id}",
    }
    return {"annotation": result}


@router.get("/catalogs/{catalog_id}/videos/{video_id}/annotations/{annotation_id}")
async def get_annotation(
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

    result = annotation.to_dict()
    result["links"] = {
        "self": f"/catalogs/{catalog_id}/videos/{video_id}/annotations/{annotation_id}",
        "video": f"/catalogs/{catalog_id}/videos/{video_id}",
        "catalog": f"/catalogs/{catalog_id}",
    }
    return {"annotation": result}


@router.put("/catalogs/{catalog_id}/videos/{video_id}/annotations/{annotation_id}")
async def update_annotation(
    catalog_id: int,
    video_id: int,
    annotation_id: int,
    payload: dict = {},
    db: Session = Depends(get_db),
):
    catalog_and_video_guard(catalog_id, video_id, db)

    annotation = db.get(Annotation, annotation_id)
    if annotation is None or annotation.video_id != video_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Annotation with id {annotation_id} not found for video {video_id}",
        )

    if "text" in payload:
        annotation.text = payload["text"]
    if "from_dur" in payload and payload["from_dur"] is not None:
        annotation.from_dur = float(payload["from_dur"])
    if "to_dur" in payload and payload["to_dur"] is not None:
        annotation.to_dur = float(payload["to_dur"])

    db.commit()
    db.refresh(annotation)

    result = annotation.to_dict()
    result["links"] = {
        "self": f"/catalogs/{catalog_id}/videos/{video_id}/annotations/{annotation_id}",
        "video": f"/catalogs/{catalog_id}/videos/{video_id}",
        "catalog": f"/catalogs/{catalog_id}",
    }
    return {"annotation": result}


@router.delete(
    "/catalogs/{catalog_id}/videos/{video_id}/annotations/{annotation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_annotation(
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
