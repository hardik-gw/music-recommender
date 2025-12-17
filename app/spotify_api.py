import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = "1a278f62915341699925be514508d285"
CLIENT_SECRET = "1085085c44574830a97f0e342ef55720"

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
)

def search_track(song_name):
    """
    Search Spotify and return track name + artist.
    """
    results = sp.search(q=song_name, limit=1, type="track")
    if not results["tracks"]["items"]:
        return None

    track = results["tracks"]["items"][0]
    return {
        "name": track["name"],
        "artist": track["artists"][0]["name"]
    }


if __name__ == "__main__":
    print(search_track("Blinding Lights"))
