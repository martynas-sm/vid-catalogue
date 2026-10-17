from fastapi import APIRouter

router = APIRouter()


@router.get("/catalogues/{catalogue_id}/videos/{video_id}/annotations")
async def get_annotations(catalogue_id: int, video_id: int):
    annotations = [
        {"id": 1, "text": "Annotation 1", "timestamp": "00:01:00"},
        {"id": 2, "text": "Annotation 2", "timestamp": "00:02:00"},
    ]
    return {"annotations": annotations}

@router.get("/catalogues/{catalogue_id}/videos/{video_id}/annotations/{annotation_id}")
async def get_annotation(catalogue_id: int, video_id: int, annotation_id: int):
    annotation = {"id": annotation_id, "text": f"Annotation {annotation_id}", "timestamp": "00:01:00"}
    return {"annotation": annotation}