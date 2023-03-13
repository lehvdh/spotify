import base64
from abc import ABC

import requests


class SpotifyConnector(ABC):
    @staticmethod
    def get_access_token(client_id: str, client_secret: str) -> str:
        """
        param: client_id
        param: client_secret
        """
        auth_url = "https://accounts.spotify.com/api/token"
        auth_header = {}
        auth_data = {}

        message = f"{client_id}:{client_secret}"
        base64_message = base64.b64encode(message.encode("ascii")).decode("ascii")

        auth_header["Authorization"] = "Basic " + base64_message
        auth_data["grant_type"] = "client_credentials"
        response = requests.post(
            auth_url, headers=auth_header, data=auth_data, timeout=2
        ).json()

        return response["access_token"]


class SpotifyService(ABC):
    def __init__(self, token: str):
        self.headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + token,
        }

    def create_playlist(
        self, user_id: str, name: str, description: str, public: bool
    ) -> None:
        """
        param: user_id
        param: name
        param: description
        """
        endpoint = f"https://api.spotify.com/v1/users/{user_id}/playlists"

        data = {"name": name, "description": description, "public": public}

        return requests.post(
            endpoint, headers=self.headers, data=data, timeout=2
        ).json()

    def change_playlist_details(self, playlist_id: str, public: bool):
        """
        param: playlist_id
        param: public
        """
        endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}"

        data = {"public": public}

        return requests.put(endpoint, headers=self.headers, data=data, timeout=2).json()

    def get_playlist_ids(self, playlist_ids: list) -> list:
        """
        param: playlists_ids
        """
        ids = []
        for id in playlist_ids:
            endpoint = f"https://api.spotify.com/v1/playlists/{id}"
            ids.append(
                requests.get(endpoint, headers=self.headers, timeout=2).json()["id"]
            )

        return ids

    def get_playlist_track_uris(self, playlist_ids: list, limit: int) -> list:
        """
        param: playlist_ids
        param: limit
        """
        items = []
        for id in playlist_ids:
            endpoint = (
                f"https://api.spotify.com/v1/playlists/{id}/tracks?&limit={limit}"
            )
            for item in requests.get(endpoint, headers=self.headers, timeout=2).json()[
                "items"
            ]:
                items.append(item["track"]["uri"])

        return items

    def get_recommendations(self, uris: list, limit: int) -> list:
        """
        param: seeds_tracks
        """
        seed_tracks = [x.replace("spotify:track:", "") for x in uris]
        recommendations = []
        for track in seed_tracks:
            endpoint = (
                f"https://api.spotify.com/v1/recommendations?"
                f"&seed_tracks={ track.replace('spotify:track:', '')}&limit={limit}"
            )
            recommendations.append(
                requests.get(endpoint, headers=self.headers, timeout=2).json()
            )

        return recommendations

    def add_tracks_to_playlist(self, playlist_id: str, uris: list) -> None:
        """
        param: playlist_id
        param: spotify_uris
        """

        endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

        data = {"uris": uris, "position": 0}

        requests.post(endpoint, headers=self.headers, data=data, timeout=2).json()
