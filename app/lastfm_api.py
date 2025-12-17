import pylast

# ----------------------------------------
# Last.fm API setup
# ----------------------------------------
API_KEY = "a9101c394ccb6ccc58b3055e034e8077"

network = pylast.LastFMNetwork(api_key=API_KEY)

def search_track(song_name):
    """
    Search Last.fm for a track and return name + artist.
    """
    results = network.search_for_track("", song_name).get_next_page()

    if not results:
        return None

    track = results[0]
    return {
        "name": track.title,
        "artist": track.artist.name
    }


def get_track_tags(song_name, artist_name):
    """
    Fetch top tags (genres/moods) for a track.
    """
    try:
        track = network.get_track(artist_name, song_name)
        tags = track.get_top_tags(limit=5)
        return [tag.item.name for tag in tags]
    except:
        return []
if __name__ == "__main__":
    song = search_track("Blinding Lights")
    print(song)

    tags = get_track_tags(song["name"], song["artist"])
    print("Tags:", tags)
