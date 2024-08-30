import requests

import os

from .album import Album
from .playlist import Playlist
from .song import Song
from .logging_config import main_logger as logger
from .error import SoundChartsError


def get_soundcharts_error_code_message(response: dict):
    error = response.get("errors")[0]
    code = error.get("code")
    message = error.get("message")
    return code, message


def check_response_for_errors(response: dict):

    if response.get("errors"):
        code, message = get_soundcharts_error_code_message(response=response)
        output_message = f"SoundCharts Error {code} - {message}"
        raise SoundChartsError(output_message)

    return response


class SoundCharts:
    def __init__(self, app_id: str, api_key: str):
        self.app_id = app_id
        self.api_key = api_key
        self.base_api_url = "https://customer.api.soundcharts.com/api"

    def get_credentials(self):
        credentials = {
            "x-app-id": self.app_id,
            "x-api-key": self.api_key
        }
        return credentials

    def make_api_request(self, add_to_base_url) -> [dict, list]:
        """
        Method to make api requests, adds the required auth headers.
        :param add_to_base_url:
        :return response.json():
        """
        try:
            url = self.base_api_url + add_to_base_url
            response: requests.Response = requests.get(
                url=url,
                headers=self.get_credentials()
            )
            response_dict: dict = response.json()
            response_dict = check_response_for_errors(response=response_dict)
            return response_dict
        except SoundChartsError as e:
            logger.error(f"{e}")
            raise e

    # Artist methods
    def get_artist_follower_count_from_uuid(self, artist_uuid: str, platform: str) -> int:
        """
        Gets the follower count for an artist uuid on a given platform.
        :param artist_uuid:
        :param platform:
        :return follower_count:
        """
        response: dict = self.make_api_request("/v2/artist/{}/audience/{}/"
                                               .format(artist_uuid, platform))
        items = response.get("items")
        follower_count = items[0]["followerCount"]
        return follower_count

    # Playlist Methods
    def get_playlist_metadata_from_uuid(self, uuid: str) -> Playlist:
        """
        Returns a playlist object with methods to access metadata.
        :param uuid:
        :return:
        """
        response: dict = self.make_api_request("/v2.8/playlist/{}"
                                               .format(uuid))
        response: dict = response.get("object")
        playlist: Playlist = Playlist(**response)
        return playlist

    # Song Methods
    def get_song_metadata_from_uuid(self, song_uuid: str) -> Song:
        """
        Returns a song object with methods to access song metadata.
        :param song_uuid:
        :return song:
        """
        response: dict = self.make_api_request("/v2.25/song/{}"
                                               .format(song_uuid))
        response: dict = response.get("object")
        song: Song = Song(**response)
        return song

    def get_song_metadata_from_isrc(self, isrc: str) -> Song:
        """
        Returns a song object with methods to access song metadata.
        :param isrc:
        :return song:
        """
        response: dict = self.make_api_request("/v2.25/song/by-isrc/{}"
                                               .format(isrc))
        response: dict = response.get("object")
        song: Song = Song(**response)
        return song

    def get_song_by_platform_id(self, platform: str, platform_id: str) -> Song:
        """
        Returns a song object with methods to access song metadata.
        :param platform:
        :param platform_id:
        :return song:
        """
        response: dict = self.make_api_request("/v2.25/song/by-platform/{}/{}"
                                               .format(platform, platform_id))
        response: dict = response.get("object")
        song: Song = Song(**response)
        return song

    def get_song_platform_ids(self, song_uuid: str, offset: int, limit: int) -> list:
        """
        Returns a list of dictionaries in the format:
            {
          "platformName": "Amazon",
          "platformCode": "amazon",
          "identifier": "B07N856BC2",
          "url": "https://music.amazon.es/albums/?trackAsin=B07N856BC2",
          "default": false
        }
        :param song_uuid:
        :param offset:
        :param limit:
        :return [{}, {}, ...]:
        """

        response: dict = self.make_api_request(
            "/v2/song/{}/identifiers?offset={}&limit={}"
            .format(song_uuid, offset, limit))
        items: list[dict] = response.get("items")
        return items

    def get_song_albums(self, song_uuid: str, type: str, offset: int, limit: int, sort_by: str, sort_order: str) -> \
            list[Album]:
        """
        Returns a list of song album objects containing metadata about the albums.

        :param song_uuid: The UUID of the song.
        :param type: The type of albums to retrieve. Possible values are 'all', 'album', 'single', 'compil'.
        :param offset: Get results starting from.
        :param limit: The limit for pagination. Max(100)
        :param sort_by: The field to sort by. Possible values are "title", "releaseDate"
        :param sort_order: The order to sort by (e.g., 'asc' or 'desc').
        :return: A list of Album objects.
        """
        response: dict = self.make_api_request("/v2/song/{}/albums?type={}&offset={}&limit={}&sortBy={}&sortOrder={}"
                                               .format(song_uuid, type, offset, limit, sort_by, sort_order))
        items = response.get("items")
        albums = [Album(**item) for item in items]
        return albums

    def get_song_audience(self, song_uuid: str, platform: str, start_date: str = None, end_date: str = None,
                          identifier: str = None) -> list[dict]:
        """
        Returns a list of dictionaries containing audience data for a song on a given platform.
        :param song_uuid: The UUID of the song.
        :param platform: The platform to get audience data for.
        :param start_date: Date in the format "YYYY-MM-DD"
        :param end_date: Date in the format "YYYY-MM-DD"
        :param identifier: An optional identifier for the song on the platform.
        :return output: A list of dictionaries containing audience data.
        Example output:
        [
            {
                "platform": "spotify",
                "audience": "monthly",
                "date": "2021-07-01",
                "identifier": "6f3e3c6f-7f0b-4f7e-8b3d-3f0e2f0f9b3d",
                "value": 0
            },
            {
                "platform": "spotify",
                "audience": "monthly",
                "date": "2021-07-02",
                "identifier": "6f3e3c6f-7f0b-4f7e-8b3d-3f0e2f0f9b3d",
                "value": 0
            }
        ]
        """
        url = "/v2/song/{}/audience/{}?".format(song_uuid, platform)

        if start_date:
            url += "startDate={}".format(start_date)

        if end_date:
            if start_date:
                url += "&"

            url += "endDate={}".format(end_date)

        if identifier:
            if start_date or end_date:
                url += "&"

            url += "identifier={}".format(identifier)

        response: dict = self.make_api_request(url)
        items = response.get("items")
        output: list = []

        for item in items:
            plots = item.get("plots")
            value = plots[0].get("value")
            identifier_string = item.get("identifier")

            new_dict = {
                "platform": platform,
                "audience": item.get("audience"),
                "date": item.get("date"),
                "identifier": identifier_string,
                "value": value
            }
            output.append(new_dict)

        return output


