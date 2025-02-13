# AIKATAULUTUSASSISTENTTI - TESTIKOMENNOT

## 1️⃣ Google API -autentikoinnin testaaminen

```bash
python src/google_auth.py
```

Jos selain **EI** avaudu, poista `token.json` ja testaa uudelleen:

```bash
del token.json  # Windows
python src/google_auth.py
```

## 2️⃣ Tehtävien hallinnan testaaminen

```bash
python src/task_manager.py
```

Valitse:
- 1️⃣ Lisää tehtävä, syötä testitiedot.
- 2️⃣ Näytä tehtävät, varmista, että lisätty tehtävä näkyy.
- 3️⃣ Poistu painamalla 3️⃣.

## 3️⃣ Tarkistetaan tehtävien tallennus

```bash
cat tasks.json  # Mac/Linux
type tasks.json  # Windows
```

Tarkista, että lisätty tehtävä näkyy JSON-tiedostossa.

## 4️⃣ Google Kalenterin synkronointi

```bash
python src/google_calendar_sync.py
```

Tarkista, että tehtävä lisätään Google Kalenteriin.
Suorita sama komento uudelleen ja varmista, ettei tehtävä lisäänny kahdesti.

## 5️⃣ Kaikkien osien yhteistestaus

```bash
python src/google_auth.py
python src/task_manager.py
python src/google_calendar_sync.py
```

Tällä järjestyksellä varmistetaan, että kaikki toimii saumattomasti.
