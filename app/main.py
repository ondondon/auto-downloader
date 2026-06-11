"""
Auto-Downloader - Flet UI
gallery-dl Python wrapper for Android
"""
import flet as ft
import subprocess
import threading
import os
import json
from pathlib import Path

# ============================================================
# Download Manager
# ============================================================
class DownloadManager:
    def __init__(self):
        self.queue = []
        self.active = False
        self.results = []

    def add_task(self, url: str, platform: str):
        self.queue.append({"url": url, "platform": platform})
        if not self.active:
            self.process_queue()

    def process_queue(self):
        if not self.queue:
            self.active = False
            return
        self.active = True
        task = self.queue.pop(0)
        self.run_gallery_dl(task)

    def run_gallery_dl(self, task):
        cmd = [
            "gallery-dl",
            "--no-check-certificate",
            "-D", "/storage/emulated/0/Download/AutoDownloader",
            task["url"]
        ]
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            self.results.append({
                "url": task["url"],
                "success": result.returncode == 0,
                "output": result.stdout[-500:] if result.stdout else "",
                "error": result.stderr[-500:] if result.stderr else ""
            })
        except Exception as e:
            self.results.append({
                "url": task["url"],
                "success": False,
                "error": str(e)
            })
        self.process_queue()


# ============================================================
# UI State
# ============================================================
dm = DownloadManager()

def main(page: ft.Page):
    page.title = "Auto-Downloader"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20

    status_text = ft.Text("Ready", size=14, color=ft.Colors.GREY)
    log_area = ft.TextField(
        multiline=True,
        read_only=True,
        min_lines=8,
        max_lines=12,
        border_color=ft.Colors.SURFACE_CONTAINER_HIGHEST,
    )
    url_input = ft.TextField(
        label="URL",
        hint_text="https://twitter.com/...",
        expand=True,
 )
    platform_dropdown = ft.Dropdown(
        label="Platform",
        value="auto",
        options=[
            ft.dropdown.Option("auto", "Auto-detect"),
            ft.dropdown.Option("twitter", "Twitter/X"),
            ft.dropdown.Option("pixiv", "Pixiv"),
            ft.dropdown.Option("instagram", "Instagram"),
            ft.dropdown.Option("reddit", "Reddit"),
            ft.dropdown.Option("danbooru", "Danbooru"),
        ],
        width=150,
    )
    download_btn = ft.ElevatedButton("Download", icon=ft.Icons.DOWNLOAD)
    clear_btn = ft.OutlinedButton("Clear Log", icon=ft.Icons.CLEAR)

    def on_download(e):
        url = url_input.value.strip()
        if not url:
            return
        platform = platform_dropdown.value
        log_area.value += f"\n[+] Starting: {url} ({platform})\n"
        status_text.value = "Downloading..."
        download_btn.disabled = True
        page.update()

        def bg():
            dm.add_task(url, platform)
            log_area.value += f"[✓] Done: {url}\n"
            status_text.value = "Ready"
            download_btn.disabled = False
            page.update()

        threading.Thread(target=bg, daemon=True).start()

    def on_clear(e):
        log_area.value = ""
        page.update()

    download_btn.on_click = on_download
    clear_btn.on_click = on_clear

    page.add(
        ft.Text("Auto-Downloader", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        ft.Row([url_input, platform_dropdown, download_btn]),
        status_text,
        ft.Container(
            content=log_area,
            border=ft.border.all(1, ft.Colors.SURFACE_VARIANT),
            border_radius=8,
            padding=10,
 ),
        clear_btn,
    )

if __name__ == "__main__":
    ft.app(target=main)
