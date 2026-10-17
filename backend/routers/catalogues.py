from fastapi import APIRouter

router = APIRouter()

@router.get("/catalogues")
async def get_catalogues():
    catalogues = [
        {"id": 1, "name": "Catalogue 1"},
        {"id": 2, "name": "Catalogue 2"},
    ]
    return {"catalogues": catalogues}

@router.get("/catalogues/{catalogue_id}")
async def get_catalogue(catalogue_id: int):
    catalogue = {"id": catalogue_id, "name": f"Catalogue {catalogue_id}"}
    return {"catalogue": catalogue}