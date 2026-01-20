import subprocess, pathlib
from .config import RTSP_URL, IMAGE_PATH

pathlib.Path(IMAGE_PATH).parent.mkdir(parents=True, exist_ok=True)

def capture_latest():
    subprocess.run([
        "ffmpeg",
        "-y",
        "-hide_banner", "-loglevel", "error",
        "-rtsp_transport", "tcp",
        "-timeout", "5000000",
        "-i", RTSP_URL,
        "-frames:v", "1",
        "-q:v", "2",
        IMAGE_PATH
    ], check=True)
    return IMAGE_PATH
