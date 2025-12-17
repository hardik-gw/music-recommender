🎧 Music Recommendation System (Content-Based)

A production-style content-based music recommender system that suggests similar songs using audio features, while explicitly handling real-world challenges such as dataset bias, song name ambiguity, covers/remixes, and API limitations.

This project prioritizes engineering realism over model complexity.
Overview

Music recommendation systems aim to personalize listening experiences by suggesting tracks aligned with a user’s taste.

This project implements a content-based recommender using:

Precomputed Spotify audio features (offline)

Live song discovery and metadata resolution via the Last.fm API

Unlike notebook-only demos, this system is designed with:

Offline feature storage

Runtime inference only (no retraining)

Robust input normalization

Explicit candidate filtering for better recommendation quality

 Key Features

Content-based recommendations using cosine similarity

Offline feature scaling and artifact storage

Live song resolution via Last.fm API

Robust handling of:

Song name ambiguity (e.g., “Change”, “Home”)

Covers, remixes, and live versions

Inconsistent or incorrect artist metadata

Era-aware and popularity-aware candidate filtering

CLI-based interactive interface

 System Architecture
User Input (Song Name)
        ↓
Last.fm API
(Song Search + Tags)
        ↓
Anchor Song Resolution
(Normalization + Fallbacks)
        ↓
Offline Feature Store
(Spotify Audio Features)
        ↓
Candidate Filtering
(Era + Popularity + Bias)
        ↓
Cosine Similarity Ranking
        ↓
Top-N Recommendations


 Dataset

Source: Spotify Audio Features Dataset (Kaggle)

Granularity: One row per track

Key features used:

danceability

energy

loudness

speechiness

acousticness

instrumentalness

liveness

valence

tempo

popularity

duration_ms

explicit

All audio features are precomputed and stored locally, mirroring how real-world systems rely on internal feature stores.

⚙️ How It Works
1️⃣ Offline Training (One-Time)

Load dataset

Select numerical audio features

Normalize features

Serialize scaled feature matrix

python model/train.py

2️⃣ Live Song Discovery

User enters a song name

Last.fm API resolves:

Canonical song title

Artist name

Optional genre / mood tags

Spotify API is intentionally not used for live audio features due to endpoint restrictions for new developer apps.

3️⃣ Anchor Resolution (Critical Step)

To avoid incorrect recommendations, the system:

Normalizes song titles (removes “cover”, “remix”, etc.)

Prioritizes exact song + artist matches

Falls back to modern, popular matches when ambiguous

Avoids anchoring to archival or incorrect tracks

4️⃣ Recommendation

Candidate pool is filtered before similarity computation:

Similar era (± 5 years)

Minimum popularity threshold

Cosine similarity is computed within the filtered pool

Top-N recommendations are returned

 Running the Project
Install dependencies
pip install -r requirements.txt

Train the model
python model/train.py

Start the recommender
python main.py


Example session:

Enter a song: Change j cole

Because you liked Change by J. Cole:
Tags: rap, hip-hop, 2016

Recommendations:
- Kendrick Lamar – ...
- J. Cole – ...
- Travis Scott – ...

 Why Last.fm Instead of Spotify API?

Spotify restricts access to the audio-features endpoint for many new developer applications.

To ensure reliability:

Spotify audio features are used offline via dataset

Last.fm API is used for live song discovery and metadata

Recommendation logic remains independent of external APIs

This mirrors industry practice, where features are computed offline and served from internal systems.

 Design Decisions

✔ Offline feature store instead of live feature extraction

✔ Explicit candidate filtering before similarity

✔ Robust normalization for real-world user inputs

✔ Focus on recommendation quality over complex models

❌ No collaborative filtering (no user history available)

⚠️ Limitations

Recommendations limited to tracks present in the dataset

No user-specific personalization

Genre inference relies on heuristic signals

🚧 Future Improvements

Genre-aware weighting using tags

Playlist-based recommendations

Artist-centric similarity mode

Web interface using Streamlit or FastAPI

Hybrid recommender (content + collaborative)

🛠️ Tech Stack

Python

Pandas, NumPy

Scikit-learn

SciPy

Last.fm API (pylast)


📌 Final Note

This project emphasizes system design, robustness, and realistic constraints over model complexity — reflecting how real-world recommendation systems are engineered and deployed.
