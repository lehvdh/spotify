import json
import os

from spotify_service import SpotifyService
from spotify_connector import SpotifyConnector

#playlist_id =  "2G7UUHsjDigOjcEBPgE5NI?si=0953a39f2c5e4b78" # zweven blijf je leven
playlist_id = "6GGW4uy8PVDK7qHUOseF1L?si=4f124ee0fdf24fd1"  # test

user_id = "1138730147"  # Lucas id

access_token = SpotifyConnector.get_access_token(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
)

instance = SpotifyService(access_token)

# create playlist
#playlist_new = instance.create_playlist(user_id, "Hallo", "Hallo", False)
playlist = instance.get_playlist(playlist_id=playlist_id)
track_ids = instance.get_playlist_info(
    playlist=playlist, 
    limit=1,
    info_type="id",
)
track_artists = instance.get_playlist_info(
    playlist=playlist, 
    limit=1,
    info_type="artists",
    extra_info="id"
)
genres = instance.get_available_genres()
#audio_analysis = instance.get_track_audio_analysis(id=track_ids[0])
recommendations = instance.get_recommendations(
    seed_artists=track_artists[0],
    seed_genres="edm,deep-house,dance,techno,trance",
    seed_tracks=track_ids[0], 
    limit=1,
)
# Add track to archive
# Replace track from playlist with recommendation
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
