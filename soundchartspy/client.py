import logging

import requests
from requests import Response

from soundchartspy.data import Song
from soundchartspy.utils import check_response_for_errors_and_convert_to_dict, convert_song_response_to_object

logger = logging.getLogger(__name__)


class SoundCharts:

    def __init__(self, app_id: str, api_key: str):
        self._app_id = app_id
        self._api_key = api_key

    def _get_credentials(self):
        credentials = {
            "x-app-id": self._app_id,
            "x-api-key": self._api_key
        }
        return credentials

    def _make_api_get_request(self, append_to_base_url: str):
        """
        Takes an additional url to append to the base url and make a get request with the required credentials
        :param self:
        :param append_to_base_url:
        :return:
        """
        base_url: str = "https://customer.api.soundcharts.com"
        url: str = base_url + append_to_base_url
        response: Response = requests.get(url, headers=self._get_credentials())
        response: dict = check_response_for_errors_and_convert_to_dict(response=response)
        logger.debug("GET request to {}".format(url))
        return response

    def song(self, uuid: str):
        append_to_base_url: str = f"/api/v2.25/song/{uuid}"
        response: dict = self._make_api_get_request(append_to_base_url=append_to_base_url)
        song: Song = convert_song_response_to_object(response)
        return song

    def song_by_isrc(self, isrc: str):
        append_to_base_url: str = f"/api/v2.25/song/by-isrc/{isrc}"
        response: dict = self._make_api_get_request(append_to_base_url=append_to_base_url)
        song: Song = convert_song_response_to_object(response)
        return song

    def song_by_platform_id(self, platform: str, identifier: str):
        append_to_base_url: str = f"/api/v2.25/song/by-platform/{platform}/{identifier}"
        response: dict = self._make_api_get_request(append_to_base_url=append_to_base_url)
        song: Song = convert_song_response_to_object(response)
        return song
