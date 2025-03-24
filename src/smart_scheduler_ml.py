# smart_scheduler_ml.py

import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime
import joblib
import os
import json

MODEL_FILE = "model.pkl"
TASK_FILE = "tasks.json"

def train_model():
    if not os.path.exists(TASK_FILE):
        print("Ei tehtävädataa mallin kouluttamiseen.")
        return

    with open(TASK_FILE, "r") as f:
        tasks = json.load(f)

    data = []
    for task in tasks:
        try:
            deadline_dt = datetime.strptime(task["deadline"], "%Y-%m-%d %H:%M")
            hour = deadline_dt.hour
            minute = deadline_dt.minute
            priority = int(task["priority"])
            duration = int(task.get("duration", 30))  # oletuskesto 30 min
            start_minutes = hour * 60 + minute - duration  # tavoitealoitusaika
            data.append([priority, duration, start_minutes])
        except Exception as e:
            print("Virhe datassa:", e)

    if not data:
        print("Ei riittävästi opetusdataa.")
        return

    df = pd.DataFrame(data, columns=["priority", "duration", "start_minutes"])
    X = df[["priority", "duration"]]
    y = df["start_minutes"]

    model = LinearRegression()
    model.fit(X, y)

    joblib.dump(model, MODEL_FILE)
    print("✅ Malli koulutettu ja tallennettu.")

def predict_schedule(priority: int, duration: int) -> str:
    if not os.path.exists(MODEL_FILE):
        print("⚠️ Mallia ei löydy. Koulutetaan ensin...")
        train_model()

    if not os.path.exists(MODEL_FILE):
        return "12:00"  # fallback

    model = joblib.load(MODEL_FILE)
    minutes = model.predict([[priority, duration]])[0]
    minutes = max(0, min(23*60+59, int(minutes)))  # välillä 00:00–23:59
    hour = minutes // 60
    minute = minutes % 60
    return f"{hour:02d}:{minute:02d}"
