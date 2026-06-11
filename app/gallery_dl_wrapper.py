"""
gallery-dl wrapper for Auto-Downloader
Handles platform-specific URL parsing and download execution
"""
import subprocess
import json
import re
from typing import List, Dict, Optional

GALLERY_DL_CMD = "gallery-dl"

SUPPORTED_PLATFORMS = {
    "twitter": "Twitter/X",
    "pixiv": "Pixiv",
    "instagram": "Instagram",
    "reddit": "Reddit",
    "danbooru": "Danbooru",
    "gelbooru": "Gelbooru",
    "yande.re": "Yande.re",
    "auto": "Auto-detect",
}

def detect_platform(url: str) -> str:
    """Detect platform from URL"""
    if "twitter.com" in url or "x.com" in url:
        return "twitter"
    elif "pixiv.net" in url:
        return "pixiv"
    elif "instagram.com" in url:
        return "instagram"
    elif "reddit.com" in url:
        return "reddit"
    elif "danbooru.donmai.us" in url:
        return "danbooru"
    elif "gelbooru.com" in url:
        return "gelbooru"
    elif "yande.re" in url:
        return "yande.re"
    return "auto"

def build_command(url: str, platform: str, output_dir: str) -> List[str]:
    """Build gallery-dl command"""
    cmd = [
        GALLERY_DL_CMD,
        "--no-check-certificate",
        "-D", output_dir,
    ]
    if platform != "auto":
        cmd.extend(["--platform", platform])
    cmd.append(url)
    return cmd

def download(url: str, platform: str = "auto", output_dir: str = "/storage/emulated/0/Download/AutoDownloader") -> Dict:
    """Execute download and return result"""
    if platform == "auto":
        platform = detect_platform(url)

    cmd = build_command(url, platform, output_dir)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600
        )
        return {
            "success": result.returncode == 0,
            "url": url,
            "platform": platform,
            "stdout": result.stdout[-1000:] if result.stdout else "",
            "stderr": result.stderr[-1000:] if result.stderr else "",
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "url": url,
            "platform": platform,
            "error": "Download timeout (>10 min)",
        }
    except Exception as e:
        return {
            "success": False,
            "url": url,
            "platform": platform,
            "error": str(e),
        }

def get_image_count(url: str, platform: str = "auto") -> Optional[int]:
    """Estimate number of images in gallery (for progress)"""
    cmd = [
        GALLERY_DL_CMD,
        "--no-check-certificate",
        "--dry-run",
 ]
    if platform != "auto":
        cmd.extend(["--platform", platform])
    cmd.append(url)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            matches = re.findall(r"\b\d+\b\s+(?:images?|files?|results?)", result.stdout, re.I)
            return int(matches[0].split()[0]) if matches else None
    except:
        pass
    return None
