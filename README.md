# 🧠 Älykäs Aikataulutusassistentti

Älykäs Aikataulutusassistentti on Pythonilla toteutettu graafinen sovellus, joka auttaa käyttäjiä hallitsemaan tehtäviään tehokkaammin. Sovellus hyödyntää koneoppimista tehtävien keston ennustamiseen ja synkronoi tehtävät automaattisesti Google Kalenteriin.

## 🚀 Ominaisuudet

- 🧩 Ennustaa tehtävien keston Random Forest -mallilla
- 📅 Integroituu Google Kalenteriin (OAuth 2.0)
- ✅ Tunnistaa parhaan ajankohdan tehtävälle tekoälyn avulla
- 🖥️ Käyttäjäystävällinen graafinen käyttöliittymä (Tkinter)
- 📊 Tuki laajennettavalle opetusdatalle (.csv)

## 📸 Kuvakaappauksia

### Sovelluksen käyttöliittymä
![UI](./screenshots/käyttöliittymä.png)

### AI-ennuste
![Ennuste](./screenshots/ennusteen_näkymä.png)

### Google Kalenteri -integraatio
![Kalenteri](./screenshots/näkymäkalenteriis.png)

## 🧪 Opetusdatan rakenne (CSV)

| task_name          | task_type | difficulty | priority | deadline_days | start_hour | day_of_week | estimated_by_user | duration_minutes |
|--------------------|-----------|------------|----------|----------------|-------------|--------------|-------------------|------------------|
| Tenttiin lukeminen | opiskelu  | 3          | 4        | 2              | 10          | 1            | 60                | 55               |

## 🛠️ Teknologiat

- Python 3.10+
- Pandas
- Scikit-learn
- Tkinter
- Google API Python Client
- Pickle

## ⚙️ Asennus

1. Asenna riippuvuudet:
   ```bash
   pip install -r requirements.txt
   ```

2. Lisää Google API -tunnistetiedosto `credentials.json` juurikansioon.

3. Kouluta malli:
   ```bash
   python train_model.py
   ```

4. Käynnistä sovellus:
   ```bash
   python gui_ai_predict.py
   ```

## 📁 Projektin rakenne

```
├── gui_ai_predict.py
├── train_model.py
├── model.pkl
├── opetusdata_ai_kalenteri.csv
├── google_auth.py
├── credentials.json
└── README.md
```

## 📚 Lisenssi

Tämä projekti on tarkoitettu opetuskäyttöön ja on vapaasti muokattavissa.

---

Kehittänyt Jouni Kiviperä – 2025  
[Tekoälyn soveltaminen -kurssi]
