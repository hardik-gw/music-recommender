import pickle
import pandas as pd
from scipy.spatial.distance import cdist
from difflib import get_close_matches

with open("model/artifacts.pkl", "rb") as f:
    obj = pickle.load(f)

df = obj["data"]
X_scaled = obj["X_scaled"]

df["year"] = pd.to_numeric(df["year"], errors="coerce")
df["popularity"] = pd.to_numeric(df["popularity"], errors="coerce")

# ----------------------------
# Anchor resolution (robust)
# ----------------------------
def find_anchor(song_name, artist_name):
    song = song_name.lower()
    artist = artist_name.lower()

    # Clean common junk
    song = song.replace("(drake)", "").replace("feat.", "").strip()

    # 1️⃣ Song + artist
    exact = df[
        df["name"].str.lower().str.contains(song, na=False) &
        df["artists"].str.lower().str.contains(artist, na=False)
    ]
    if not exact.empty:
        return exact.index[0]

    # 2️⃣ Song-only
    name_only = df[df["name"].str.lower().str.contains(song, na=False)]
    if not name_only.empty:
        return name_only.index[0]

    # 3️⃣ Fuzzy fallback
    names = df["name"].str.lower().tolist()
    match = get_close_matches(song, names, n=1, cutoff=0.6)
    if match:
        return names.index(match[0])

    return None

# ----------------------------
# Recommender
# ----------------------------
def recommend_from_song(song_name, artist_name, n=10):
    idx = find_anchor(song_name, artist_name)

    if idx is None:
        return "Song not found in dataset."

    anchor_year = df.loc[idx, "year"]
    anchor_vec = X_scaled[idx].reshape(1, -1)

    # 🔥 PDF LOGIC: Era + popularity filter
    candidates = df[
        (df["year"] >= anchor_year - 5) &
        (df["year"] <= anchor_year + 5) &
        (df["popularity"] >= 20)
    ]

    # Fallback: same decade
    if len(candidates) < n + 1:
        decade = (anchor_year // 10) * 10
        candidates = df[
            (df["year"] >= decade) &
            (df["year"] < decade + 10) &
            (df["popularity"] >= 15)
        ]

    if candidates.empty:
        return "No suitable candidates found."

    cand_idx = candidates.index
    cand_vecs = X_scaled[cand_idx]

    distances = cdist(anchor_vec, cand_vecs, metric="cosine")[0]
    results = candidates.copy()
    results["distance"] = distances

    return (
        results
        .sort_values("distance")
        .iloc[1:n+1][["name", "artists", "year", "popularity"]]
    )
