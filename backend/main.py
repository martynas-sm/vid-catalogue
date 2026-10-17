from fastapi import FastAPI

from database import engine
from models import Base
from routers import annotations, catalogs, users, videos

Base.metadata.create_all(bind=engine)
app = FastAPI()

# Router structure from: https://fastapi.tiangolo.com/tutorial/bigger-applications/
app.include_router(catalogs.router)
app.include_router(videos.router)
app.include_router(annotations.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
