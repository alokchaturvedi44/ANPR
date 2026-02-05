from pymongo import MongoClient
from datetime import datetime

# client = MongoClient("mongodb+srv://chaturvedialok44_db_user:FxHFDZZKMacwuohR@cluster0.thvr1so.mongodb.net/?appName=Cluster0")
client = MongoClient("mongodb+srv://chaturvedialok44_db_user:sDDTLmBMSTwEhh9C@cluster0.bgcmtgp.mongodb.net/?appName=Cluster0")
db = client["gate_db"]
logs = db["vehicle_logs"]

doc = {
    "plate": "TEST1234",
    "timestamp": datetime.now(),
    "status": "IN",
}

logs.insert_one(doc)
print("Inserted:", doc)
