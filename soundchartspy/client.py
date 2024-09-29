import logging

import requests
from requests import Response

from soundchartspy.data import Song, PlatformIdentifier, Album
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
        # Base url for the SoundCharts API
        base_url: str = "https://customer.api.soundcharts.com"
        # Append the additional url to the base url
        url: str = base_url + append_to_base_url

        # Make the get request with the required credentials
        response: Response = requests.get(url, headers=self._get_credentials())
        # Check the response for errors and convert it to a dictionary
        response: dict = check_response_for_errors_and_convert_to_dict(response=response)
        logger.debug("GET request to {}".format(url))
        return response

    def song(self, uuid: str) -> Song:
        """
        Get a song by its SoundCharts uuid.
        :param uuid:
        :return song:
        """
        endpoint: str = f"/api/v2.25/song/{uuid}"
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)

        song: Song = convert_song_response_to_object(response)
        return song

    def song_by_isrc(self, isrc: str) -> Song:
        """
        Get a song by its ISRC.
        :param isrc:
        :return song:
        """
        endpoint: str = f"/api/v2.25/song/by-isrc/{isrc}"
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        song: Song = convert_song_response_to_object(response)
        return song

    def song_by_platform_id(self, platform: str, identifier: str) -> Song:
        """
        Get a song by its platform and identifier.
        :param platform:
        :param identifier:
        :return song:
        """
        endpoint: str = f"/api/v2.25/song/by-platform/{platform}/{identifier}"
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        song: Song = convert_song_response_to_object(response)
        return song

    def song_ids(self, uuid: str, platform: str = None, offset: int = 0, limit: int = 100) -> list[PlatformIdentifier]:
        """
        Get the identifiers for a song by its SoundCharts uuid. Returns a list of PlatformIdentifier objects.
        :param uuid:
        :param platform:
        :param offset:
        :param limit:
        :return platform_identifiers:
        """
        endpoint = f"/api/v2/song/{uuid}/identifiers?offset={offset}&limit={limit}"
        if platform:
            endpoint: str = f"/api/v2/song/{uuid}/identifiers?platform={platform}&offset={offset}&limit={limit}"
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        items: list = response.get("items")
        platform_identifiers = [PlatformIdentifier(**item) for item in items]
        return platform_identifiers

    def song_albums(self, uuid: str, type: str = "all", offset: int = 0,
                    limit: int = 100, sort_by: str = "title", sort_order: str = "asc") -> list:
        """
        Retrieve albums associated with a specific song.

        This function fetches a list of albums related to a given song, identified by its UUID.
        The results can be filtered, sorted, and paginated using various parameters.

        :param uuid: A string representing the UUID of the song (required).
        :param type: A string to filter the album list. Available values are:
                     'all', 'album', 'single', 'compil'. Defaults to 'all'.
        :param offset: An integer specifying the starting position of results. Defaults to 0.
        :param limit: An integer specifying the number of results to return (max. 100). Defaults to 100.
        :param sort_by: A string specifying the sort criteria. Available values are:
                        'title', 'releaseDate'. Defaults to 'title'.
        :param sort_order: A string specifying the sort order. Available values are:
                           'asc' (ascending), 'desc' (descending). Defaults to 'asc'.

        :return: A list of Album objects representing the albums associated with the song.

        :raises: May raise exceptions related to API requests (e.g., connection errors, authentication issues).

        Example usage:
            albums = soundcharts.song_albums(uuid="1234567890", type="album", limit=50, sort_by="releaseDate", sort_order="desc")
        """
        endpoint = f"/api/v2/song/{uuid}/albums?type={type}&offset={offset}&limit={limit}&sort_by={sort_by}&sort_order={sort_order}"
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        items: list = response.get("items")
        albums = [Album(**item) for item in items]
        return albums

    def song_audience(self, uuid: str, platform: str, start_date: str = None, end_date: str = None,
                      identifier: str = None) -> dict:
        """
        Retrieve audience data for a specific song on a given platform.

        This method fetches audience data for a song, identified by its UUID, on a specified platform
        using the SoundCharts API.

        :param self: The instance of the SoundCharts class.
        :param uuid: A string representing the UUID of the song (required).
        :param platform: A string representing the platform code (required).
        :param start_date: An optional string representing the start date of the period to fetch data for.
                           Format should be 'YYYY-MM-DD'. If provided, the period cannot exceed 90 days.
        :param end_date: An optional string representing the end date of the period to fetch data for.
                         Format should be 'YYYY-MM-DD'. If not provided, the latest 90 days will be used.
        :param identifier: An optional string representing a specific song identifier
                           (e.g., '2Fxmhks0bxGSBdJ92vM42m').

        :return: A dictionary containing the audience data items for the specified song and platform.

        :raises: May raise exceptions related to API requests (e.g., connection errors, authentication issues).

        Note:
        - If both start_date and end_date are provided, the period between them cannot exceed 90 days.
        - If end_date is not provided, the method will return data for the latest 90 days from the start_date,
          or from the current date if start_date is also not provided.

        Example usage:
            audience_data = soundcharts.song_audience(uuid="1234567890", platform="spotify",
                                                      start_date="2023-01-01", end_date="2023-03-31",
                                                      identifier="2Fxmhks0bxGSBdJ92vM42m")
        """
        endpoint = f"/api/v2/song/{uuid}/audience/{platform}?start_date={start_date}&end_date={end_date}"
        if identifier:
            endpoint += f"&identifier={identifier}"

        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        items = response.get("items")
        return items
