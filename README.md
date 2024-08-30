# Sounchartspy

A python wrapper for the [Soundcharts API](https://www.soundcharts.com/api/docs).

## Installation

```bash
pip install soundchartspy
```

## Example Usage

Get the metadata of a song using its uuid.

```python
from soundchartspy import Soundcharts

sc = Soundcharts(api_key='your_api_key', app_id='your_app_id')
song = sc.get_song_metadata_from_uuid('song_uuid')

print(song.get_name())
print(song.get_main_artist_name())
print(song.get_release_date())
```

Get the song audience on spotify.

```python
from soundchartspy import Soundcharts

sc = Soundcharts(api_key='your_api_key', app_id='your_app_id')
audience_data: list[dict] = sc.get_song_audience('song_uuid', 'spotify')
for data in audience_data:
    print("Date: {}, Metric Value:{}".format(data.get('date'), data.get('value')) 
```