from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import joblib
import random
import os  # Add this import if not already present

# Simulated data
apps = ["Code.exe", "Slack.exe", "YouTube.exe", "Chrome.exe", "Explorer.exe"]
labels = ["work", "break", "idle", "work", "unproductive"]

data = []

for _ in range(500):
    app = random.choice(apps)
    idle_time = random.randint(0, 300)
    keyboard_activity = random.choice([0, 1])
    mouse_activity = random.choice([0, 1])
    time_of_day = random.randint(0, 23)

    label = "work" if app in ["Code.exe", "Slack.exe"] and idle_time < 60 else \
            "idle" if idle_time > 180 else \
            "unproductive" if app in ["YouTube.exe"] else "break"

    data.append({
        "app_name": app,
        "idle_time": idle_time,
        "keyboard_activity": keyboard_activity,
        "mouse_activity": mouse_activity,
        "time_of_day": time_of_day,
        "label": label
    })

df = pd.DataFrame(data)

# Convert categorical 'app_name' to one-hot
X = pd.get_dummies(df.drop(columns=["label"]))
y = df["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)

# Ensure the 'tracker' directory exists
os.makedirs("model", exist_ok=True)

# Save model
joblib.dump(clf, "model/model.joblib")

print("✅ Dummy model trained and saved as 'tracker/model.joblib'")
