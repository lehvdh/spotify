import json
import os

from spotify_service import SpotifyConnector, SpotifyService

playlist_ids = [
    # "2G7UUHsjDigOjcEBPgE5NI?si=0953a39f2c5e4b78", # zweven blijf je leven
    "6GGW4uy8PVDK7qHUOseF1L?si=4f124ee0fdf24fd1",  # test
]
user_id = "1138730147"  # Lucas id

access_token = SpotifyConnector.get_access_token(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
)

instance = SpotifyService(access_token)

ids = instance.get_playlist_ids(playlist_ids=playlist_ids)
uris = instance.get_playlist_track_uris(playlist_ids=ids, limit=5)
recommendations = instance.get_recommendations(uris=uris, limit=1)
# instance.change_playlist_details(playlist_id=ids[0], public=False)
uris_to_add = []
for recommended_tracks in recommendations:
    for track in recommended_tracks["tracks"]:
        uris_to_add.append(track["uri"])
instance.add_tracks_to_playlist(playlist_id=ids[0], uris=uris_to_add)

print(json.dumps(uris))

# instance.create_public_playlist(user_id, "test", "test")

# Get tracks from playlists ABC - Get Tracks based on playlist D
# Add tracks to playlist D
# Move tracks from playlist D to Archive
