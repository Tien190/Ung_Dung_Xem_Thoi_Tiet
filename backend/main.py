from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.src.api.download_api import router as download_router

app = FastAPI(title="Multi File Download Manager")

# Thêm phần này để bật CORS cho frontend truy cập
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Để an toàn hơn, thay "*" bằng ["http://localhost:5500"] hoặc domain web-ui của bạn
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(download_router, prefix="/api")