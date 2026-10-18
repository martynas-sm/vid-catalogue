from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from database import engine
from models import Base
from routers import annotations, catalogs, users, videos

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Video Catalogs API",
    version="1.0.0",
    description="REST API for Video Catalogs application (KTU Saityno taikomųjų programų projektavimas).",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(IntegrityError)
def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "Database integrity conflict occurred."},
    )


# Router structure from: https://fastapi.tiangolo.com/tutorial/bigger-applications/
app.include_router(catalogs.router, tags=["Catalogs"])
app.include_router(videos.router, tags=["Videos"])
app.include_router(annotations.router, tags=["Annotations"])
app.include_router(users.router, tags=["Users"])


@app.get("/", tags=["System"], summary="Root status check")
async def root():
    return {"message": "Hello World"}


@app.get("/health", tags=["System"], summary="Health check probe")
async def health():
    return {"status": "healthy"}
