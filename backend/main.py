from fastapi import FastAPI
from routers import catalogues, videos, annotations

app = FastAPI()

# Router structure from: https://fastapi.tiangolo.com/tutorial/bigger-applications/
app.include_router(catalogues.router)
app.include_router(videos.router)
app.include_router(annotations.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

