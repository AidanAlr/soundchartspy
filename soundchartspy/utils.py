import datetime

from requests import Response

from soundchartspy.data import Label, Genre, Artist, ISRC, Audio, Song, Playlist, PlaylistPosition
from soundchartspy.exceptions import SoundChartsError


def convert_song_response_to_object(response: dict) -> Song:
    """
    Converts a song response from SoundCharts to a Song object.
    Args:
        response: The response from SoundCharts.
    Returns:
        Song: The Song object created
    """
    response_object = response.get("object")

    # Extract the json representation of the objects from the response
    isrc: dict = response_object.get("isrc")
    artists: list = response_object.get("artists")
    genres: list = response_object.get("genres")
    labels: list = response_object.get("labels")
    audio: dict = response_object.get("audio")

    # Create the objects from the response data
    isrc_object = ISRC(**isrc)
    artists_objects = [Artist(**artist) for artist in artists]
    genres_objects = [Genre(**genre) for genre in genres]
    labels_objects = [Label(**label) for label in labels]
    audio_object = Audio(**audio)

    # Remove the object attributes from the response object
    non_object_attributes: dict = {key: value for key, value in response_object.items() if
                                   key not in ["isrc", "artists", "genres", "labels", "audio"]}

    # Convert the release date string to a datetime object
    non_object_attributes = convert_release_date_to_datetime(non_object_attributes)

    # Create the song object
    song = Song(
        isrc=isrc_object,
        artists=artists_objects,
        genres=genres_objects,
        labels=labels_objects,
        audio=audio_object,
        **non_object_attributes
    )

    return song


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


def convert_release_date_to_datetime(item: dict) -> dict:
    release_date = item.get("releaseDate")
    if release_date:
        item["releaseDate"] = datetime.datetime.fromisoformat(release_date)
    return item


def convert_playlist_entry_data_to_tuple_pair(item: dict) -> tuple[Playlist, PlaylistPosition]:
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
        "peakPositionDate": item.get("peakPositionDate")
    }
