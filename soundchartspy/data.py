import json
from dataclasses import dataclass
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

# # Example usage
# song = Song(
#     uuid="7d534228-5165-11e9-9375-549f35161576",
#     name="bad guy",
#     isrc=ISRC(value="USUM71900764", countryCode="US", countryName="United States"),
#     creditName="Billie Eilish",
#     artists=[Artist(
#         uuid="11e81bcc-9c1c-ce38-b96b-a0369fe50396",
#         slug="billie-eilish",
#         name="Billie Eilish",
#         appUrl="https://app.soundcharts.com/app/artist/billie-eilish/overview",
#         imageUrl="https://assets.soundcharts.com/artist/c/1/c/11e81bcc-9c1c-ce38-b96b-a0369fe50396.jpg"
#     )],
#     releaseDate="2019-03-29T00:00:00+00:00",
#     copyright="℗ 2019 Darkroom/Interscope Records",
#     appUrl="https://app.soundcharts.com/app/song/7d534228-5165-11e9-9375-549f35161576/overview",
#     imageUrl="https://assets.soundcharts.com/song/5/6/1/7d534228-5165-11e9-9375-549f35161576.jpg",
#     duration=194,
#     genres=[
#         Genre(root="alternative", sub=["alternative"]),
#         Genre(root="electronic", sub=["electronic"]),
#         Genre(root="rock", sub=["rock"])
#     ],
#     composers=["Finneas O'Connell", "Billie Eilish O'Connell"],
#     producers=["Finneas O'Connell"],
#     labels=[
#         Label(name="Interscope", type="Universal"),
#         Label(name="Darkroom", type="Universal")
#     ],
#     audio=Audio(
#         danceability=0.7,
#         energy=0.43,
#         instrumentalness=0.13,
#         key=7,
#         liveness=0.1,
#         loudness=-10.97,
#         mode=1,
#         speechiness=0.38,
#         tempo=135.13,
#         timeSignature=4,
#         valence=0.56
#     )
# )
