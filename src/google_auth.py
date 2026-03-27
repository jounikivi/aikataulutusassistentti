from __future__ import annotations

import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

TOKEN_FILE = Path("token.json")
SESSION_FILE = Path("session.json")
CLIENT_SECRET_CANDIDATES = ("client_secret.json", "credentials.json")
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/calendar",
]


class GoogleAuthError(RuntimeError):
    """Selkeä virheluokka käyttöliittymää varten."""


def _load_google_modules():
    try:
        from google.auth.transport.requests import Request as GoogleRequest
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError as exc:
        raise GoogleAuthError(
            "Google-kirjastot puuttuvat. Asenna riippuvuudet komennolla `pip install -r requirements.txt`."
        ) from exc

    return Credentials, InstalledAppFlow, GoogleRequest


def _find_client_secret_file() -> str:
    for candidate in CLIENT_SECRET_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    raise FileNotFoundError(
        "Lisää projektin juureen Google OAuth -tiedosto `client_secret.json` tai `credentials.json`."
    )


def load_user_session() -> dict[str, str]:
    if not SESSION_FILE.exists():
        return {}

    try:
        with SESSION_FILE.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return {}

    if not isinstance(data, dict):
        return {}

    return {key: str(value) for key, value in data.items() if value}


def _save_user_session(profile: dict[str, str]) -> None:
    if not profile:
        return

    with SESSION_FILE.open("w", encoding="utf-8") as handle:
        json.dump(profile, handle, ensure_ascii=False, indent=2)


def get_current_user_email(default: str = "default_user") -> str:
    session = load_user_session()
    return session.get("email", default)


def is_authenticated() -> bool:
    return TOKEN_FILE.exists()


def _fetch_user_profile(access_token: str) -> dict[str, str]:
    if not access_token:
        return {}

    request = Request(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    try:
        with urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, OSError):
        return {}

    profile = {}
    if data.get("email"):
        profile["email"] = str(data["email"])
    if data.get("name"):
        profile["name"] = str(data["name"])
    return profile


def get_credentials(interactive: bool = True):
    Credentials, InstalledAppFlow, GoogleRequest = _load_google_modules()

    creds = None
    if TOKEN_FILE.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
            if not creds.has_scopes(SCOPES):
                creds = None
        except Exception:
            creds = None

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(GoogleRequest())
        except Exception:
            creds = None

    if not creds or not creds.valid:
        if not interactive:
            return None

        flow = InstalledAppFlow.from_client_secrets_file(_find_client_secret_file(), SCOPES)
        creds = flow.run_local_server(port=0)

    with TOKEN_FILE.open("w", encoding="utf-8") as handle:
        handle.write(creds.to_json())

    profile = _fetch_user_profile(getattr(creds, "token", ""))
    if profile:
        _save_user_session(profile)

    return creds


def authenticate_google():
    return get_credentials(interactive=True)


def logout_google() -> None:
    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()
    if SESSION_FILE.exists():
        SESSION_FILE.unlink()
