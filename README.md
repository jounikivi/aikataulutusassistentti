# Älykäs Aikataulutusassistentti

Älykäs Aikataulutusassistentti on Pythonilla tehty Tkinter-työpöytäsovellus, jolla voit hallita tehtäviä paikallisesti ja synkronoida ne halutessasi Google Kalenteriin. Sovellus antaa lisäksi dataan perustuvan suosituksen siitä, milloin tehtävä kannattaa aloittaa ja kuinka paljon sille kannattaa varata aikaa.

## Ominaisuudet

- Paikallinen tehtävien hallinta ilman Google-kirjautumista
- Google Calendar -synkronointi OAuth 2.0 -kirjautumisella
- AI-avusteinen kesto- ja aloitusaikaehdotus tehtävälle
- Käyttäjäkohtaiset tehtävätiedostot kirjautumisen jälkeen
- CSV-pohjainen opetusdata, jota voi täydentää omalla tehtävähistorialla

## Teknologiat

- Python 3.10+
- Tkinter
- Google API Python Client
- Pickle
- CSV/JSON-pohjainen kevyt ennustemalli

## Käynnistys

1. Asenna riippuvuudet:
   ```bash
   pip install -r requirements.txt
   ```
2. Lisää projektin juureen Google OAuth -tiedosto:
   - `client_secret.json`
   - tai `credentials.json`
3. Kouluta malli valmiiksi halutessasi:
   ```bash
   python train_model.py
   ```
4. Käynnistä sovellus:
   ```bash
   python gui_ai_predict.py
   ```

Huomaa: Google-tiedosto tarvitaan vain kirjautumista ja kalenterisynkkaa varten. Tehtäviä voi lisätä, muokata ja poistaa myös ilman sitä.

## Miten AI-suositus toimii

Sovellus käyttää tiedostoa `opetusdata_ai_kalenteri.csv` perusopetusdatana. Kun mallia koulutetaan, se hyödyntää myös olemassa olevia `tasks*.json`-tiedostoja, jolloin suositukset voivat vähitellen mukautua omaan käyttötapaan.

Suositus käyttää seuraavia tietoja:

- tehtävän tärkeys
- käyttäjän oma kestoarvio
- deadline
- viikonpäivä ja kellonaika

Tuloksena sovellus arvioi tehtävälle sopivan työskentelykeston ja ehdottaa aloitusaikaa ennen deadlinea.

## Projektin rakenne

```
├── gui_ai_predict.py          # pääkäynnistin
├── train_model.py             # mallin koulutus
├── opetusdata_ai_kalenteri.csv
├── requirements.txt
├── src/
│   ├── gui_ai_predict.py      # kanoninen GUI-toteutus
│   ├── google_auth.py
│   ├── google_calendar_sync.py
│   ├── smart_scheduler_ml.py
│   ├── task_manager.py
│   └── task_utils.py
└── README.md
```

## Tallentuvat tiedostot

- `tasks_default_user.json`: paikallinen oletuskäyttäjän tehtävälista
- `tasks_<email>.json`: kirjautuneen käyttäjän tehtävälista
- `token.json`: Google OAuth -token
- `session.json`: kirjautuneen käyttäjän perustiedot
- `model.pkl`: koulutettu ennustemalli

## Lisenssi

Tämä projekti on tarkoitettu opetuskäyttöön ja on vapaasti muokattavissa.
