### **📌 Päivitetty `README.md`**  
✅ **Parannettu versio, joka sisältää selkeämmät ohjeet ja lisätietoja.**  

📌 **Tallenna tämä `README.md`-tiedostoksi projektisi juurikansioon (`C:\aikataulutusassistentti\README.md`).**  

---

### **📅 Älykäs Aikataulutusassistentti**
**Graafinen tehtävienhallintasovellus, joka hyödyntää tekoälyä ja Google Kalenteria tehtävien optimointiin.**  
Tehtävien aikataulutusta ja muistutuksia optimoidaan koneoppimisen avulla, ja kaikki synkronoidaan Google Kalenteriin.

---

## 🔹 **Ominaisuudet**
✅ **Tehtävien hallinta (lisää, muokkaa, poista)**  
✅ **Tekoäly arvioi parhaan ajankohdan tehtävälle**  
✅ **Google Kalenteriin synkronointi**  
✅ **Muistutukset perustuvat käyttäjän aiempaan toimintaan**  
✅ **Graafinen käyttöliittymä (Tkinter)**  

---

## 🔹 **1️⃣ Asennusohjeet**
### **1.1. Lataa projektin tiedostot**
📌 **Jos käytät GitHubia, lataa tiedostot näin:**  
```bash
git clone https://github.com/KÄYTTÄJÄNIMI/aikataulutusassistentti.git
cd aikataulutusassistentti
```
📌 **Jos kopioit tiedostot manuaalisesti, siirry projektikansioon:**  
```bash
cd C:\aikataulutusassistentti
```

---

### **1.2. Asenna tarvittavat riippuvuudet**
📌 **Asenna kaikki paketit `requirements.txt`-tiedostosta:**  
```bash
pip install -r requirements.txt
```

📌 **Jos `requirements.txt` puuttuu, voit asentaa tärkeimmät paketit manuaalisesti näin:**  
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client pandas
```

---

### **1.3. Käynnistä sovellus**
📌 **Avaa käyttöliittymä (GUI) suorittamalla:**  
```bash
python src/gui.py
python src/gui_ai_predict.py   
```

---

## 🔹 **2️⃣ Sovelluksen käyttö**
1️⃣ **Kirjaudu sisään Google-tililläsi**  
2️⃣ **Lisää tehtävä** (Anna tehtävän nimi, deadline ja tärkeys)  
3️⃣ **Muokkaa tai poista tehtäviä tarpeen mukaan**  
4️⃣ **Synkronoi tehtävät Google Kalenteriin**  
5️⃣ **Tekoäly ehdottaa sinulle optimaalisen ajankohdan tehtävän suorittamiseen**  

---

## 🔹 **3️⃣ Vaaditut teknologiat ja kirjastot**
✅ **Python 3.10+** – Ohjelmointikieli  
✅ `tkinter` – Graafinen käyttöliittymä  
✅ `google-auth`, `google-auth-oauthlib`, `google-auth-httplib2` – Google API -kirjastot  
✅ `google-api-python-client` – Google Kalenterin hallinta  
✅ `pandas` – Tietojenkäsittely ja analytiikka  
✅ `datetime` – Aikataulujen hallinta  

---

## 🛠 **4️⃣ Vianetsintä**
### **"ModuleNotFoundError: No module named 'google.oauth2'"**
✅ Asenna puuttuvat paketit komennolla:  
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### **"Google API -autentikointi epäonnistui"**
✅ Varmista, että **`token.json`** on olemassa ja päivitä tunnukset uudelleen käynnistämällä sovellus.

---

## 📌 **5️⃣ Jatkokehitys**
💡 **Seuraavat lisäominaisuudet:**  
- **Tietokantapohjainen tehtävien tallennus (SQLite/PostgreSQL)**  
- **Graafinen analytiikka tehtävien suorittamisesta (matplotlib)**  
- **Tehtävien jako ja yhteistyömahdollisuudet**  
- **Parempi tekoäly ennustamaan käyttäjän ajankäyttöä**  

