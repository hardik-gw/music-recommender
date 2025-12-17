 Music Recommendation System (Content-Based)


A production-style content-based music recommender system that suggests similar songs based on audio features, while handling real-world issues such as dataset bias, song name ambiguity, covers/remixes, and API limitations.
This project focuses on engineering realism over model complexity.
 Overview
Music recommendation systems aim to personalize listening experiences by suggesting tracks that align with a user’s taste.

This project implements a content-based recommender using precomputed Spotify audio features, combined with live song discovery via the Last.fm API.
Unlike simple notebook demos, this system is designed with:

offline feature storage
runtime inference only (no retraining)
robust input handling
realistic filtering logic


 Key Features
Content-based recommendations using cosine similarity
Offline feature scaling and artifact storage
Live song resolution using Last.fm API
Robust handling of:
song name ambiguity (e.g., “Change”, “Home”)
covers / remixes / live versions
wrong or inconsistent artist metadata
Era-aware and popularity-aware recommendation filtering
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
Offline Feature Store (Spotify audio features)
        ↓
Candidate Filtering
(era + popularity + bias)
        ↓
Cosine Similarity Ranking
        ↓Top-N Recommendations


Project Structure

spotify-recommender/
│
├── data/
│   └── data.csv              # Spotify audio feature dataset
│
├── model/
│   ├── train.py              # Offline training script
│   └── artifacts.pkl         # Saved feature matrix
│
├── app/
│   ├── lastfm_api.py         # Live song discovery (Last.fm)
│   └── recommender.py        # Recommendation logic
│
├── main.py                   # CLI entry point
├── requirements.txt
└── README.md


Dataset
Source: Spotify audio feature dataset (Kaggle)
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
All audio features are precomputed and stored locally, mimicking how real systems use feature stores.


How It Works
1️⃣ Offline Training (One-Time)
Load dataset
Select numerical audio features
Normalize features
Save scaled feature matrix to disk

python model/train.py
2️⃣ Live Song Discovery
User enters a song name
Last.fm API resolves:
canonical song title
artist name
optional genre / mood tags
Spotify API was intentionally not used for audio features due to endpoint restrictions for new apps.
3️⃣ Anchor Resolution (Critical Step)
To avoid incorrect recommendations, the system:

normalizes song titles (removes “cover”, “remix”, etc.)
prioritizes song + artist matches
falls back to modern, popular matches
avoids anchoring to archival or ambiguous tracks
4️⃣ Recommendation
Candidate pool is filtered before similarity
similar era (± 5 years)
minimum popularity threshold
Cosine similarity is computed within the filtered pool
Top-N recommendations are returned


Running the Project
Install dependencies

pip install -r requirements.txt
Train the model

python model/train.py
Start the recommender

python main.py




Why Last.fm Instead of Spotify API?
Spotify has restricted access to the audio-features endpoint for many new developer apps.

To ensure reliability and realism:
Spotify audio features are used offline via dataset
Last.fm API is used for live song discovery and metadata
Recommendation logic is fully independent of external APIs
This mirrors industry practice, where features are computed offline and served from internal stores.


 Design Decisions
✔ Offline feature store instead of live feature extraction
✔ Explicit candidate filtering before similarity
✔ Robust normalization for real-world inputs
✔ Focus on recommendation quality, not flashy models
 No collaborative filtering (no user history available)
⚠️ Limitations
Recommendations limited to tracks present in the dataset
No user-specific personalization
Genre inference relies on heuristic signals
🚧 Future Improvements
Genre-aware weighting using tags
Playlist-based recommendations
Artist-centric similarity mode
Web interface using Streamlit or FastAPI


Tech Stack
Python
Pandas, NumPy
Scikit-learn
SciPy
Last.fm API (pylast)


Final note
This project prioritizes engineering realism and system design over model complexity — reflecting how real recommendation systems are built and deployed.
