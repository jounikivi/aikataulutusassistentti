import datetime
from googleapiclient.discovery import build
from google_auth import get_credentials
from task_manager import load_tasks

def sync_tasks_to_calendar():
    """
    Synkronoi tehtävät Google Kalenteriin.
    Käyttää kirjautunutta käyttäjää ja lisää tapahtumat Kalenteriin.
    """
    try:
        creds = get_credentials()
        service = build("calendar", "v3", credentials=creds)
        tasks = load_tasks()

        for task in tasks:
            try:
                start_time = datetime.datetime.strptime(task["deadline"], "%Y-%m-%d %H:%M")
                end_time = start_time + datetime.timedelta(minutes=30)  # oletuskesto

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
                print(f"✅ Tapahtuma lisätty: {task['title']}")

            except Exception as e:
                print(f"⚠️ Virhe lisättäessä tehtävää '{task['title']}': {e}")

    except Exception as e:
        print(f"❌ Virhe kalenteriyhteydessä: {e}")
