from __future__ import print_function
import os
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Google Calendar API:n käyttöoikeusalue
SCOPES = ['https://www.googleapis.com/auth/calendar']

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

def delete_old_events():
    """
    Poistaa kaikki menneet tapahtumat Google Kalenterista.
    """
    creds = authenticate_google_calendar()
    service = build("calendar", "v3", credentials=creds)

    # Hae nykyhetki UTC-ajassa
    now = datetime.datetime.utcnow().isoformat() + "Z"

    # Hae menneet tapahtumat
    events_result = service.events().list(
        calendarId="primary",
        timeMax=now,  # Hae vain menneisyyteen sijoittuvat tapahtumat
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])

    if not events:
        print("📭 Ei poistettavia tapahtumia.")
        return
    
    # Poistetaan kaikki haetut tapahtumat
    for event in events:
        try:
            event_id = event["id"]
            service.events().delete(calendarId="primary", eventId=event_id).execute()
            print(f"🗑️ Poistettu: {event.get('summary')} (ID: {event_id})")
        except Exception as e:
            print(f"⚠️ Virhe poistettaessa tapahtumaa: {event.get('summary')} - {e}")

if __name__ == "__main__":
    delete_old_events()
