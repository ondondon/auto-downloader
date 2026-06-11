"""
Download Queue Manager
Manages concurrent downloads with threading
"""
import threading
import queue
import time
from typing import List, Dict, Callable
from .gallery_dl_wrapper import download

class DownloadTask:
    def __init__(self, url: str, platform: str = "auto", output_dir: str = None):
        self.url = url
        self.platform = platform
        self.output_dir = output_dir or "/storage/emulated/0/Download/AutoDownloader"
        self.status = "pending"  # pending | running | done | failed
        self.result = None

class DownloadManager:
    def __init__(self, max_concurrent: int = 2):
        self.max_concurrent = max_concurrent
        self.task_queue: List[DownloadTask] = []
        self.active_workers = 0
        self._lock = threading.Lock()
        self._callbacks: List[Callable] = []

    def add_task(self, url: str, platform: str = "auto", output_dir: str = None) -> DownloadTask:
        task = DownloadTask(url, platform, output_dir)
        self.task_queue.append(task)
        self._ensure_worker()
        return task

    def _ensure_worker(self):
        with self._lock:
            if self.active_workers < self.max_concurrent:
                self.active_workers += 1
                threading.Thread(target=self._worker, daemon=True).start()

    def _worker(self):
        while True:
            task = None
            with self._lock:
                for t in self.task_queue:
                    if t.status == "pending":
                        task = t
                        break
                if not task:
                    self.active_workers -= 1
                    break

            if task:
                task.status = "running"
                task.result = download(task.url, task.platform, task.output_dir)
                task.status = "done" if task.result["success"] else "failed"
                self._notify()

    def _notify(self):
        for cb in self._callbacks:
            try:
                cb()
            except:
                pass

    def on_update(self, callback: Callable):
        self._callbacks.append(callback)

    def get_status(self) -> Dict:
        pending = sum(1 for t in self.task_queue if t.status == "pending")
        running = sum(1 for t in self.task_queue if t.status == "running")
        done = sum(1 for t in self.task_queue if t.status == "done")
        failed = sum(1 for t in self.task_queue if t.status == "failed")
        return {
            "pending": pending,
            "running": running,
            "done": done,
            "failed": failed,
            "total": len(self.task_queue),
        }
