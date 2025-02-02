from __future__ import print_function
import os
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Lataa ympäristömuuttujat
load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_calendar():
    """Lataa client_secret.json ja todenna käyttäjä."""
    creds = None
    if os.path.exists("token.json"):
        creds = InstalledAppFlow.from_authorized_user_file("token.json", SCOPES).run_local_server(port=0)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secret.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds

def list_events():
    """Listaa käyttäjän tulevat tapahtumat."""
    creds = authenticate_google_calendar()
    service = build("calendar", "v3", credentials=creds)

    now = datetime.datetime.utcnow().isoformat() + "Z"
    events_result = service.events().list(
        calendarId="primary",
        timeMin=now,
        maxResults=10,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])

    if not events:
        print("Ei tulevia tapahtumia.")
    for event in events:
        start = event.get("start", {}).get("dateTime", event.get("start", {}).get("date"))
        print(f"{start}: {event['summary']}")

if __name__ == "__main__":
    list_events()
