from enum import Enum

class DownloadStatus(str, Enum):
    PENDING = "pending"
    DOWNLOADING = "downloading"
    PAUSED = "paused"
    COMPLETED = "completed"
    STOPPED = "stopped"
    ERROR = "error"


class DownloadTask:
    def __init__(self, task_id: str, url: str, filename: str):
        self.task_id = task_id
        self.url = url
        self.filename = filename
        self.status = DownloadStatus.PENDING
        self.progress = 0
        self.total_size = 0
