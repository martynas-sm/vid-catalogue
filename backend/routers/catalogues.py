from fastapi import APIRouter, Response, status

router = APIRouter()


@router.get("/catalogues")
async def get_catalogues(limit: int = 10, offset: int = 0, name: str | None = None):
    catalogues = [
        {
            "id": 1,
            "name": "Catalogue 1",
            "links": {"self": "/catalogues/1", "videos": "/catalogues/1/videos"},
        },
        {
            "id": 2,
            "name": "Catalogue 2",
            "links": {"self": "/catalogues/2", "videos": "/catalogues/2/videos"},
        },
    ]
    return {
        "catalogues": catalogues,
        "pagination": {"limit": limit, "offset": offset, "total": len(catalogues)},
    }


@router.post("/catalogues", status_code=status.HTTP_201_CREATED)
async def create_catalogue(payload: dict = {}):
    created_catalogue = {
        "id": 3,
        "name": payload.get("name", "New Catalogue"),
        "links": {"self": "/catalogues/3", "videos": "/catalogues/3/videos"},
    }
    return {"catalogue": created_catalogue}


@router.get("/catalogues/{catalogue_id}")
async def get_catalogue(catalogue_id: int):
    catalogue = {
        "id": catalogue_id,
        "name": f"Catalogue {catalogue_id}",
        "links": {
            "self": f"/catalogues/{catalogue_id}",
            "videos": f"/catalogues/{catalogue_id}/videos",
            "dashboard": f"/catalogues/{catalogue_id}/dashboard",
        },
    }
    return {"catalogue": catalogue}


@router.put("/catalogues/{catalogue_id}")
async def update_catalogue(catalogue_id: int, payload: dict = {}):
    updated_catalogue = {
        "id": catalogue_id,
        "name": payload.get("name", f"Updated Catalogue {catalogue_id}"),
        "links": {
            "self": f"/catalogues/{catalogue_id}",
            "videos": f"/catalogues/{catalogue_id}/videos",
        },
    }
    return {"catalogue": updated_catalogue}


@router.delete("/catalogues/{catalogue_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_catalogue(catalogue_id: int):
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/catalogues/{catalogue_id}/dashboard")
async def get_catalogue_dashboard(catalogue_id: int):
    return {
        "catalogue": {
            "id": catalogue_id,
            "name": f"Catalogue {catalogue_id}",
            "links": {"self": f"/catalogues/{catalogue_id}"},
        },
        "stats": {
            "total_videos": 5,
            "total_annotations": 14,
        },
        "recent_videos": [
            {
                "id": 1,
                "title": "Introduction to FastAPI",
                "annotation_count": 3,
                "links": {"self": f"/catalogues/{catalogue_id}/videos/1"},
            }
        ],
    }