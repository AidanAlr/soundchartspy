from types import SimpleNamespace

import requests

from src.soundchartspy.playlist import Playlist
from src.soundchartspy.song import Song
from src.soundchartspy.logging_config import main_logger as logger
import numpy as np


def create_credentials(app_id: str, api_key: str):
    credentials = {
        "x-app-id": app_id,
        "x-api-key": api_key
    }
    return credentials


def process_soundcharts_error(error_message):
    error = error_message.get("errors")[0]
    code = error.get("code")
    message = error.get("message")

    output_message = f"SoundCharts Error {code} - {message}"

    return output_message


class SoundCharts:
    def __init__(self, app_id: str, api_key: str):
        self.app_id: str = app_id
        self.api_key: str = api_key
        self.credentials: dict = create_credentials(app_id, api_key)
        self.base_api_url: str = "https://customer.api.soundcharts.com/api"

    def make_api_request(self, url) -> [dict, list]:
        """
        Method to make api requests, adds the required auth headers.
        :param url:
        :return response.json():
        """
        try:
            response: requests.Response = requests.get(
                url=url,
                headers=self.credentials
            )
            response_dict: dict = response.json()
            return response_dict
        except Exception as e:
            logger.error(f"Error: {e}")

    def get_song_metadata_from_uuid(self, uuid: str) -> Song:
        """
        Returns a song object with methods to access song metadata.
        :param uuid:
        :return song:
        """
        try:
            response: dict = self.make_api_request(self.base_api_url + "/v2.25/song/" + uuid)
            song: Song = Song(**response.get("object"))
            return song
        except Exception as e:
            logger.error(f"Error: {e}")
            return e

    def get_artist_follower_count_from_uuid(self, artist_uuid: str, platform: str) -> int:
        """
        Gets the follower count for an artist uuid on a given platform.
        :param artist_uuid:
        :param platform:
        :return follower_count:
        """
        try:
            response: dict = self.make_api_request(
                self.base_api_url + "/v2/artist/" + artist_uuid + "/audience/" + platform)
            items = response["items"]
            logger.debug(items)
            main_artist = items[0]
            follower_count = main_artist["followerCount"]
            return follower_count
        except KeyError:
            logger.error(process_soundcharts_error(response))
            return None

    def get_playlist_metadata_from_uuid(self, uuid: str) -> Playlist:
        """
        Returns a playlist object with methods to access metadata.
        :param uuid:
        :return:
        """
        try:
            response: dict = self.make_api_request(self.base_api_url + "/v2.8/playlist/" + uuid)
            playlist: Playlist = Playlist(**response["object"])
            logger.debug(playlist)
            return playlist
        except Exception as e:
            logger.error(process_soundcharts_error(response))



