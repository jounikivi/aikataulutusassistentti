import json
import os

# JSON-tiedoston nimi, johon tehtävät tallennetaan
TasksFile = "tasks.json"

def load_tasks():
  """
    Lataa tehtävät JSON-tiedostosta.
    Jos tiedostoa ei ole, palauttaa tyhjän listan.
  """
  if os.path.exists(TasksFile):
    with open(TasksFile, "r") as file:
      return json.load(file)
  return [] # Palautetaan tyhjä lista, jos tiedostoa ei ole

def save_tasks(tasks):
  """
    Tallentaa tehtävät JSON-tiedostoon.
  """
  with open(TasksFile, "w", encoding="utf-8") as file:
    json.dump(tasks, file, indent=4, ensure_ascii=False)

def add_task(tasks, task):
  """
    Pyytää käyttäjältä tehtävän tiedot ja tallentaa ne JSON-tiedostoon.
  """
  print("\nLisää uusi tehtävä")
  
  # Pyydetään käyttäjältä tehtävän tiedot
  title = input("Tehtävän otsikko: ")
  deadline = input("Deadline (YYYY-MM-DD HH:MM): ")
  
  # Tarkistetaan, että tärkeys on vielä 1–5
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
      print("Virheellinen syöte. Yritä uudelleen.")
  
  
  
  