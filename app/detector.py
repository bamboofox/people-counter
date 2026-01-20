import cv2
from ultralytics import YOLO
from .config import MODEL_PATH, CONF

model = YOLO(MODEL_PATH)

def detect(image_path: str):
    img = cv2.imread(image_path)
    h, w, _ = img.shape

    result = model(img, conf=CONF, verbose=False)[0]

    boxes = []
    for box, cls in zip(result.boxes.xyxy, result.boxes.cls):
        if int(cls) == 0:  # person
            x1, y1, x2, y2 = map(int, box)
            boxes.append({
                "x1": x1, "y1": y1,
                "x2": x2, "y2": y2
            })

    return {
        "count": len(boxes),
        "boxes": boxes,
        "width": w,
        "height": h
    }
