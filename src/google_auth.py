import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Määritellään kalenterikäyttöön tarvittava lupa
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_credentials():
    """
    Palauttaa Google API -valtuutukset.
    Käyttää token.json-tiedostoa jos olemassa, tai aloittaa kirjautumisen.
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Tallennetaan token uudelleen
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds
