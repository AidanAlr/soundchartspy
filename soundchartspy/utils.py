import datetime

from requests import Response

from soundchartspy.data import (
    Label,
    Genre,
    Artist,
    ISRC,
    Audio,
    Song,
    Playlist,
    PlaylistPosition,
)
from soundchartspy.exceptions import SoundChartsError


def convert_song_response_to_object(response: dict) -> Song:
    """
    Converts a song response from SoundCharts to a Song object.
    Args:
        response: The response from SoundCharts.
    Returns:
        Song: The Song object created
    """
    song: dict = response.get("object")

    # Create the objects from the response data
    song["isrc"] = ISRC(**song.get("isrc"))
    song["artists"] = [Artist(**artist) for artist in song.get("artists")]
    song["genres"] = [Genre(**genre) for genre in song.get("genres")]
    song["labels"] = [Label(**label) for label in song.get("labels")]
    song["audio"] = Audio(**song.get("audio"))
    song["releaseDate"] = datetime.datetime.fromisoformat(song.get("releaseDate"))

    return Song(**song)


def get_soundcharts_error_code_message(response: dict):
    error: dict = response.get("errors")[0]
    code: str = error.get("code")
    message: str = error.get("message")
    return code, message


def check_response_for_errors_and_convert_to_dict(response: Response) -> dict:
    """
    Checks the response object from SoundCharts for an error and raises a python exception containing the same info
    if found.
    :param response:
    :return response: The response object converted to a dictionary
    :raises SoundChartsError: If an error is found in the response
    """
    response_status: int = response.status_code
    response: dict = response.json()
    error = response.get("errors")
    if not error:
        return response

    code, message = get_soundcharts_error_code_message(response)
    raise SoundChartsError(http_status=response_status, code=code, msg=message)


def convert_playlist_entry_data_to_tuple_pair(
    item: dict,
) -> tuple[Playlist, PlaylistPosition]:
    """
    Takes a dictionary of playlist entry data and converts it to a tuple of Playlist and PlaylistPosition objects.
    Args:
        item:

    Returns:
        tuple[Playlist, PlaylistPosition]: A tuple of Playlist and PlaylistPosition objects.

    """
    # Get the playlist and playlist position data required to construct the objects
    playlist = item.get("playlist")
    playlist_position = get_playlist_position_data(item)

    # Create the objects
    playlist = Playlist(**playlist)
    playlist_position = PlaylistPosition(**playlist_position)

    return playlist, playlist_position


def get_playlist_position_data(item):
    return {
        "position": item.get("position"),
        "peakPosition": item.get("peakPosition"),
        "entryDate": item.get("entryDate"),
        "positionDate": item.get("positionDate"),
        "peakPositionDate": item.get("peakPositionDate"),
    }


def convert_json_to_artist_object(artist: dict) -> Artist:
    # Convert the genres to Genre objects
    genres: list[Genre] = [Genre(**genre) for genre in artist.get("genres")]
    artist["genres"] = genres
    # Convert the birth date to a datetime object
    artist["birthDate"] = datetime.datetime.fromisoformat(artist["birthDate"])
    # Create the Artist object
    artist: Artist = Artist(**artist)
    return artist


def check_and_add_start_and_end_date_to_query_params(
    endpoint: str, start_date: str, end_date: str
):
    endpoint += "?"
    if start_date:
        endpoint += f"startDate={start_date}"
    if end_date:
        endpoint += f"&endDate={end_date}"

    return endpoint
