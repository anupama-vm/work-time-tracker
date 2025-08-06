import json
from urllib import request

from storage import Storage

def is_online():
    try:
        request.get("https://www.google.com", timeout=3)
        return True
    except request.RequestException:
        return False

def export_to_json(filepath="tracker/exported_logs.json"):
    storage = Storage()
    records = storage.get_all_records()

    data = [
        {
            "timestamp": r[1],
            "app_name": r[2],
            "idle_time": r[3],
            "mouse_activity": r[4],
            "keyboard_activity": r[5],
            "predicted_label": r[6]
        }
        for r in records
    ]

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Data exported to {filepath}")
