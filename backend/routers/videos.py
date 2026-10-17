from fastapi import APIRouter

router = APIRouter()

@router.get("/catalogues/{catalogue_id}/videos")
async def get_videos(catalogue_id: int):
    videos = [
        {"id": 1, "title": "Video 1", "url": "http://example.com/video1"},
        {"id": 2, "title": "Video 2", "url": "http://example.com/video2"},
    ]
    return {"videos": videos}

@router.get("/catalogues/{catalogue_id}/videos/{video_id}")
async def get_video(catalogue_id: int, video_id: int):
    video = {"id": video_id, "title": f"Video {video_id}", "url": f"http://example.com/video{video_id}"}
    return {"video": video}