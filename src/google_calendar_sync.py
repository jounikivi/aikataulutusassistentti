from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import os
import datetime
from google_auth import authenticate_google

TASKS_FILE = "tasks.json"

def load_tasks():
    """Lataa tehtävät tiedostosta"""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    """Tallentaa päivitetyt tehtävät tiedostoon"""
    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)

def add_task_to_calendar(service, task):
    """Lisää yksittäisen tehtävän Google Kalenteriin"""
    title = task["title"]
    deadline = task["deadline"]
    
    # Jos käyttäjä ei määritä aikaa, käytetään oletuksena klo 12:00
    if len(deadline) == 10:
        deadline += " 12:00"

    start_time = datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M")
    end_time = start_time + datetime.timedelta(minutes=30)  # Oletuskesto 30 min

    event = {
        'summary': title,
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'Europe/Helsinki'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'Europe/Helsinki'},
    }

    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f"✅ Tehtävä lisätty kalenteriin: {title}")
        return event.get("id")  # Palauttaa tapahtuman ID:n
    except HttpError as error:
        print(f"⚠️ Virhe lisättäessä tehtävää {title}: {error}")
        return None

def sync_tasks_to_calendar():
    """Synkronoi tehtävät Google Kalenteriin"""
    print("🔄 Synkronoidaan tehtävät Google Kalenteriin...")
    creds = authenticate_google()
    service = build("calendar", "v3", credentials=creds)

    tasks = load_tasks()
    if not tasks:
        print("📭 Ei tehtäviä lisättäväksi.")
        return

    for task in tasks:
        if task.get("status") == "completed":
            continue  # Ohitetaan jo lisätyt tehtävät

        event_id = add_task_to_calendar(service, task)
        if event_id:
            task["status"] = "completed"
    
    save_tasks(tasks)
    print("✅ Synkronointi valmis!")

if __name__ == "__main__":
    sync_tasks_to_calendar()
    print("✅ Tehtävät synkronoitu Google Kalenteriin.")