import requests

import os
from .error import SoundChartsError
from .playlist import Playlist
from .song import Song
from .logging_config import main_logger as logger


def get_credentials():
    credentials = {
        "x-app-id": os.getenv("SOUNDCHARTS_APP_ID"),
        "x-api-key": os.getenv("SOUNDCHARTS_API_KEY")
    }
    return credentials


def get_soundcharts_error_code_message(response: dict):
    error = response.get("errors")[0]
    code = error.get("code")
    message = error.get("message")
    return code, message


def make_api_request(add_to_base_url, base_a=None) -> [dict, list]:
    """
    Method to make api requests, adds the required auth headers.
    :param add_to_base_url:
    :return response.json():
    """
    try:
        base_api_url = "https://api.soundcharts.com"
        url = base_api_url + add_to_base_url
        response: requests.Response = requests.get(
            url=url,
            headers=get_credentials()
        )
        response_dict: dict = response.json()
        return response_dict
    except Exception as e:
        logger.error(f"Error: {e}")


def process_soundcharts_response(response: dict, requirement: str = None):
    if requirement and response.get(requirement) is None:
        code, message = get_soundcharts_error_code_message(response=response)
        output_message = f"SoundCharts Error {code} - {message}"
        raise SoundChartsError(output_message)

    return response


def get_song_metadata_from_uuid(self, uuid: str) -> Song:
    """
    Returns a song object with methods to access song metadata.
    :param uuid:
    :return song:
    """
    try:
        response: dict = self.make_api_request(self.base_api_url + "/v2.25/song/" + uuid)
        response = process_soundcharts_response(response=response, requirement="object")
        response: dict = response.get("object")
        song: Song = Song(**response)
        return song
    except SoundChartsError as e:
        logger.error(e)


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
        response = process_soundcharts_response(response=response, requirement="items")
        items = response.get("items")
        main_artist = items[0]
        follower_count = main_artist["followerCount"]
        return follower_count
    except SoundChartsError as e:
        logger.error(e)


def get_playlist_metadata_from_uuid(self, uuid: str) -> Playlist:
    """
    Returns a playlist object with methods to access metadata.
    :param uuid:
    :return:
    """
    try:
        response: dict = self.make_api_request(self.base_api_url + "/v2.8/playlist/" + uuid)
        response = process_soundcharts_response(response=response, requirement="object")
        response: dict = response.get("object")
        playlist: Playlist = Playlist(**response)
        return playlist
    except SoundChartsError as e:
        logger.error(e)
