import json
import os

# JSON-tiedoston nimi, johon tehtävät tallennetaan
TASKS_FILE = "tasks.json"

def load_tasks():
    """
    Lataa tehtävät JSON-tiedostosta.
    Jos tiedosto on tyhjä tai virheellinen, palauttaa tyhjän listan.
    """
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, "r", encoding="utf-8") as file:
                data = file.read().strip()
                if not data:
                    return []
                return json.loads(data)
        except (json.JSONDecodeError, ValueError):
            print("⚠️ Virhe `tasks.json` -tiedoston lukemisessa. Luodaan uusi tiedosto.")
            return []
    return []

def save_tasks(tasks):
    """
    Tallentaa tehtävät JSON-tiedostoon.
    """
    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)

def add_task():
    """
    Pyytää käyttäjältä tehtävän tiedot ja tallentaa ne JSON-tiedostoon.
    """
    print("\n📌 Lisää uusi tehtävä\n")

    # Käyttäjän syötteet
    title = input("Tehtävän otsikko: ")
    deadline = input("Deadline (YYYY-MM-DD HH:MM): ").strip()

    # Jos käyttäjä ei syötä kellonaikaa, lisätään oletus (klo 12:00)
    if len(deadline) == 10:
        deadline += " 12:00"

    # Tarkistetaan, että tärkeys on välillä 1–5
    while True:
        try:
            priority = int(input("Tärkeysaste (1-5, jossa 5 on korkein): "))
            if 1 <= priority <= 5:
                break
            else:
                print("⚠️ Anna numero väliltä 1–5.")
        except ValueError:
            print("⚠️ Syötä numero väliltä 1–5.")

    # Tarkistetaan, että kesto on kokonaisluku
    while True:
        try:
            duration = int(input("Arvioitu kesto (minuutteina): "))
            break
        except ValueError:
            print("⚠️ Syötä numero.")

    # Luodaan tehtävä sanakirjana
    task = {
        "title": title,
        "deadline": deadline,
        "priority": priority,
        "duration": duration,
        "status": "pending"  # Oletuksena tehtävä on kesken
    }

    # Ladataan olemassa olevat tehtävät
    tasks = load_tasks()
    tasks.append(task)  # Lisätään uusi tehtävä listaan

    # Tallennetaan päivitetty tehtävälista
    save_tasks(tasks)

    print(f"\n✅ Tehtävä lisätty: {title} (Tärkeys: {priority}, Deadline: {deadline})")

def list_tasks():
    """
    Tulostaa kaikki tallennetut tehtävät komentoriville.
    """
    tasks = load_tasks()
    if not tasks:
        print("\n📭 Ei tallennettuja tehtäviä.")
        return
    
    print("\n📋 Tallennetut tehtävät:\n")
    for index, task in enumerate(tasks, start=1):
        print(f"{index}. {task['title']} (Deadline: {task['deadline']}, Tärkeys: {task['priority']}, Kesto: {task['duration']} min, Tila: {task['status']})")

def delete_task():
    """
    Poistaa käyttäjän valitseman tehtävän.
    """
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
    """
    Päävalikko, josta käyttäjä voi valita toiminnon.
    """
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

    
# Komentorivi: python task_manager.py
