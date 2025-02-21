import json
import os
from google_calendar_sync import get_calendar_service, update_task_in_calendar, delete_task_from_calendar

TASKS_FILE = "tasks.json"

def load_tasks():
    """Lataa tehtävät tiedostosta"""
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return []

def save_tasks(tasks):
    """Tallentaa tehtävät tiedostoon"""
    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)

def list_tasks():
    """Tulostaa kaikki tallennetut tehtävät"""
    tasks = load_tasks()
    if not tasks:
        print("\n📭 Ei tallennettuja tehtäviä.")
        return
    
    print("\n📋 Tallennetut tehtävät:")
    for index, task in enumerate(tasks, start=1):
        print(f"{index}. {task['title']} (Deadline: {task['deadline']}, Tärkeys: {task['priority']}, Tila: {task['status']})")

def update_task():
    """Päivittää käyttäjän valitseman tehtävän"""
    tasks = load_tasks()
    if not tasks:
        print("\n📭 Ei tehtäviä päivitettäväksi.")
        return

    list_tasks()
    try:
        task_num = int(input("\nValitse päivitettävän tehtävän numero: ")) - 1
        if 0 <= task_num < len(tasks):
            task = tasks[task_num]
            print(f"\n✏️ Päivitetään tehtävä: {task['title']}")
            task["title"] = input(f"Uusi nimi ({task['title']}): ") or task["title"]
            task["deadline"] = input(f"Uusi deadline (YYYY-MM-DD HH:MM) ({task['deadline']}): ") or task["deadline"]
            task["priority"] = input(f"Uusi tärkeysaste (1-5) ({task['priority']}): ") or task["priority"]

            save_tasks(tasks)
            update_task_in_calendar(get_calendar_service(), task)
            print(f"✅ Tehtävä päivitetty: {task['title']}")
        else:
            print("⚠️ Virheellinen valinta.")
    except ValueError:
        print("⚠️ Anna kelvollinen numero.")

def delete_task():
    """Poistaa käyttäjän valitseman tehtävän sekä Google Kalenterista että JSON-tiedostosta"""
    tasks = load_tasks()
    if not tasks:
        print("\n📭 Ei tehtäviä poistettavaksi.")
        return

    list_tasks()
    try:
        task_num = int(input("\nValitse poistettava tehtävän numero: ")) - 1
        if 0 <= task_num < len(tasks):
            removed_task = tasks.pop(task_num)
            save_tasks(tasks)
            delete_task_from_calendar(get_calendar_service(), removed_task)
            print(f"\n🗑️ Tehtävä poistettu: {removed_task['title']}")
        else:
            print("⚠️ Virheellinen valinta.")
    except ValueError:
        print("⚠️ Anna kelvollinen numero.")

def main():
    """Ohjelman päävalikko"""
    while True:
        print("\n📌 TEHTÄVÄHALLINTA")
        print("1️⃣ Näytä tehtävät")
        print("2️⃣ Päivitä tehtävä")
        print("3️⃣ Poista tehtävä")
        print("4️⃣ Poistu")

        choice = input("\nValitse toiminto (1-4): ")

        if choice == "1":
            list_tasks()
        elif choice == "2":
            update_task()
        elif choice == "3":
            delete_task()
        elif choice == "4":
            print("\n👋 Ohjelma suljetaan. Kiitos!")
            break
        else:
            print("\n⚠️ Virheellinen valinta, yritä uudelleen.")

if __name__ == "__main__":
    main()
