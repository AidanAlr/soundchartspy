import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class AudienceData:
    """
    Represents audience data for an artist or song.

    Attributes:
        date (datetime.datetime): The date of the audience data.
        likeCount (int): The number of likes.
        followerCount (int): The number of followers.
        followingCount (int): The number of accounts followed.
        postCount (int): The number of posts.
        viewCount (int): The number of views.
    """

    date: datetime.datetime
    likeCount: Optional[int]
    followerCount: Optional[int]
    followingCount: Optional[int]
    postCount: Optional[int]
    viewCount: Optional[int]


@dataclass
class ISRC:
    """
    Represents an International Standard Recording Code (ISRC) for a song.

    Attributes:
        value (str): The ISRC value, a unique identifier for the recording.
        countryCode (str): The country code associated with the ISRC.
        countryName (str): The name of the country associated with the ISRC.
    """

    value: str
    countryCode: str
    countryName: str


@dataclass
class Artist:
    """
    Represents an artist's information.

    Attributes:
        uuid (str): The unique identifier for the artist.
        slug (str): A short string that identifies the artist in a URL-friendly format.
        name (str): The name of the artist.
        appUrl (str): The URL to the artist's profile on the SoundCharts platform.
        imageUrl (str): The URL to the artist's image.
    """

    uuid: str
    slug: str
    name: str
    appUrl: str
    imageUrl: str
    countryCode: Optional[str] = None
    biography: Optional[str] = None
    isni: Optional[str] = None
    ipi: Optional[str] = None
    gender: Optional[str] = None
    type: Optional[str] = None
    birthDate: Optional[datetime.datetime] = None
    genres: Optional[list[str]] = None


@dataclass
class Genre:
    """
    Represents the genre of a song.

    Attributes:
        root (str): The main or root genre of the song.
        sub (list[str]): A list of sub-genres associated with the song.
    """

    root: str
    sub: list[str]


@dataclass
class Label:
    """
    Represents a record label associated with a song.

    Attributes:
        name (str): The name of the label.
        type (str): The type of label (e.g., major, indie).
    """

    name: str
    type: str


@dataclass
class Audio:
    """
    Represents the audio properties of a song.

    Attributes:
        danceability (float): A measure of how suitable the track is for dancing.
        energy (float): A measure of intensity and activity.
        instrumentalness (float): Predicts whether the track contains no vocals.
        key (int): The key of the track.
        liveness (float): A measure of the presence of a live audience in the track.
        loudness (float): The overall loudness of the track in decibels.
        mode (int): The modality (major or minor) of the track.
        speechiness (float): A measure of the presence of spoken words.
        tempo (float): The tempo of the track in beats per minute (BPM).
        timeSignature (int): The time signature of the track.
        valence (float): A measure of the musical positiveness of the track.
    """

    danceability: float
    energy: float
    instrumentalness: float
    key: int
    liveness: float
    loudness: float
    mode: int
    speechiness: float
    tempo: float
    timeSignature: int
    valence: float


@dataclass
class PlatformIdentifier:
    """
    Represents platform-specific identifiers for a song or artist.

    Attributes:
        platformName (str): The name of the platform (e.g., Spotify, Apple Music).
        platformCode (str): A short code representing the platform.
        identifier (str): The unique identifier for the song or artist on the platform.
        url (str): The URL to the song or artist on the platform.
        default (bool): Whether this is the default identifier.
    """

    platformName: str
    platformCode: str
    identifier: str
    url: str
    default: bool


@dataclass
class Song:
    """
    Represents a song with its metadata.

    Attributes:
        uuid (str): The unique identifier for the song.
        name (str): The name of the song.
        isrc (ISRC): The ISRC code for the song.
        creditName (str): The credited name for the song's release.
        artists (list[Artist]): A list of artists associated with the song.
        releaseDate (str): The release date of the song in ISO format.
        copyright (str): The copyright information for the song.
        appUrl (str): The URL to the song on the SoundCharts platform.
        imageUrl (str): The URL to the song's cover image.
        duration (int): The duration of the song in seconds.
        genres (list[Genre]): A list of genres associated with the song.
        composers (list[str]): A list of composers of the song.
        producers (list[str]): A list of producers of the song.
        labels (list[Label]): A list of labels associated with the song.
        audio (Audio): The audio properties of the song.
        explicit (bool): Whether the song contains explicit content.
        languageCode (str): The language code of the song.
    """

    uuid: str
    name: str
    isrc: ISRC
    creditName: str
    artists: list[Artist]
    releaseDate: str
    copyright: str
    appUrl: str
    imageUrl: str
    duration: int
    genres: list[Genre]
    composers: list[str]
    producers: list[str]
    labels: list[Label]
    audio: Audio
    explicit: bool
    languageCode: str


@dataclass
class ArtistSongEntry:
    uuid: str
    creditName: str
    name: str
    releaseDate: datetime.datetime


@dataclass
class Album:
    """
    Represents an album with its metadata.

    Attributes:
        name (str): The name of the album.
        creditName (str): The credited name for the album's release.
        releaseDate (datetime.datetime): The release date of the album.
        default (bool): Whether this album is the default release.
        type (str): The type of album (e.g. Album, Compil).
        uuid (str): The unique identifier for the album.
    """

    name: str
    creditName: str
    releaseDate: datetime.datetime
    type: str
    uuid: str
    default: Optional[bool] = None


@dataclass
class Playlist:
    """
    Represents a playlist with its metadata.

    Attributes:
        uuid (str): The unique identifier for the playlist.
        name (str): The name of the playlist.
        identifier (str): The identifier of the playlist.
        platform (str): The platform where the playlist is hosted.
        countryCode (str): The country code associated with the playlist.
        latestCrawlDate (datetime.datetime): The date of the latest crawl.
        latestTrackCount (int): The latest track count of the playlist.
        latestSubscriberCount (int): The latest subscriber count of the playlist.
        type (str): The type of playlist (e.g., user, editorial).
    """

    uuid: str
    name: str
    identifier: str
    platform: str
    countryCode: str
    latestCrawlDate: datetime.datetime
    latestTrackCount: int
    latestSubscriberCount: int
    type: str


@dataclass
class PlaylistPosition:
    """
    Represents the position of a song in a playlist.

    Attributes:
        position (int): The position of the song in the playlist.
        peakPosition (int): The peak position of the song in the playlist.
        entryDate (datetime.datetime): The date the song entered the playlist.
        positionDate (datetime.datetime): The date of the position.
        peakPositionDate (datetime.datetime): The date of the peak position.
    """

    position: int
    peakPosition: int
    entryDate: datetime.datetime
    positionDate: datetime.datetime
    peakPositionDate: datetime.datetime


@dataclass
class RadioStation:
    """
    Represents a radio station with its metadata.

    Attributes:
        slug (str): The unique identifier for the radio station.
        name (str): The name of the radio station.
        cityName (str): The city where the radio station is located.
        countryCode (str): The country code associated with the radio station.
        countryName (str): The name of the country associated with the radio station.
        timeZone (str): The time zone of the radio station.
    """

    slug: str
    name: str
    cityName: str
    countryCode: str
    countryName: str
    timeZone: str


@dataclass
class ShortVideo:
    """
    Represents a short video with its metadata.
    """

    identifier: str
    title: str
    description: str
    createdAt: datetime.datetime
    externalUrl: str
    latestAudience: dict
