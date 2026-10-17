from fastapi import APIRouter, Response, status

router = APIRouter()


@router.get("/catalogues/{catalogue_id}/videos")
async def get_videos(
    catalogue_id: int, limit: int = 10, offset: int = 0, title: str | None = None
):
    videos = [
        {
            "id": 1,
            "catalogue_id": catalogue_id,
            "title": "Video 1",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "duration": 212,
            "links": {
                "self": f"/catalogues/{catalogue_id}/videos/1",
                "catalogue": f"/catalogues/{catalogue_id}",
                "annotations": f"/catalogues/{catalogue_id}/videos/1/annotations",
            },
        },
        {
            "id": 2,
            "catalogue_id": catalogue_id,
            "title": "Video 2",
            "url": "https://www.youtube.com/watch?v=3JZ_D3ELwOQ",
            "duration": 180,
            "links": {
                "self": f"/catalogues/{catalogue_id}/videos/2",
                "catalogue": f"/catalogues/{catalogue_id}",
                "annotations": f"/catalogues/{catalogue_id}/videos/2/annotations",
            },
        },
    ]
    return {
        "videos": videos,
        "pagination": {"limit": limit, "offset": offset, "total": len(videos)},
    }


@router.post("/catalogues/{catalogue_id}/videos", status_code=status.HTTP_201_CREATED)
async def create_video(catalogue_id: int, payload: dict = {}):
    created_video = {
        "id": 3,
        "catalogue_id": catalogue_id,
        "title": payload.get("title", "New Video"),
        "url": payload.get("url", "https://www.youtube.com/watch?v=example"),
        "duration": payload.get("duration", 120),
        "links": {
            "self": f"/catalogues/{catalogue_id}/videos/3",
            "catalogue": f"/catalogues/{catalogue_id}",
            "annotations": f"/catalogues/{catalogue_id}/videos/3/annotations",
        },
    }
    return {"video": created_video}


@router.get("/catalogues/{catalogue_id}/videos/{video_id}")
async def get_video(catalogue_id: int, video_id: int):
    video = {
        "id": video_id,
        "catalogue_id": catalogue_id,
        "title": f"Video {video_id}",
        "url": f"https://www.youtube.com/watch?v=video{video_id}",
        "duration": 300,
        "links": {
            "self": f"/catalogues/{catalogue_id}/videos/{video_id}",
            "catalogue": f"/catalogues/{catalogue_id}",
            "annotations": f"/catalogues/{catalogue_id}/videos/{video_id}/annotations",
        },
    }
    return {"video": video}


@router.put("/catalogues/{catalogue_id}/videos/{video_id}")
async def update_video(catalogue_id: int, video_id: int, payload: dict = {}):
    updated_video = {
        "id": video_id,
        "catalogue_id": catalogue_id,
        "title": payload.get("title", f"Updated Video {video_id}"),
        "url": payload.get("url", f"https://www.youtube.com/watch?v=video{video_id}"),
        "duration": payload.get("duration", 300),
        "links": {
            "self": f"/catalogues/{catalogue_id}/videos/{video_id}",
            "catalogue": f"/catalogues/{catalogue_id}",
            "annotations": f"/catalogues/{catalogue_id}/videos/{video_id}/annotations",
        },
    }
    return {"video": updated_video}


@router.delete(
    "/catalogues/{catalogue_id}/videos/{video_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_video(catalogue_id: int, video_id: int):
    return Response(status_code=status.HTTP_204_NO_CONTENT)