 
import json
import os

TASKS_FILE = "tasks.json"

def load_tasks():
    """Lataa tehtävät tiedostosta ja lisää puuttuvan status-kentän."""
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, "r", encoding="utf-8") as file:
                tasks = json.load(file)
                for task in tasks:
                    if "status" not in task:
                        task["status"] = "pending"
                return tasks
        except json.JSONDecodeError:
            return []
    return []

def save_tasks(tasks):
    """Tallentaa tehtävät tiedostoon."""
    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)

def add_task():
    """Lisää uusi tehtävä."""
    title = input("Tehtävän otsikko: ")
    deadline = input("Deadline (YYYY-MM-DD HH:MM): ")
    priority = input("Tärkeysaste (1-5): ")

    task = {
        "title": title,
        "deadline": deadline,
        "priority": priority,
        "status": "pending"
    }

    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)

    print(f"✅ Tehtävä lisätty: {title}")

def main():
    """Ohjelman päävalikko."""
    while True:
        print("\n1️⃣ Lisää tehtävä\n2️⃣ Näytä tehtävät\n3️⃣ Poistu")
        choice = input("Valitse: ")

        if choice == "1":
            add_task()
        elif choice == "2":
            print(load_tasks())
        elif choice == "3":
            break

if __name__ == "__main__":
    main()
