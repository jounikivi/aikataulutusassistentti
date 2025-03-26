import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import pickle

# Ladataan data
df = pd.read_csv("opetusdata_ai_kalenteri.csv")

# Valitaan selittävät muuttujat ja kohdemuuttuja
X = df[["difficulty", "priority", "deadline_days", "start_hour", "day_of_week", "estimated_by_user"]]
y = df["duration_minutes"]

# Jaetaan data opetus- ja testiosaan
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Koulutetaan malli
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Ennustetaan ja lasketaan virhe
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f"Mean Absolute Error: {mae:.2f} min")

# Tallennetaan malli tiedostoon
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
