from datetime import datetime
import time

from classifier import Classifier
from storage import Storage
from sync import export_to_json, is_online
from tracker import ActivityMonitor


def run_tracker():
    print("Starting activity tracker...")
    try:
        monitor = ActivityMonitor()
        classifier = Classifier()
        storage = Storage()
        print("✓ Initialized all components")
    except Exception as e:
        print(f"Error during initialization: {e}")
        return

    try:
        while True:
            try:
                print("\n--- Activity Check ---")
                now = datetime.now().isoformat()
                print(f"Time: {now}")
                
                app = monitor.get_active_window()
                print(f"Active Window: {app}")
                
                idle_time = monitor.get_idle_time()
                print(f"Idle Time: {idle_time}s")
                
                mouse_active = monitor.mouse_activity
                keyboard_active = monitor.keyboard_activity
                print(f"Mouse Active: {mouse_active}, Keyboard Active: {keyboard_active}")

                feature_vector = {
                    "app_name": app,
                    "idle_time": idle_time,
                    "mouse_activity": mouse_active,
                    "keyboard_activity": keyboard_active,
                    "time_of_day": now[11:13]
                }

                label = classifier.classify(feature_vector)
                print(f"Predicted Label: {label}")

                log_record = {
                    "timestamp": now,
                    "app_name": app,
                    "idle_time": idle_time,
                    "mouse_activity": mouse_active,
                    "keyboard_activity": keyboard_active,
                    "predicted_label": label
                }

                storage.insert_record(log_record)
                monitor.reset_activity_flags()

                if is_online():
                    export_to_json()
                    print("Data exported to JSON")

                print(f"Waiting 60 seconds before next check...")
                time.sleep(60)

            except Exception as e:
                print(f"Error during tracking: {e}")
                time.sleep(5)  

    except KeyboardInterrupt:
        print("\nTracker stopped by user.")


if __name__ == "__main__":
    run_tracker()
