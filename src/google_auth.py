import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv

# Ladataan API-avaimet .env-tiedostosta
load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google():
    """Autentikoi käyttäjän Google Calendar API:lle ja palauttaa käyttöoikeustunnisteet."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds

