from fastapi import APIRouter
from backend.src.core.download_manager import download_manager

router = APIRouter()

@router.post("/download")
def start_download(url: str):
    task = download_manager.create_task(url)
    return {"task_id": task.task_id}


@router.get("/tasks")
def get_tasks():
    return download_manager.get_all()


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
