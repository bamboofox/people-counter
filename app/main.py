from fastapi import FastAPI
from fastapi.responses import FileResponse
from threading import Thread
import time, datetime

from .camera import capture_latest
from .detector import detect
from .discord import update_channel
from .config import IMAGE_PATH, INTERVAL

app = FastAPI()

state = {
    "count": 0,
    "boxes": [],
    "width": 0,
    "height": 0,
    "updated_at": None
}

def worker():
    while True:
        try:
            img = capture_latest()
            res = detect(img)

            state.update(res)
            state["updated_at"] = datetime.datetime.now().isoformat()

            update_channel(res["count"])
        except Exception as e:
            print("worker error:", e)

        time.sleep(INTERVAL)

Thread(target=worker, daemon=True).start()

@app.get("/status")
def status():
    return state

@app.get("/image")
def image():
    return FileResponse(IMAGE_PATH)

@app.get("/")
def index():
    return FileResponse("static/index.html")
