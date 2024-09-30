import logging
import requests
from requests import Response

from soundchartspy.data import Song, PlatformIdentifier, Album
from soundchartspy.utils import check_response_for_errors_and_convert_to_dict, convert_song_response_to_object

logger = logging.getLogger(__name__)


class SoundCharts:

    def __init__(self, app_id: str, api_key: str):
        """
        Initialize the SoundCharts client.

        Args:
            app_id (str): Your SoundCharts app ID.
            api_key (str): Your SoundCharts API key.
        """
        self._app_id = app_id
        self._api_key = api_key

    def _get_credentials(self):
        credentials = {
            "x-app-id": self._app_id,
            "x-api-key": self._api_key
        }
        return credentials

    def _make_api_get_request(self, append_to_base_url: str) -> dict:
        """
        Make a GET request to the SoundCharts API.

        Args:
            append_to_base_url (str): The endpoint to append to the base API URL.

        Returns:
            dict: The JSON response from the API as a dictionary.
        """
        base_url: str = "https://customer.api.soundcharts.com"
        url: str = base_url + append_to_base_url
        response: Response = requests.get(url, headers=self._get_credentials())
        response: dict = check_response_for_errors_and_convert_to_dict(response=response)
        logger.debug("GET request to {}".format(url))
        return response

    def song(self, uuid: str) -> Song:
        """
        Get a song by its SoundCharts UUID.

        Args:
            uuid (str): The UUID of the song.

        Returns:
            Song: The song object.

        Example:
            >>> soundcharts = SoundCharts(app_id="your_app_id", api_key="your_api_key")
            >>> song = soundcharts.song(uuid="1234567890")
        """
        endpoint: str = f"/api/v2.25/song/{uuid}"
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        song: Song = convert_song_response_to_object(response)
        return song

    def song_by_isrc(self, isrc: str) -> Song:
        """
        Get a song by its ISRC.

        Args:
            isrc (str): The ISRC of the song.

        Returns:
            Song: The song object.

        Example:
            >>> soundcharts = SoundCharts(app_id="your_app_id", api_key="your_api_key")
            >>> song = soundcharts.song_by_isrc(isrc="USUM71712345")
        """
        endpoint: str = f"/api/v2.25/song/by-isrc/{isrc}"
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        song: Song = convert_song_response_to_object(response)
        return song

    def song_by_platform_id(self, platform: str, identifier: str) -> Song:
        """
        Get a song by its platform and identifier.

        Args:
            platform (str): The platform name (e.g., 'spotify').
            identifier (str): The platform-specific song identifier.

        Returns:
            Song: The song object.

        Example:
            >>> soundcharts = SoundCharts(app_id="your_app_id", api_key="your_api_key")
            >>> song = soundcharts.song_by_platform_id(platform="spotify", identifier="2Fxmhks0bxGSBdJ92vM42m")
        """
        endpoint: str = f"/api/v2.25/song/by-platform/{platform}/{identifier}"
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        song: Song = convert_song_response_to_object(response)
        return song

    def song_ids(self, uuid: str, platform: str = None, offset: int = 0, limit: int = 100) -> list[PlatformIdentifier]:
        """
        Get platform-specific identifiers for a song.

        Args:
            uuid (str): The UUID of the song.
            platform (str, optional): A platform name to filter the results.
            offset (int, optional): The starting position of the results. Defaults to 0.
            limit (int, optional): The number of results to return. Defaults to 100.

        Returns:
            list[PlatformIdentifier]: A list of platform identifiers for the song.

        Example:
            >>> soundcharts = SoundCharts(app_id="your_app_id", api_key="your_api_key")
            >>> platform_ids = soundcharts.song_ids(uuid="1234567890", platform="spotify", limit=50)
        """
        endpoint = f"/api/v2/song/{uuid}/identifiers?offset={offset}&limit={limit}"
        if platform:
            endpoint = f"/api/v2/song/{uuid}/identifiers?platform={platform}&offset={offset}&limit={limit}"
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        items: list = response.get("items")
        platform_identifiers = [PlatformIdentifier(**item) for item in items]
        return platform_identifiers

    def song_albums(self, uuid: str, type: str = "all", offset: int = 0, limit: int = 100,
                    sort_by: str = "title", sort_order: str = "asc") -> list[Album]:
        """
        Retrieve albums associated with a song.

        Args:
            uuid (str): The UUID of the song.
            type (str, optional): Filter by album type. Defaults to 'all'.
            offset (int, optional): The starting position of the results. Defaults to 0.
            limit (int, optional): The number of results to return. Defaults to 100.
            sort_by (str, optional): Sort by field. Defaults to 'title'.
            sort_order (str, optional): Sort order. Defaults to 'asc'.

        Returns:
            list[Album]: A list of albums associated with the song.

        Example:
            >>> soundcharts = SoundCharts(app_id="your_app_id", api_key="your_api_key")
            >>> albums = soundcharts.song_albums(uuid="1234567890", type="album", limit=50, sort_by="releaseDate", sort_order="desc")
        """
        endpoint = f"/api/v2/song/{uuid}/albums?type={type}&offset={offset}&limit={limit}&sort_by={sort_by}&sort_order={sort_order}"
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        items: list = response.get("items")
        albums = [Album(**item) for item in items]
        return albums

    def song_audience(self, uuid: str, platform: str, start_date: str = None, end_date: str = None,
                      identifier: str = None) -> dict:
        """
        Retrieve audience data for a song on a specific platform.

        Args:
            uuid (str): The UUID of the song.
            platform (str): The platform code.
            start_date (str, optional): The start date for the audience data (format 'YYYY-MM-DD').
            end_date (str, optional): The end date for the audience data (format 'YYYY-MM-DD').
            identifier (str, optional): A specific song identifier on the platform.

        Returns:
            dict: Audience data for the song on the specified platform.

        Example:
            >>> soundcharts = SoundCharts(app_id="your_app_id", api_key="your_api_key")
            >>> audience_data = soundcharts.song_audience(uuid="1234567890", platform="spotify", start_date="2023-01-01", end_date="2023-03-31", identifier="2Fxmhks0bxGSBdJ92vM42m")
        """
        endpoint = f"/api/v2/song/{uuid}/audience/{platform}?start_date={start_date}&end_date={end_date}"
        if identifier:
            endpoint += f"&identifier={identifier}"

        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        items = response.get("items")
        return items
