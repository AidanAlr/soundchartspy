import datetime
import logging

import requests
from requests import Response

from soundchartspy.data import (
    Song,
    PlatformIdentifier,
    Album,
    Playlist,
    PlaylistPosition,
    RadioStation,
    Artist,
    ArtistSongEntry,
    AudienceData,
    ShortVideo,
)
from soundchartspy.utils import (
    check_response_for_errors_and_convert_to_dict,
    convert_song_response_to_object,
    convert_playlist_entry_data_to_tuple_pair,
    convert_json_to_artist_object,
    check_and_add_start_and_end_date_to_query_params,
)

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
        credentials = {"x-app-id": self._app_id, "x-api-key": self._api_key}
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
        response: dict = check_response_for_errors_and_convert_to_dict(
            response=response
        )
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
            >>> song = soundcharts.song(uuid="7d534228-5165-11e9-9375-549f35161576")
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

    def song_ids(
        self, uuid: str, platform: str = None, offset: int = 0, limit: int = 100
    ) -> list[PlatformIdentifier]:
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
            >>> platform_ids = soundcharts.song_ids(uuid="7d534228-5165-11e9-9375-549f35161576", platform="spotify", limit=50)
        """
        endpoint = f"/api/v2/song/{uuid}/identifiers?offset={offset}&limit={limit}"
        if platform:
            endpoint = f"/api/v2/song/{uuid}/identifiers?platform={platform}&offset={offset}&limit={limit}"
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        items: list = response.get("items")
        platform_identifiers = [PlatformIdentifier(**item) for item in items]
        return platform_identifiers

    def song_albums(
        self,
        uuid: str,
        type: str = "all",
        offset: int = 0,
        limit: int = 100,
        sort_by: str = "title",
        sort_order: str = "asc",
    ) -> list[Album]:
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
            >>> albums = soundcharts.song_albums(uuid="7d534228-5165-11e9-9375-549f35161576", type="album", limit=50, sort_by="releaseDate", sort_order="desc")
        """
        endpoint = f"/api/v2/song/{uuid}/albums?type={type}&offset={offset}&limit={limit}&sort_by={sort_by}&sort_order={sort_order}"
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        items: list[dict] = response.get("items")

        for item in items:
            item["releaseDate"] = datetime.datetime.fromisoformat(
                item.get("releaseDate")
            )

        albums = [Album(**item) for item in items]
        return albums

    def song_audience(
        self,
        uuid: str,
        platform: str,
        start_date: str = None,
        end_date: str = None,
        identifier: str = None,
    ) -> dict:
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
            >>> audience_data = soundcharts.song_audience(uuid="7d534228-5165-11e9-9375-549f35161576", platform="spotify", start_date="2023-01-01", end_date="2023-03-31", identifier="2Fxmhks0bxGSBdJ92vM42m")
        """
        endpoint = f"/api/v2/song/{uuid}/audience/{platform}?start_date={start_date}&end_date={end_date}"
        if identifier:
            endpoint += f"&identifier={identifier}"

        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        items = response.get("items")
        return items

    def song_spotify_popularity(
        self, uuid: str, start_date: str = None, end_date: str = None
    ) -> dict:
        """
        Retrieve Spotify popularity data for a song.

        Args:
            uuid (str): The UUID of the song.
            start_date (str, optional): The start date for the popularity data (format 'YYYY-MM-DD').
            end_date (str, optional): The end date for the popularity data (format 'YYYY-MM-DD').

        Returns:
            dict: Spotify popularity data for the song.

        Example:
            >>> soundcharts = SoundCharts(app_id="your_app_id", api_key="your_api_key")
            >>> spotify_popularity = soundcharts.song_spotify_popularity(uuid="7d534228-5165-11e9-9375-549f35161576")
        """
        endpoint = f"/api/v2/song/{uuid}/spotify/identifier/popularity?start_date={start_date}&end_date={end_date}"
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        items = response.get("items")
        return items

    def song_chart_entries(
        self,
        uuid: str,
        platform: str = "spotify",
        current_only: bool = True,
        offset: int = 0,
        limit: int = 100,
        sort_by: str = "position",
        sort_order: str = "asc",
    ) -> dict:
        """
        Retrieve chart entries for a song.

        Args:
            uuid (str): The UUID of the song.
            platform (str, optional): The platform code.
            current_only (bool, optional): Whether to return only current chart entries. Set to False for current and past entries. Defaults to True.
            offset (int, optional): The starting position of the results. Defaults to 0.
            limit (int, optional): The number of results to return. Defaults to 100. Maximum is 100.
            sort_by (str, optional): Sort by field. Defaults to 'position'. Other options are 'rankdate'.
            sort_order (str, optional): Sort order. Defaults to 'asc'. Other options are 'desc'.

        Returns:
            dict: Chart entries for the song.

        Example:
            >>> soundcharts = SoundCharts(app_id="your_app_id", api_key="your_api_key")
            >>> chart_entries = soundcharts.song_chart_entries(uuid="7d534228-5165-11e9-9375-549f35161576", platform="spotify", current_only=True, limit=50)
        """

        current_only: int = int(current_only)
        endpoint: str = (
            f"/api/v2/song/{uuid}/charts/ranks/{platform}?current_only={current_only}&offset={offset}&limit={limit}&sort_by={sort_by}&sort_order={sort_order}"
        )
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        items: dict = response.get("items")
        return items

    def song_playlist_entries(
        self,
        uuid: str,
        platform: str = "spotify",
        type: str = "all",
        offset: int = 0,
        limit: int = 100,
        sort_by: str = "position",
        sort_order: str = "asc",
    ) -> list[tuple[Playlist, PlaylistPosition]]:
        """
        Retrieve playlist entries for a song.

        Args:
            uuid (str): The UUID of the song
            platform (str, optional): The platform code
            type (str, optional): A playlist type. Available values are : 'all' or one of editorial, algorithmic, algotorial, major, charts, curators_listeners, radios, this_is
            offset (int, optional): The starting position of the results
            limit (int, optional): The number of results to return. Maximum is 100
            sort_by (str, optional): Sort criteria. Available values are : 'position', 'positionDate', 'subscriberCount', 'entryDate'
            sort_order (str, optional): Sort order. Available values are : asc, desc

        Returns:
            list[tuple[Playlist, PlaylistPosition]]: A list of playlist entries for the song

        Example:
            >>> soundcharts = SoundCharts(app_id="your_app_id", api_key="your_api_key")
            >>> playlist_entries = soundcharts.song_playlist_entries(uuid="7d534228-5165-11e9-9375-549f35161576")
        """
        endpoint: str = (
            f"/api/v2.20/song/{uuid}/playlist/current/{platform}?type={type}&offset={offset}&limit={limit}&sort_by={sort_by}&sort_order={sort_order}"
        )
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        items: dict = response.get("items")
        playlist_entries: list[tuple[Playlist, PlaylistPosition]] = [
            convert_playlist_entry_data_to_tuple_pair(item) for item in items
        ]
        return playlist_entries

    def song_radio_spins(
        self,
        uuid: str,
        radio_slugs: list[str],
        country_code: str = None,
        start_date: str = None,
        end_date: str = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[dict[str, RadioStation | str]]:
        """
        Retrieve radio spins for a song.

        Args:
            uuid (str): The UUID of the song.
            radio_slugs (list[str]): A list of radio slugs.
            country_code (str): The country code.
            start_date (str) : Period start date (Format ATOM). Example : 2019-01-01T00:00:00Z
            end_date (str): Period end date (Format ATOM). Example : 2019-01-01T00:00:00Z
            offset (int, optional): The starting position of the results. Defaults to 0.
            limit (int, optional): The number of results to return. Defaults to 100. Maximum is 100.

        Returns:
            dict: Radio spins for the song.

        Example:
            >>> soundcharts = SoundCharts(app_id="your_app_id", api_key="your_api_key")
            >>> radio_spins = soundcharts.song_radio_spins(uuid="7d534228-5165-11e9-9375-549f35161576", radio_slugs=["nrj", "funradio"], country_code="FR", start_date="2019-01-01T00:00:00Z", end_date="2019-01-01T00:00:00Z", offset=0, limit=100)
        """
        radio_slugs_str = ",".join(radio_slugs)
        endpoint = f"/api/v2/song/{uuid}/broadcasts?radio_slugs={radio_slugs_str}&country_code={country_code}&start_date={start_date}&end_date={end_date}&offset={offset}&limit={limit}"
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        items = response.get("items")

        new_items = []
        for item in items:
            radio = item.get("radio")
            item["radio"] = RadioStation(**radio)
            new_items.append(item)

        return new_items

    def song_radio_spin_count(
        self,
        uuid: str,
        radio_slugs: list[str],
        country_code: str = None,
        start_date: str = None,
        end_date: str = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[dict[str, RadioStation | int]]:
        """
        Retrieve radio spin count for a song.

        Args:
            uuid (str): The UUID of the song.
            radio_slugs (list[str]): A list of radio slugs.
            country_code (str): The country code.
            start_date (str) : Period start date (Format ATOM). Example : 2019-01-01T00:00:00Z
            end_date (str): Period end date (Format ATOM). Example : 2019-01-01T00:00:00Z
            offset (int, optional): The starting position of the results. Defaults to 0.
            limit (int, optional): The number of results to return. Defaults to 100. Maximum is 100.

        Returns:
            list of dict: Radio spin count for the song. Example Return = [{"playCount": 10,"radio": RadioStation}, {"playCount": 20,"radio": RadioStation}]

        Example:
            >>> soundcharts = SoundCharts(app_id="your_app_id", api_key="your_api_key")
            >>> radio_spins = soundcharts.song_radio_spin_count(uuid="7d534228-5165-11e9-9375-549f35161576", radio_slugs=["nrj", "funradio"], country_code="FR", start_date="2019-01-01T00:00:00Z", end_date="2019-01-01T00:00:00Z", offset=0, limit=100)
        """
        radio_slugs_str = ",".join(radio_slugs)
        endpoint = f"/api/v2/song/{uuid}/broadcasts?radio_slugs={radio_slugs_str}&country_code={country_code}&start_date={start_date}&end_date={end_date}&offset={offset}&limit={limit}"
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        items = response.get("items")

        new_items = []
        for item in items:
            radio = item.get("radio")
            item["radio"] = RadioStation(**radio)
            new_items.append(item)

        return new_items

    def artist(self, uuid: str) -> Artist:
        """
        Get an artist by its SoundCharts UUID.

        Args:
            uuid (str): The UUID of the artist.

        Returns:
            artist (Artist): The artist object.

        Example:
            >>> soundcharts = SoundCharts(app_id="your_app_id", api_key="your_api_key")
            >>> artist = soundcharts.artist(uuid="7d534228-5165-11e9-9375-549f35161576")
        """
        endpoint: str = f"/api/v2.9/artist/{uuid}"
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        # Get the artist object from the response
        artist: dict = response.get("object")
        artist: Artist = convert_json_to_artist_object(artist)
        return artist

    def artist_by_platform_id(self, platform: str, identifier: str) -> Artist:
        """
        Get an artist by its platform and identifier.
        Args:
            platform (str): The platform code (e.g.'spotify'). Usually just the platform name in lowercase, replace spaces with -.
             These can be found using the platforms method.
            identifier (str): The platform-specific artist identifier.

        Returns:
            artist (Artist): The artist object.

        """
        endpoint: str = f"/api/v2.9/artist/by-platform/{platform}/{identifier}"
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        # Get the artist object from the response
        artist: dict = response.get("object")
        artist: Artist = convert_json_to_artist_object(artist)
        return artist

    def artist_ids(
        self, uuid: str, platform: str = None, offset: int = 0, limit: int = 100
    ) -> list[PlatformIdentifier]:
        """
        Get platform-specific identifiers for an artist.

        Args:
            uuid (str): The UUID of the artist.
            platform (str, optional): A platform name to filter the results.
            offset (int, optional): The starting position of the results. Defaults to 0.
            limit (int, optional): The number of results to return. Defaults to 100.

        Returns:
            list[PlatformIdentifier]: A list of platform identifiers for the artist.

        Example:
            >>> soundcharts = SoundCharts(app_id="your_app_id", api_key="your_api_key")
            >>> platform_ids = soundcharts.artist_ids(uuid="7d534228-5165-11e9-9375-549f35161576", platform="spotify", limit=50)
        """
        endpoint = f"/api/v2/artist/{uuid}/identifiers?platform={platform}&offset={offset}&limit={limit}"
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        items: list = response.get("items")
        platform_identifiers = [PlatformIdentifier(**item) for item in items]
        return platform_identifiers

    def artist_songs(
        self,
        uuid: str,
        offset: int = 0,
        limit: int = 100,
        sort_by: str = "name",
        sort_order: str = "asc",
    ) -> list[Song]:
        """
        Get songs associated with an artist.

        Args:
            uuid (str): The UUID of the artist.
            offset (int, optional): The starting position of the results. Defaults to 0.
            limit (int, optional): The number of results to return. Defaults to 100.
            sort_by (str, optional): Sort by field. Defaults to 'name'. Available values are : name, releaseDate, spotifyStream, shazamCount, youtubeViews, spotifyPopularity
            sort_order (str, optional): Sort order. Defaults to 'asc'. Other options are 'desc'.

        Returns:
            list[Song]: A list of songs associated with the artist.

        Example:
            >>> soundcharts = SoundCharts(app_id="your_app_id", api_key="your_api_key")
            >>> songs = soundcharts.artist_songs(offset=0, limit=50)
        """
        endpoint = f"/api/v2.21/artist/{uuid}/songs?offset={offset}&limit={limit}&sortBy={sort_by}&sortOrder={sort_order}"
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        items: list = response.get("items")
        # Convert the release date to a datetime object
        for song in items:
            release_date = song.get("releaseDate")
            if release_date:
                song["releaseDate"] = datetime.datetime.fromisoformat(release_date)

        songs = [ArtistSongEntry(**item) for item in items]
        return songs

    def artist_albums(
        self,
        uuid: str,
        type: str = "all",
        offset: int = 0,
        limit: int = 100,
        sort_by: str = "title",
        sort_order: str = "asc",
    ) -> list[Album]:
        """
        Get albums associated with an artist.
        Args:
            uuid (str): The UUID of the artist.
            type (str, optional): Filter by album type. Defaults to 'all'. Available values are : all, album, single, compil
            offset (int, optional): The starting position of the results. Defaults to 0.
            limit (int, optional): The number of results to return. Defaults to 100.
            sort_by (str, optional): Sort by field. Defaults to 'title'. Available values are : title, releaseDate
            sort_order (str, optional): Sort order. Defaults to 'asc'. Other options are 'desc'.

        Returns:
            list[Album]: A list of albums associated with the artist.

        """

        endpoint = f"/api/v2.34/artist/{uuid}/albums?offset={offset}&limit={limit}&sortBy={sort_by}&sortOrder={sort_order}"
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        albums: list[dict] = response.get("items")
        albums: list[Album] = [Album(**item) for item in albums]
        return albums

    def artist_similar_artists(
        self, uuid: str, offset: int = 0, limit: int = 100
    ) -> list[Artist]:
        """
        Similar artists ("Fans Also Like" profiles) are determined by Spotify algorithms that analyze the listening habits of artists' fans.
        For instance, if many fans of artist A frequently listen to artists B and C, then B and C are considered similar artists. Artists cannot edit what appears in "Fans Also Like."
        We obtain the list of similar artists from Spotify and rank it alphabetically, which may differ from the ranking on Spotify's dashboard.
        Args:
            uuid (str): The UUID of the artist.
            offset (int, optional): The starting position of the results. Defaults to 0.
            limit (int, optional): The number of results to return. Defaults to 100.

        Returns:

        """
        endpoint = f"/api/v2/artist/{uuid}/related?offset={offset}&limit={limit}"
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        items: list = response.get("items")
        similar_artists: list[Artist] = [Artist(**item) for item in items]
        return similar_artists

    def artist_current_stats(self, uuid: str, period: int = 7) -> dict:
        """
        This API returns all current stats of all platforms, with the growth period of your choice.
        Args:
            uuid (str): The UUID of the artist.
            period (int, optional): The number of days to calculate the growth. Defaults to 7.
        Returns:
            dict: The current stats for the artist. "Social", "Popularity", "Retention", "Streaming" are main categories.
        """
        endpoint = f"/api/v2/artist/{uuid}/current/stats"
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        return response

    def artist_audience(
        self,
        uuid: str,
        platform: str = "spotify",
        start_date: str = None,
        end_date: str = None,
    ) -> list[AudienceData]:
        """
        Available platforms are listed in the Get platforms for audience data endpoint.

        The API response will include the platform's primary “fan” metric even if it is named differently (e.g., Facebook likes, YouTube subscribers, Deezer fans, Gaana favorites, Line Music Likes). All these are under the "followerCount" metric.

        The API response may not return a value for all dates, as we may miss a day or two. These data points may still show on our UI because we estimate the missing data between two points.

        Audience refresh frequency depends on the artist’s followers on the platform:

        less than 9 followers: every 15 days
        between 10 and 149 followers: every 7 days
        between 150 and 499 followers: every 5 days
        between 500 and 4,999 followers: every 3 days
        more than 5,000: every 2 days

        Args:
            uuid (str): The UUID of the artist.
            platform (str): The platform code. Options include but not limited to "instagram", "spotify", "soundcloud", "tiktok", "triller", "youtube", "deezer" etc.
            start_date (str): Optional period start date for the audience data (format 'YYYY-MM-DD'). Period cannot exceed 90 days
            end_date (str): Optional period end date for the audience data (format 'YYYY-MM-DD'). Period cannot exceed 90 days

        Returns:
            list[AudienceData]: A list of audience data for the artist on the specified platform.

        """
        endpoint = f"/api/v2/artist/{uuid}/audience/{platform}"
        endpoint = check_and_add_start_and_end_date_to_query_params(
            endpoint, start_date, end_date
        )
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        items = response.get("items")
        audience_data_ls: list[AudienceData] = [AudienceData(**item) for item in items]
        return audience_data_ls

    def artist_local_audience(
        self,
        uuid: str,
        platform: str = "spotify",
        start_date: str = None,
        end_date: str = None,
    ) -> dict:
        """
        Get all values for artist followers for a month and located followers for a given date within that month

        Args:
            uuid (str): The UUID of the artist.
            platform (str): The platform code.
            start_date (str): The start date for the listening data (format 'YYYY-MM-DD').
            end_date (str): The end date for the listening data (format 'YYYY-MM-DD').
        Returns:

        """
        endpoint = f"/api/v2.37/artist/{uuid}/social/{platform}/followers/"
        endpoint = check_and_add_start_and_end_date_to_query_params(
            endpoint, start_date, end_date
        )
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        return response

    def artist_listeners_streams_views(
        self, uuid: str, platform: str, start_date: str = None, end_date: str = None
    ) -> dict:
        """
        Get the number of listeners, streams, and views for an artist on a specific platform.

        Args:
            uuid (str): The UUID of the artist.
            platform (str): The platform code.
            start_date (str): The start date for the listening data (format 'YYYY-MM-DD').
            end_date (str): The end date for the listening data (format 'YYYY-MM-DD').

        Returns:
            dict: The number of listeners, streams, and views for the artist on the specified platform.

        """
        endpoint = f"/api/v2/artist/{uuid}/streaming/{platform}/listening"
        endpoint = check_and_add_start_and_end_date_to_query_params(
            endpoint, start_date, end_date
        )
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        return response

    def artist_spotify_monthly_listeners_latest(self, uuid: str) -> dict:
        """
        Get the number of monthly listeners for an artist on Spotify.
        Spotify uses 28 rolling days (4 weeks of 7 days) to measure a month.
        It makes sense as the number of days in a month varies from 28 to 31, and people’s behavior depends more on the
        days of the week than on dates within a single month.
        This way, there is always an equal number of each day within the 28 rolling day ‘monthly listeners’ stats.

        Args:
            uuid (str): The UUID of the artist.

        Returns:
            dict: The number of monthly listeners for the artist on Spotify.

        """
        endpoint = f"/api/v2/artist/{uuid}/streaming/spotify/listeners"
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        return response

    def artist_spotify_monthly_listeners_by_month(
        self, uuid: str, year: str, month: str
    ) -> dict:
        """
        Get the number of monthly listeners for an artist on Spotify by month.
        Args:
            uuid (str): The UUID of the artist.
            year (str): Year YYYY format
            month (str): Month MM format

        Returns:
            dict: The number of monthly listeners for the artist on Spotify by month.

        """
        endpoint = f"/api/v2/artist/{uuid}/streaming/spotify/listeners/{year}/{month}"
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        return response

    def artist_retention(
        self,
        uuid: str,
        platform: str = "spotify",
        start_date: str = None,
        end_date: str = None,
    ) -> dict:
        """
        Get an artist's fan retention rate across platforms.

        Also called “conversion rate” or “followers to listeners ratio”, this metric shows the relationship between the listeners and the followers. Do take into account that not all followers are listeners. We calculate this by dividing the total number of listeners by the total number of followers, multiplied by 100. The higher the percentage is, the better the artist can turn its listeners into followers.

        Available platforms for this endpoint are Spotify, YouTube, Anghami and JioSaavn.

        Note that the metrics can be different according to the platform:

        Spotify: Followers / Monthly Listeners
        JioSaavn: Followers / Monthly Listeners
        YouTube: Subscribers / Views
        Anghami: Followers / Plays

        Args:
            uuid (str): The UUID of the artist.
            platform (str): The platform code.
            start_date (str): The start date for the retention data (format 'YYYY-MM-DD').
            end_date (str): The end date for the retention data (format 'YYYY-MM-DD').

        Returns:
            dict: The retention data for the artist on the specified platform.

        """
        endpoint = f"/api/v2/artist/{uuid}/{platform}/retention"
        endpoint = check_and_add_start_and_end_date_to_query_params(
            endpoint, start_date, end_date
        )
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        return response

    def artist_popularity(
        self,
        uuid: str,
        platform: str = "spotify",
        start_date: str = None,
        end_date: str = None,
    ) -> dict:
        """
        Get an artist's popularity on a platform.

        Args:
            uuid (str): The UUID of the artist.
            platform (str): The platform code.
            start_date (str): The start date for the popularity data (format 'YYYY-MM-DD').
            end_date (str): The end date for the popularity data (format 'YYYY-MM-DD').

        Returns:
            dict: The popularity data for the artist on the specified platform.

        """
        endpoint = f"/api/v2/artist/{uuid}/popularity/{platform}"
        endpoint = check_and_add_start_and_end_date_to_query_params(
            endpoint, start_date, end_date
        )
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        return response

    def artist_audience_report_latest(self, uuid: str, platform: str = "instagram"):
        """
        Get the latest demographics reports for social/streaming platforms.

        Please note that:

        Available platforms for this endpoint are instagram, youtube, and tiktok.
        The artist should have at least 1,000 followers/subscribers on the platform for us to get an audience report.
        The depth for these platform reports depends on the platform. Instagram is the only platform that returns data for both likes & followers.
        Audience reports are updated monthly.

        Args:
            uuid (str): The UUID of the artist.
            platform (str): The platform code.

        Returns:
            dict: The latest audience report for the artist on the specified platform.

        """
        endpoint = f"/api/v2/artist/{uuid}/audience/{platform}/report/latest"
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        return response

    def artist_audience_report_dates(
        self,
        uuid: str,
        platform: str = "instagram",
        start_date: str = None,
        end_date: str = None,
        offset: int = 0,
        limit: int = 100,
    ):
        """
        Get the available dates for demographics reports for social/streaming platforms.

        Please note that:

        Available platforms for this endpoint are instagram, youtube, and tiktok.
        The artist should have at least 1,000 followers/subscribers on the platform for us to get an audience report.
        The depth for these platform reports depends on the platform. Instagram is the only platform that returns data for both likes & followers.
        Audience reports are updated monthly.

        Args:
            uuid (str): The UUID of the artist.
            platform (str): The platform code.
            start_date (str): The start date for the audience reports (format 'YYYY-MM-DD').
            end_date (str): The end date for the audience reports (format 'YYYY-MM-DD').
            offset (int): The starting position of the results.
            limit (int): The number of results to return. Maximum is 100.

        Returns:
            dict: The available dates for audience reports for the artist on the specified platform.

        """
        endpoint = f"/api/v2/artist/{uuid}/audience/{platform}/report/available-dates"
        endpoint = check_and_add_start_and_end_date_to_query_params(
            endpoint, start_date, end_date
        )
        if offset:
            endpoint += f"&offset={offset}"
        if limit:
            endpoint += f"&limit={limit}"
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        return response

    def artist_audience_report_by_date(
        self, uuid: str, platform: str = "instagram", date: str = None
    ):
        """
        Get the demographics reports for social/streaming platforms by date.

        Please note that:

        To avoid unnecessary requests, you can first get the dates with available data from the Get available audience report dates endpoint.
        Available platforms for this endpoint are Instagram, YouTube, and TikTok. Note that the depth for these platform reports depends on the platform. Instagram is the only platform that returns data for both likes & followers.

        Args:
            uuid (str): The UUID of the artist.
            platform (str): The platform code.
            date (str): The date for the audience reports (format 'YYYY-MM-DD').

        Returns:
            dict: The audience report for the artist on the specified platform by date.

        """
        endpoint = f"/api/v2/artist/{uuid}/audience/{platform}/report/{date}"
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        return response

    def artist_short_videos(
        self, uuid: str, platform: str = "instagram"
    ) -> list[ShortVideo]:
        """
        Get an artist’s short videos, and the current audience of each video (comments/likes/views).

        This endpoint is available for YouTube shorts and Instagram reels.

        Args:
            uuid (str): The UUID of the artist.
            platform (str): The platform code. Options include "instagram", "youtube".

        Returns:

        """
        endpoint = f"/api/v2/artist/{uuid}/shorts/{platform}/videos"
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        items = response.get("items")
        short_videos = [ShortVideo(**item) for item in items]
        return short_videos

    def artist_short_video_audience(
        self, identifier: str, start_date: str = None, end_date: str = None
    ) -> dict:
        """
        Get the audience data for a short video.

        This endpoint is available for YouTube shorts and Instagram reels.

        Args:
            identifier (str): The identifier of the short video.
            start_date (str): The start date for the audience data (format 'YYYY-MM-DD').
            end_date (str): The end date for the audience data (format 'YYYY-MM-DD').

        Returns:

        """
        endpoint = f"/api/v2/artist/shorts/{identifier}/audience"
        endpoint = check_and_add_start_and_end_date_to_query_params(
            endpoint, start_date, end_date
        )
        response: dict = self._make_api_get_request(append_to_base_url=endpoint)
        return response
