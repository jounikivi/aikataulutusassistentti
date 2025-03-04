import json
import os

TASKS_FILE_TEMPLATE = "tasks_{}.json"

def get_user_task_file():
    """Palauttaa kirjautuneen käyttäjän tehtävätiedoston nimen"""
    if os.path.exists("token.json"):
        with open("token.json", "r") as token:
            try:
                token_data = json.load(token)
                if isinstance(token_data, str):  # Jos JSON on string-muodossa, ladataan se uudelleen
                    token_data = json.loads(token_data)
                user_email = token_data.get("email", "default_user")
                return TASKS_FILE_TEMPLATE.format(user_email.replace("@", "_").replace(".", "_"))
            except json.JSONDecodeError:
                return None
    return None

def load_tasks():
    """Lataa tehtävät vain kirjautuneelle käyttäjälle"""
    user_task_file = get_user_task_file()
    if not user_task_file or not os.path.exists(user_task_file):
        return []
    with open(user_task_file, "r") as file:
        return json.load(file)

def save_tasks(tasks):
    """Tallentaa tehtävät kirjautuneelle käyttäjälle"""
    user_task_file = get_user_task_file()
    if user_task_file:
        with open(user_task_file, "w") as file:
            json.dump(tasks, file, indent=4)

def clear_tasks():
    """Tyhjentää tehtävälistan"""
    user_task_file = get_user_task_file()
    if user_task_file and os.path.exists(user_task_file):
        os.remove(user_task_file)
