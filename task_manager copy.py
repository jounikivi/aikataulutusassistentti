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

def svae_tasks(tasks):
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
  titlte = input("Otsikko: ")
  deadline = input("Määräpäivä (yyyy-mm-dd): ")
  
  #Tarkistetaan, että tärkeys on välillä 1–5
  while True:
    try:
      priority = int(input("Tärkeys (1-5): "))
      if 1 <= priority <= 5:
        break
      else:
        print("Tärkeys on oltava välillä 1–5.")

    #Tarkistetaan, että tärkeys on välillä 1–5
    
    while True:
      try:
        duration = int(input("Kesto (minuutteina): "))
        break
      except ValueError:
        print("Syötä numero.")
        
        # Luodaan tehtävä sanakirjana
    task = {
      "title": title,
      "deadline": deadline,
      "priority": priority,
      "duration": duration
    }
    tasks.append(task)