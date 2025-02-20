import json
import os
from smart_scheduler import suggest_schedule

TASKS_FILE = "tasks.json"

def load_tasks():
    """Lataa tehtävät tiedostosta ja lisää puuttuva status-kenttä."""
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
    """Lisää uusi tehtävä ja käyttää tekoälyä suosittelemaan ajankohtaa."""
    title = input("Tehtävän otsikko: ")
    
    # AI ehdottaa ajankohtaa
    ai_suggestion = suggest_schedule()
    print(f"Tekoälyn suositus ajankohdaksi: {ai_suggestion}")
    
    # Käyttäjä voi joko hyväksyä suosituksen tai syöttää oman ajan
    deadline = input(f"Deadline (YYYY-MM-DD HH:MM) [Paina Enter hyväksyäksesi AI-suosituksen]: ")
    if deadline.strip() == "":
        deadline = f"2025-02-28 {ai_suggestion.split(':')[1]}:00"  # Käyttää AI:n suositusta

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

    print(f"✅ Tehtävä lisätty: {title} klo {deadline}")

def list_tasks():
    """Tulostaa kaikki tallennetut tehtävät komentoriville."""
    tasks = load_tasks()
    if not tasks:
        print("\n📭 Ei tallennettuja tehtäviä.")
        return
    
    print("\n📋 Tallennetut tehtävät:\n")
    for index, task in enumerate(tasks, start=1):
        print(f"{index}. {task['title']} (Deadline: {task['deadline']}, Tärkeys: {task['priority']}, Tila: {task['status']})")

def delete_task():
    """Poistaa käyttäjän valitseman tehtävän."""
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
            print(f"\n🗑️ Tehtävä poistettu: {removed_task['title']}")
        else:
            print("⚠️ Virheellinen valinta.")
    except ValueError:
        print("⚠️ Anna kelvollinen numero.")

def main():
    """Ohjelman päävalikko."""
    while True:
        print("\n📌 TEHTÄVÄHALLINTA")
        print("1️⃣ Lisää uusi tehtävä")
        print("2️⃣ Näytä kaikki tehtävät")
        print("3️⃣ Poista tehtävä")
        print("4️⃣ Poistu")

        choice = input("\nValitse toiminto (1-4): ")

        if choice == "1":
            add_task()
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            delete_task()
        elif choice == "4":
            print("\n👋 Ohjelma suljetaan. Kiitos!")
            break
        else:
            print("\n⚠️ Virheellinen valinta, yritä uudelleen.")

if __name__ == "__main__":
    main()
