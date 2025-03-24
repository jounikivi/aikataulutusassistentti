import datetime
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from task_manager import load_tasks

def get_calendar_service():
    """Palauttaa valmiin Google Calendar API -palvelun, käyttäen token.json -tiedostoa"""
    creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/calendar"])
    return build("calendar", "v3", credentials=creds)

def sync_tasks_to_calendar():
    """
    Synkronoi kaikki tehtävät Google Kalenteriin.
    Jokaisesta tehtävästä lisätään kalenteritapahtuma annetun deadlinen mukaisesti.
    """
    try:
        service = get_calendar_service()
        tasks = load_tasks()

        for task in tasks:
            try:
                # Muunnetaan deadline datetime-muotoon
                start_time = datetime.datetime.strptime(task["deadline"], "%Y-%m-%d %H:%M")
                end_time = start_time + datetime.timedelta(minutes=30)  # Oletuskesto 30 min

                event = {
                    "summary": task["title"],
                    "description": f"Tärkeysaste: {task['priority']}",
                    "start": {
                        "dateTime": start_time.isoformat(),
                        "timeZone": "Europe/Helsinki"
                    },
                    "end": {
                        "dateTime": end_time.isoformat(),
                        "timeZone": "Europe/Helsinki"
                    }
                }

                service.events().insert(calendarId="primary", body=event).execute()
                print(f"✅ Tapahtuma lisätty Google Kalenteriin: {task['title']}")

            except Exception as e:
                print(f"⚠️ Virhe lisättäessä tehtävää '{task['title']}': {e}")

    except Exception as e:
        print(f"❌ Virhe kalenteriyhteydessä: {e}")
