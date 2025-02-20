from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import os
import datetime
from google_auth import authenticate_google
from smart_scheduler import suggest_reminder

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
    """Lisää yksittäisen tehtävän Google Kalenteriin AI:n suosittelemalla muistutuksella"""
    title = task["title"]
    deadline = task["deadline"]

    # Muistutus perustuen AI-analyysiin
    reminder_minutes = suggest_reminder()

    try:
        # Varmistetaan, että deadline on oikeassa muodossa
        start_time = datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M")
    except ValueError:
        print(f"⚠️ Virheellinen deadline-muoto: {deadline}. Käytetään oletusarvoa 12:00.")
        start_time = datetime.datetime.strptime("2025-02-28 12:00", "%Y-%m-%d %H:%M")

    end_time = start_time + datetime.timedelta(minutes=30)  # Oletuskesto 30 min

    event = {
        'summary': title,
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'Europe/Helsinki'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'Europe/Helsinki'},
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': reminder_minutes},  # AI:n ehdottama muistutus
            ],
        },
    }

    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f"✅ Tehtävä lisätty kalenteriin muistutuksella {reminder_minutes} min ennen: {title}")
        return event.get("id")  # Palauttaa tapahtuman ID:n
    except HttpError as error:
        print(f"⚠️ Virhe lisättäessä tehtävää {title}: {error}")
        return None

def sync_tasks_to_calendar():
    """Synkronoidaan tehtävät Google Kalenteriin AI:n suosittelemalla muistutuksella"""
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
