import json
import os

TASK_FILE = "tasks.json"

def get_user_email():
    """
    Palauttaa kirjautuneen käyttäjän sähköpostin token.json-tiedostosta.
    Jos käyttäjä ei ole kirjautunut, palautetaan oletusnimi.
    """
    try:
        with open("token.json", "r") as token_file:
            token_data = json.load(token_file)
            return token_data.get("email", "default_user")
    except Exception:
        return "default_user"

def get_user_task_file():
    """
    Palauttaa käyttäjäkohtaisen tehtävätiedoston nimen.
    """
    email = get_user_email().replace("@", "_").replace(".", "_")
    return f"tasks_{email}.json"

def load_tasks():
    """
    Lataa tehtävät käyttäjäkohtaisesta tiedostosta.
    """
    file_path = get_user_task_file()
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    """
    Tallentaa annetut tehtävät käyttäjäkohtaisesti.
    """
    file_path = get_user_task_file()
    with open(file_path, "w") as file:
        json.dump(tasks, file, indent=2)
