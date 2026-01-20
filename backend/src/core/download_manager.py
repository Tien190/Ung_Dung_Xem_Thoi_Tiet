import os
import threading
import uuid
from backend.src.models.download_task import DownloadTask, DownloadStatus
from backend.src.services.download_service import download_file
from backend.config import DOWNLOAD_FOLDER

class DownloadManager:
    def __init__(self):
        self.tasks = {}
        os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

    def create_task(self, url: str):
        task_id = str(uuid.uuid4())
        filename = url.split("/")[-1]
        task = DownloadTask(task_id, url, filename)
        self.tasks[task_id] = task

        thread = threading.Thread(
            target=download_file,
            args=(task, DOWNLOAD_FOLDER),
            daemon=True
        )
        thread.start()

        return task

    def pause(self, task_id):
        self.tasks[task_id].status = DownloadStatus.PAUSED

    def resume(self, task_id):
        self.tasks[task_id].status = DownloadStatus.DOWNLOADING

    def stop(self, task_id):
        self.tasks[task_id].status = DownloadStatus.STOPPED

    def get_all(self):
        return self.tasks


download_manager = DownloadManager()
