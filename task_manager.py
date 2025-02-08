import json
import os

# JSON-tiedoston nimi, johon tehtävät tallennetaan
TASKS_FILE = "tasks.json"

def load_tasks():
    """
    Lataa tehtävät JSON-tiedostosta.
    Jos tiedostoa ei ole, palauttaa tyhjän listan.
    """
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []  # Palautetaan tyhjä lista, jos tiedostoa ei ole

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
    deadline = input("Deadline (YYYY-MM-DD HH:MM): ")
    
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
        "duration": duration
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
        print(f"{index}. {task['title']} (Deadline: {task['deadline']}, Tärkeys: {task['priority']}, Kesto: {task['duration']} min)")

def main():
    """
    Päävalikko, josta käyttäjä voi valita toiminnon.
    """
    while True:
        print("\n📌 TEHTÄVÄHALLINTA")
        print("1️⃣ Lisää uusi tehtävä")
        print("2️⃣ Näytä kaikki tehtävät")
        print("3️⃣ Poistu")
        
        choice = input("\nValitse toiminto (1-3): ")

        if choice == "1":
            add_task()
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            print("\n👋 Ohjelma suljetaan. Kiitos!")
            break
        else:
            print("\n⚠️ Virheellinen valinta, yritä uudelleen.")

if __name__ == "__main__":
    main()
