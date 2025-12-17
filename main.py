from app.lastfm_api import search_track, get_track_tags
from app.recommender import recommend_from_song

while True:
    query = input("\nEnter a song (or exit): ").strip()
    if query.lower() == "exit":
        break

    track = search_track(query)
    if not track:
        print("Song not found.")
        continue

    print(f"\nBecause you liked {track['name']} by {track['artist']}:")
    tags = get_track_tags(track["name"], track["artist"])
    if tags:
        print("Tags:", ", ".join(tags))

    print("\nRecommendations:")
    print(recommend_from_song(track["name"], track["artist"], n=10))
