import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression

TASKS_FILE = "tasks.json"

def load_tasks():
    """Lataa tehtävät tiedostosta"""
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def train_model(tasks):
    """Kouluttaa koneoppimismallin käyttäjän aikataulutottumuksista"""
    data = []
    
    for task in tasks:
        if "completed_time" in task:  # Käytetään vain suoritettuja tehtäviä
            dt = datetime.strptime(task["completed_time"], "%Y-%m-%d %H:%M")
            data.append([dt.hour, dt.minute])
    
    if len(data) < 3:  # Tarvitaan vähintään 3 datapistettä, jotta malli voidaan kouluttaa
        return None

    df = pd.DataFrame(data, columns=["hour", "minute"])
    model = LinearRegression()
    model.fit(df[["hour"]], df["minute"])  # Opetetaan malli ennustamaan minuutit kellonajasta
    return model

def suggest_schedule():
    """Suosittelee parasta aikaa uudelle tehtävälle käyttäjän datan perusteella"""
    tasks = load_tasks()
    model = train_model(tasks)

    if model is None:
        return "Ei tarpeeksi dataa ennustamiseen. Käytä oletusaikaa 12:00."

    predicted_hour = int(model.predict(np.array([[12]]))[0])  # Ennustetaan klo 12 perustuen dataan
    return f"Suositeltu aika: {predicted_hour}:00"

if __name__ == "__main__":
    print(suggest_schedule())
# Compare this snippet from src/task_manager.py: