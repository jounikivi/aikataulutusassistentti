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

def suggest_reminder():
    """Suosittelee muistutusaikaa perustuen käyttäjän tehtäväkäyttäytymiseen"""
    tasks = load_tasks()
    model = train_model(tasks)

    if model is None:
        return 30  # Oletusmuistutus: 30 minuuttia ennen

    predicted_minute = int(model.predict(np.array([[12]]))[0])  # Ennustetaan minuuttimäärä klo 12
    return max(5, min(60, predicted_minute))  # Varmistetaan, että muistutus on 5–60 minuuttia ennen
