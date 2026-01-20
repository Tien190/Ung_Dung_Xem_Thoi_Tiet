from fastapi import FastAPI
from backend.src.api.download_api import router as download_router

app = FastAPI(title="Multi File Download Manager")

app.include_router(download_router, prefix="/api")
