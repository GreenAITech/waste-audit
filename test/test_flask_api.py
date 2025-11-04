import requests
import time
from datetime import datetime


def send_detection(class_name, confidence=0.95):
    url = "http://127.0.0.1:5000/api/throw"

    data = {
        "timestamp_str": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "class_name": class_name,
        "location": "bin_1",
        "confidence": confidence
    }

    try:
        response = requests.post(url, json=data)
        print(f"✓ Sent {class_name}: {response.json()}")
    except Exception as e:
        print(f"✗ Error: {e}")


if __name__ == "__main__":
    print("Testing Flask API - Sending detections...")
    time.sleep(2)

    items = ["bottle", "can", "bottle", "tetra", "plastic_bottle"]

    for i, item in enumerate(items, 1):
        print(f"\n[{i}/5] Throwing {item}...")
        send_detection(item)
        time.sleep(1.5)

    print("\n✓ Test complete! Check UI - Total should be 5")