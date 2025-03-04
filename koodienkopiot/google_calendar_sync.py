from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import os
import datetime
from google_auth import authenticate_google
from smart_scheduler import suggest_reminder
from task_manager import load_tasks

TASKS_FILE = "tasks.json"

def get_calendar_service():
    """Hakee Google Calendar -palvelun"""
    creds = authenticate_google()
    return build("calendar", "v3", credentials=creds)

def add_task_to_calendar(service, task):
    """Lisää tehtävän Google Kalenteriin AI:n suosittelemalla muistutuksella"""
    title = task["title"]
    deadline = task["deadline"]
    
    reminder_minutes = suggest_reminder()

    try:
        start_time = datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M")
    except ValueError:
        print(f"⚠️ Virheellinen deadline-muoto: {deadline}. Käytetään oletusarvoa 12:00.")
        start_time = datetime.datetime.strptime("2025-02-28 12:00", "%Y-%m-%d %H:%M")

    end_time = start_time + datetime.timedelta(minutes=30)  

    event = {
        'summary': title,
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'Europe/Helsinki'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'Europe/Helsinki'},
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': reminder_minutes},  
            ],
        },
    }

    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f"✅ Tehtävä lisätty kalenteriin muistutuksella {reminder_minutes} min ennen: {title}")
        return event.get("id")  
    except HttpError as error:
        print(f"⚠️ Virhe lisättäessä tehtävää {title}: {error}")
        return None

def sync_tasks_to_calendar():
    """Synkronoi kaikki tehtävät Google Kalenteriin"""
    service = get_calendar_service()
    tasks = load_tasks()

    for task in tasks:
        add_task_to_calendar(service, task)
    
    print("✅ Tehtävät synkronoitu Google Kalenteriin!")
