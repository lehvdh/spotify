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
