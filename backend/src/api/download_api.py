from fastapi import APIRouter, Query
from fastapi.responses import FileResponse, JSONResponse
from backend.src.core.download_manager import download_manager
from backend.src.models.download_task import DownloadStatus
from backend.config import DOWNLOAD_FOLDER
import os

router = APIRouter()

@router.post("/download")
def start_download(url: str = Query(...)):
    task = download_manager.create_task(url)
    return {"task_id": task.task_id}

@router.get("/tasks")
def get_tasks():
    data = {
        tid: {
            "task_id": t.task_id,
            "url": t.url,
            "filename": t.filename,
            "status": t.status,
            "progress": t.progress,
            "total_size": t.total_size
        } for tid, t in download_manager.get_all().items()
    }
    return data

@router.post("/pause/{task_id}")
def pause(task_id: str):
    download_manager.pause(task_id)
    return {"status": "paused"}

@router.post("/resume/{task_id}")
def resume(task_id: str):
    download_manager.resume(task_id)
    return {"status": "resumed"}

@router.post("/stop/{task_id}")
def stop(task_id: str):
    download_manager.stop(task_id)
    return {"status": "stopped"}

@router.delete("/delete/{task_id}")
def delete_task(task_id: str):
    task = download_manager.get_all().get(task_id)
    if not task:
        return JSONResponse({"error": "Không tìm thấy task!"}, status_code=404)
    # Nếu đã completed thì xóa luôn file
    if task.status == DownloadStatus.COMPLETED:
        fpath = os.path.join(DOWNLOAD_FOLDER, task.filename)
        if os.path.exists(fpath):
            try:
                os.remove(fpath)
            except Exception as e:
                return JSONResponse({"error": f"Lỗi xóa file: {e}"}, status_code=500)
    # Xóa khỏi dict quản lý task
    del download_manager.tasks[task_id]
    return {"success": True}

@router.get("/file/{task_id}")
def download_file_endpoint(task_id: str):
    task = download_manager.get_all().get(task_id)
    if not task or task.status != DownloadStatus.COMPLETED:
        return JSONResponse({"error": "File chưa tải hoàn tất!"}, status_code=404)
    full_path = os.path.join(DOWNLOAD_FOLDER, task.filename)
    if not os.path.exists(full_path):
        return JSONResponse({"error": "File không tồn tại trên server."}, status_code=404)
    return FileResponse(full_path, filename=task.filename, media_type="application/octet-stream")