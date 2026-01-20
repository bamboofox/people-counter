import os

RTSP_URL = os.environ.get(
    "RTSP_URL",
    "rtsp://user:pass@127.0.0.1/stream"
)

MODEL_PATH = "models/yolov8l.pt"
CONF = float(os.environ.get("CONF", "0.45"))
INTERVAL = int(os.environ.get("INTERVAL", "10"))
IMAGE_PATH = "/tmp/people/latest.jpg"

DISCORD_ENABLED = os.environ.get("DISCORD_ENABLED", "false") == "true"
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN", "")
DISCORD_CHANNEL_ID = os.environ.get("DISCORD_CHANNEL_ID", "")
DISCORD_NAME_TEMPLATE = os.environ.get(
    "DISCORD_NAME_TEMPLATE",
    "club-space-{count-people}"
)
