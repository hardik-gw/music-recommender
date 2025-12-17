import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler

# ----------------------------
# Features used for similarity
# ----------------------------
FEATURES = [
    'valence',
    'acousticness',
    'danceability',
    'duration_ms',
    'energy',
    'explicit',
    'instrumentalness',
    'liveness',
    'loudness',
    'popularity',
    'speechiness',
    'tempo'
]

# ----------------------------
# Load dataset
# ----------------------------
df = pd.read_csv("data/data.csv")

# ----------------------------
# Prepare feature matrix
# ----------------------------
X = df[FEATURES].fillna(df[FEATURES].mean())

# ----------------------------
# Scale features
# ----------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ----------------------------
# Save artifacts
# ----------------------------
with open("model/artifacts.pkl", "wb") as f:
    pickle.dump(
        {
            "scaler": scaler,
            "data": df,
            "X_scaled": X_scaled,
            "features": FEATURES
        },
        f
    )

print("✅ Training complete. Artifacts saved to model/artifacts.pkl")
