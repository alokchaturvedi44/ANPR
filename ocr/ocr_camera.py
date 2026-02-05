from ultralytics import YOLO
import cv2
import easyocr
from pymongo import MongoClient
from datetime import datetime
import re
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))

db = client["gate_db"]
logs = db["vehicle_logs"]

def get_next_status(plate: str, logs_collection):
    """Toggle IN/OUT based on last record for this plate."""
    last = logs_collection.find_one({"plate": plate}, sort=[("timestamp", -1)])
    if not last:
        return "IN"
    return "OUT" if last.get("status") == "IN" else "IN"


model = YOLO("models/license_plate_detector.pt")
reader = easyocr.Reader(["en"], gpu=False)

plate_pattern = re.compile(
    r"^([A-Z]{2}\d{2}[A-Z]{1,2}\d{4}|\d{2}[A-Z]{2}\d{4}[A-Z]{1,2})$"
)

last_seen = {}  

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model.predict(source=frame, conf=0.5, verbose=False)

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            crop = frame[y1:y2, x1:x2]
            text = reader.readtext(crop)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            if not text:
                continue

            plate_raw = text[0][1]
            plate = re.sub(r"[^A-Z0-9]", "", plate_raw.upper())

            print("OCR:", plate_raw, "->", plate)

            if not plate_pattern.match(plate):
                continue

            now = datetime.now()

            if plate in last_seen and (now - last_seen[plate]).total_seconds() < 10:
                continue

            status = get_next_status(plate, logs)

            doc = {
                "plate": plate,
                "timestamp": now,
                "status": status,
            }
            logs.insert_one(doc)
            last_seen[plate] = now
            print("Saved:", doc)

            display_text = f"{plate} ({status})"
            cv2.putText(
                frame,
                display_text,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 0, 0),
                2,
            )

    cv2.imshow("Vehicle Plate Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
