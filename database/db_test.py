import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))

db = client["gate_db"]
logs = db["vehicle_logs"]

doc = {
    "plate": "TEST1234",
    "timestamp": datetime.now(),
    "status": "IN",
}

logs.insert_one(doc)
print("Inserted:", doc)
