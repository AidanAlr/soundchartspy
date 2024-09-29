import datetime
import json
from dataclasses import dataclass, field
from typing import List


@dataclass
class ISRC:
    value: str
    countryCode: str
    countryName: str


@dataclass
class Artist:
    uuid: str
    slug: str
    name: str
    appUrl: str
    imageUrl: str


@dataclass
class Genre:
    root: str
    sub: List[str]


@dataclass
class Label:
    name: str
    type: str


@dataclass
class Audio:
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
    platformName: str
    platformCode: str
    identifier: str
    url: str
    default: bool


@dataclass
class Song:
    uuid: str
    name: str
    isrc: ISRC
    creditName: str
    artists: List[Artist]
    releaseDate: str
    copyright: str
    appUrl: str
    imageUrl: str
    duration: int
    genres: List[Genre]
    composers: List[str]
    producers: List[str]
    labels: List[Label]
    audio: Audio


@dataclass
class Album:
    name: str
    creditName: str
    releaseDate: str | datetime.datetime
    default: bool
    type: str
    uuid: str
    _releaseDate: datetime.datetime = field(init=False, repr=False)

    def __post_init__(self):
        self._releaseDate = datetime.datetime.fromisoformat(self.releaseDate)
        self.releaseDate = self._releaseDate
