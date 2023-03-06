import json
import os

from spotify_service import SpotifyConnector, SpotifyService

playlist_ids = [
    # "2G7UUHsjDigOjcEBPgE5NI?si=0953a39f2c5e4b78",
    "6GGW4uy8PVDK7qHUOseF1L?si=4f124ee0fdf24fd1",
]
user_id = "1138730147"

access_token = SpotifyConnector.get_access_token(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
)

instance = SpotifyService(access_token)

playlist_ids = instance.get_playlist_ids(playlist_ids=playlist_ids)
uris = instance.get_playlist_track_uris(playlist_ids=playlist_ids, limit=5)
recommendations = instance.get_recommendations(seed_tracks=uris[0:5])
instance.change_playlist_details(playlist_id=playlist_ids[0], public=False)
instance.add_tracks_to_playlist(playlist_id=playlist_ids[0], uris=uris)

print(json.dumps(uris))

# instance.create_public_playlist(user_id, "test", "test")

# Get tracks from playlists ABC - Get Tracks based on playlist D
# Add tracks to playlist D
# Move tracks from playlist D to Archive
