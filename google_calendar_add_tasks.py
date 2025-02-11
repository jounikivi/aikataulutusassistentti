from __future__ import print_function
import os
import json
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Google Calendar API:n käyttöoikeusalue
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Tiedosto, josta tehtävät luetaan
TASKS_FILE = "tasks.json"

def authenticate_google_calendar():
    """
    Lataa client_secret.json ja todenna käyttäjä.
    Jos token.json on jo olemassa, käytetään sitä.
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds

def load_tasks():
    """
    Lataa tehtävät `tasks.json` -tiedostosta.
    """
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []  # Palautetaan tyhjä lista, jos tiedostoa ei ole

def add_tasks_to_calendar():
    """
    Lisää kaikki tehtävät Google Kalenteriin.
    """
    creds = authenticate_google_calendar()
    service = build("calendar", "v3", credentials=creds)

    tasks = load_tasks()
    
    if not tasks:
        print("\n📭 Ei tehtäviä lisättäväksi.")
        return
    
    for task in tasks:
        try:
            # Luetaan tehtävän tiedot
            title = task["title"]
            deadline = task["deadline"]
            duration = int(task["duration"])  # Muutetaan kesto minuuteiksi

            # Jos käyttäjä on syöttänyt vain päivämäärän ilman kellonaikaa, lisätään oletuskellonaika (klo 12:00)
            if len(deadline) == 10:  # "YYYY-MM-DD" on 10 merkkiä pitkä
                deadline += " 12:00"  # Lisätään oletuskellonaika

            # Muunnetaan deadline oikeaan datetime-muotoon
            start_time = datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M")
            end_time = start_time + datetime.timedelta(minutes=duration)

            # Muodostetaan tapahtuman tietue
            event = {
                'summary': title,
                'description': f"Tärkeysaste: {task['priority']}",
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'Europe/Helsinki',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'Europe/Helsinki',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 30},  # Muistutus 30 min ennen
                    ],
                },
            }

            # Lähetetään tapahtuma Google Kalenteriin
            event = service.events().insert(calendarId='primary', body=event).execute()
            print(f"✅ Tapahtuma lisätty: {event.get('htmlLink')} ({title})")

        except Exception as e:
            print(f"⚠️ Virhe lisättäessä tehtävää {title}: {e}")

if __name__ == "__main__":
    add_tasks_to_calendar()
