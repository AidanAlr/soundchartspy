# Sounchartspy

A python wrapper for the [Soundcharts API](https://doc.api.soundcharts.com/api/v2/doc).

## Installation

```bash
pip install soundchartspy
```

## Example Usage

```python
from soundchartspy.client import SoundCharts
from soundchartspy.data import Song, Album

# Initialize the SoundCharts client
sc = SoundCharts(api_key='your_api_key', app_id='your_app_id')

# Get the song by uuid
song: Song = sc.song(song_uuid='7d534228-5165-11e9-9375-549f35161576')
print("Song Name: {}, Artists: {}".format(song.name, song.artists))

# Get the song audience on spotify.
audience_data: dict = sc.song_audience(song.uuid, 'spotify')
print("Spotify Audience: {}".format(audience_data))

# Get the song albums
albums: list[Album] = sc.song_albums(song.uuid)
print("Albums: {}".format(albums))
```