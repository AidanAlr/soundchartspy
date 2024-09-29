from requests import Response

from soundchartspy.data import Label, Genre, Artist, ISRC, Audio, Song
from soundchartspy.exceptions import SoundChartsError


def convert_song_response_to_object(response: dict) -> Song:
    """
    Takes a response containing song object data from SoundCharts and extracts the attributes for a song object.
    :param responset:
    :return song: A song object
    """
    response_object = response.get("object")
    isrc: dict = response_object.get("isrc")
    artists: list = response_object.get("artists")
    genres: list = response_object.get("genres")
    labels: list = response_object.get("labels")
    audio: dict = response_object.get("audio")

    isrc_object = ISRC(**isrc)
    artists_objects = [Artist(**artist) for artist in artists]
    genres_objects = [Genre(**genre) for genre in genres]
    labels_objects = [Label(**label) for label in labels]
    audio_object = Audio(**audio)

    non_object_attributes: dict = {key: value for key, value in response_object.items() if
                                   key not in ["isrc", "artists", "genres", "labels", "audio"]}

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
