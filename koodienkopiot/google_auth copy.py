from google_auth_oauthlib.flow import InstalledAppFlow
import os
import json

TOKEN_FILE = "token.json"

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def authenticate_google():
    """Autentikoi käyttäjä ja tallentaa Google-tunnukset."""
    creds = None

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as token:
            creds = json.load(token)

    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
        creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as token:
            json.dump(creds.to_json(), token)

    return creds

def logout_google():
    """Poistaa kirjautumistiedot ja kirjaa käyttäjän ulos."""
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
        print("✅ Käyttäjä kirjattu ulos!")
    else:
        print("⚠️ Käyttäjä ei ollut kirjautunut sisään.")
