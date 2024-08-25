from types import SimpleNamespace

import requests

from src.soundchartspy.song import Song
from src.soundchartspy.logging_config import main_logger as logger

def create_credentials(app_id: str, api_key: str):
    credentials = {
        "x-app-id": app_id,
        "x-api-key": api_key
    }
    return credentials


class SoundCharts:
    def __init__(self, app_id: str, api_key: str):
        self.app_id: str = app_id
        self.api_key: str = api_key
        self.credentials: dict = create_credentials(app_id, api_key)
        self.base_api_url: str = "https://customer.api.soundcharts.com/api"

    def get_song_metadata_from_uuid(self, uuid: str) -> SimpleNamespace:
        """
        Returns an object containing the attributes of the requested song
        :param uuid:
        :return:
        """
        try:
            response: requests.Response = requests.get(
                self.base_api_url + "/v2.25/song/" + uuid,
                headers=self.credentials
            )
            song: Song = Song(**response.json().get("object"))

            return song

        except Exception as e:
            logger.error(f"Error: {e}")
            return e
