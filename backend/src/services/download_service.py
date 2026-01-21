import requests
import os
import time
from backend.src.models.download_task import DownloadStatus
from backend.config import CHUNK_SIZE

def download_file(task, folder):
    task.status = DownloadStatus.DOWNLOADING
    filepath = os.path.join(folder, task.filename)
    headers = { # Dùng user-agent của trình duyệt phổ biến
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/120.0.0.0 Safari/537.36"),
    "Referer": "https://pixabay.com/",
}
    try:
        with requests.get(task.url, headers=headers, stream=True) as r:
            r.raise_for_status()
            task.total_size = int(r.headers.get("Content-Length", 0))
            downloaded = 0

            with open(filepath, "wb") as f:
                for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
                    if task.status == DownloadStatus.PAUSED:
                        time.sleep(0.5)
                        continue

                    if task.status == DownloadStatus.STOPPED:
                        return

                    f.write(chunk)
                    downloaded += len(chunk)
                    task.progress = int(downloaded / task.total_size * 100)

        task.status = DownloadStatus.COMPLETED

    except Exception as e:
        print(">>> DOWNLOAD ERROR for task", task.filename, ":", e)
        import traceback
        traceback.print_exc()
        task.status = DownloadStatus.ERROR