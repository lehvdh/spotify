from abc import ABC

import requests


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

        response = requests.post(
            endpoint, headers=self.headers, json=data, timeout=2
        )
        return response.json()

    def change_playlist_details(self, playlist_id: str, public: bool):
        """
        param: playlist_id
        param: public
        """
        endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}"

        data = {"public": public}

        return requests.put(endpoint, headers=self.headers, json=data, timeout=2).json()

    def get_playlist(self, playlist_id: str) -> list:
        """
        param: playlists_id
        """
        return requests.get(
                f"https://api.spotify.com/v1/playlists/{playlist_id}", 
                headers=self.headers, 
                timeout=2
            ).json()

    
    def get_playlist_info(self, playlist, info_type, limit, extra_info=None):
        ls = []
        for item in playlist["tracks"]["items"][0:limit]:
            item_to_add = item["track"][info_type][0][extra_info] if extra_info else item["track"][info_type]
            ls.append(item_to_add)
        
        return ls

    def get_available_genres(self):
        endpoint = (
           "https://api.spotify.com/v1/recommendations/available-genre-seeds"
        )
        return requests.get(endpoint, headers=self.headers, timeout=2).json()

    # def get_track_audio_analysis(self, id: str):
    #     return requests.get(
    #             f"https://api.spotify.com/v1/audio-analysis/{id}",
    #             headers=self.headers, 
    #             timeout=2
    #         ).json()

    def get_recommendations(self, seed_artists: list, seed_genres: list, seed_tracks: list, limit: int) -> list:
        """
        param: seed_artists
        param: seed_tracks
        param: seed_genres
        param: limit
        """
        endpoint = (
           f"https://api.spotify.com/v1/recommendations?"
           f"&seed_artists={seed_artists}&seed_genres={seed_genres}&seed_tracks={seed_tracks}&limit={limit}"
        )
        return requests.get(endpoint, headers=self.headers, timeout=2).json()


    def add_tracks_to_playlist(self, playlist_id: str, uris: list) -> None:
        """
        param: playlist_id
        param: spotify_uris
        """

        endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

        data = {"uris": uris, "position": 0}

        requests.put(endpoint, headers=self.headers, json=data, timeout=2).json()

    def update_playlist_items(self, playlist_id: str, uris: list) -> None:
        """
        param: playlist_id
        param: uris
        """
        endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

        data = {"uris": uris, "position": 0}

        requests.put(endpoint, headers=self.headers, data=data, timeout=2).json()