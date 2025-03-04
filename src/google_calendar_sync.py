from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json
import os
from task_manager import load_tasks
from datetime import datetime, timedelta

def get_calendar_service():
    """Hakee Google Kalenterin API-palvelun"""
    if os.path.exists("token.json"):
        try:
            with open("token.json", "r") as token:
                token_data = json.load(token)

                # Jos token_data on string-muodossa, muokataan se dict-muotoon
                if isinstance(token_data, str):
                    token_data = json.loads(token_data)

                creds = Credentials.from_authorized_user_info(token_data)
                return build("calendar", "v3", credentials=creds)
        except json.JSONDecodeError:
            print("⚠️ Virhe: token.json ei ole kelvollinen JSON-tiedosto.")
            return None
    else:
        print("⚠️ Virhe: token.json puuttuu. Kirjaudu sisään ensin.")
        return None

def add_task_to_calendar(service, task):
    """Lisää tehtävän Google Kalenteriin"""
    try:
        # Tarkistetaan, onko deadline olemassa ja oikeassa muodossa
        try:
            deadline_dt = datetime.strptime(task["deadline"], "%Y-%m-%d %H:%M")
        except ValueError:
            print(f"⚠️ Virhe: Tehtävän '{task['title']}' deadline on väärässä muodossa.")
            return None

        start_time = deadline_dt.strftime("%Y-%m-%dT%H:%M:%S")  # Googleen oikea formaatti
        end_time = (deadline_dt + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")  # +1 tunti oletuksena

        event = {
            'summary': task["title"],
            'start': {
                'dateTime': start_time,
                'timeZone': 'Europe/Helsinki',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'Europe/Helsinki',
            },
            'description': f"Tärkeysaste: {task['priority']}",
        }

        event_result = service.events().insert(calendarId='primary', body=event).execute()
        return event_result.get('id')

    except Exception as e:
        print(f"⚠️ Virhe lisättäessä tehtävää '{task['title']}' Google Kalenteriin: {e}")
        return None

def sync_tasks_to_calendar():
    """Synkronoi tehtävät Google Kalenteriin"""
    service = get_calendar_service()
    if not service:
        print("⚠️ Google Kalenterin API-palvelua ei saatu ladattua.")
        return

    tasks = load_tasks()
    if not tasks:
        print("ℹ️ Ei tehtäviä synkronoitavaksi.")
        return

    for task in tasks:
        event_id = add_task_to_calendar(service, task)
        if event_id:
            print(f"✅ Tehtävä '{task['title']}' lisätty Google Kalenteriin (ID: {event_id})")
