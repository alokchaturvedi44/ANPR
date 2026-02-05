def get_next_status(plate, logs_collection):
    """Toggle IN/OUT based on last record for this plate."""
    last = logs_collection.find_one({"plate": plate}, sort=[("timestamp", -1)])
    if not last:
        return "IN"
    return "OUT" if last.get("status") == "IN" else "IN"
