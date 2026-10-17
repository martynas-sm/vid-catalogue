from fastapi import APIRouter, Response, status

router = APIRouter()


@router.get("/catalogues/{catalogue_id}/videos/{video_id}/annotations")
async def get_annotations(
    catalogue_id: int,
    video_id: int,
    limit: int = 10,
    offset: int = 0,
    text: str | None = None,
):
    annotations = [
        {
            "id": 1,
            "catalogue_id": catalogue_id,
            "video_id": video_id,
            "text": "Annotation 1",
            "timestamp": "00:01:00",
            "links": {
                "self": f"/catalogues/{catalogue_id}/videos/{video_id}/annotations/1",
                "video": f"/catalogues/{catalogue_id}/videos/{video_id}",
                "catalogue": f"/catalogues/{catalogue_id}",
            },
        },
        {
            "id": 2,
            "catalogue_id": catalogue_id,
            "video_id": video_id,
            "text": "Annotation 2",
            "timestamp": "00:02:00",
            "links": {
                "self": f"/catalogues/{catalogue_id}/videos/{video_id}/annotations/2",
                "video": f"/catalogues/{catalogue_id}/videos/{video_id}",
                "catalogue": f"/catalogues/{catalogue_id}",
            },
        },
    ]
    return {
        "annotations": annotations,
        "pagination": {"limit": limit, "offset": offset, "total": len(annotations)},
    }


@router.post(
    "/catalogues/{catalogue_id}/videos/{video_id}/annotations",
    status_code=status.HTTP_201_CREATED,
)
async def create_annotation(catalogue_id: int, video_id: int, payload: dict = {}):
    created_annotation = {
        "id": 3,
        "catalogue_id": catalogue_id,
        "video_id": video_id,
        "text": payload.get("text", "New Annotation"),
        "timestamp": payload.get("timestamp", "00:03:00"),
        "links": {
            "self": f"/catalogues/{catalogue_id}/videos/{video_id}/annotations/3",
            "video": f"/catalogues/{catalogue_id}/videos/{video_id}",
            "catalogue": f"/catalogues/{catalogue_id}",
        },
    }
    return {"annotation": created_annotation}


@router.get(
    "/catalogues/{catalogue_id}/videos/{video_id}/annotations/{annotation_id}"
)
async def get_annotation(catalogue_id: int, video_id: int, annotation_id: int):
    annotation = {
        "id": annotation_id,
        "catalogue_id": catalogue_id,
        "video_id": video_id,
        "text": f"Annotation {annotation_id}",
        "timestamp": "00:01:00",
        "links": {
            "self": f"/catalogues/{catalogue_id}/videos/{video_id}/annotations/{annotation_id}",
            "video": f"/catalogues/{catalogue_id}/videos/{video_id}",
            "catalogue": f"/catalogues/{catalogue_id}",
        },
    }
    return {"annotation": annotation}


@router.put(
    "/catalogues/{catalogue_id}/videos/{video_id}/annotations/{annotation_id}"
)
async def update_annotation(
    catalogue_id: int, video_id: int, annotation_id: int, payload: dict = {}
):
    updated_annotation = {
        "id": annotation_id,
        "catalogue_id": catalogue_id,
        "video_id": video_id,
        "text": payload.get("text", f"Updated Annotation {annotation_id}"),
        "timestamp": payload.get("timestamp", "00:01:30"),
        "links": {
            "self": f"/catalogues/{catalogue_id}/videos/{video_id}/annotations/{annotation_id}",
            "video": f"/catalogues/{catalogue_id}/videos/{video_id}",
            "catalogue": f"/catalogues/{catalogue_id}",
        },
    }
    return {"annotation": updated_annotation}


@router.delete(
    "/catalogues/{catalogue_id}/videos/{video_id}/annotations/{annotation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_annotation(catalogue_id: int, video_id: int, annotation_id: int):
    return Response(status_code=status.HTTP_204_NO_CONTENT)