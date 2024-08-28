import inspect
import os
import unittest
from types import SimpleNamespace

from dotenv import load_dotenv

from src.soundchartspy.playlist import Playlist
from src.soundchartspy.soundcharts import SoundCharts
from src.soundchartspy.song import Song
from src.soundchartspy.logging_config import test_logger as logger

app_id = "soundcharts"
api_key = "soundcharts"

class TestSongMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.song_uuid: str = "7d534228-5165-11e9-9375-549f35161576"
        cls.soundcharts = SoundCharts(app_id=app_id, api_key=api_key)

    def test_get_song_data(self):
        song = self.soundcharts.get_song_metadata_from_uuid(uuid=self.song_uuid)
        assert isinstance(song, Song)
        assert song.get_uuid() == self.song_uuid
        assert song.get_name() == "bad guy"
        logger.debug(f"Song: {song.__dict__()}")

    def test_all_get_methods(self):
        song = self.soundcharts.get_song_metadata_from_uuid(uuid=self.song_uuid)
        methods = inspect.getmembers(song, predicate=inspect.ismethod)
        for name, method in methods:
            if "get_" in name:
                result = method()
                assert result is not None, f"Method {name}() returned None"

    def test_get_artist_follower_count_from_uuid(self):
        song = self.soundcharts.get_song_metadata_from_uuid(uuid=self.song_uuid)
        artist_uuid = song.get_main_artist_uuid()
        platform_list = ["spotify", "soundcloud"]
        for platform in platform_list:
            followers = self.soundcharts.get_artist_follower_count_from_uuid(artist_uuid=artist_uuid, platform=platform)
            assert followers > 0, "Followers were not fetched! Error in test"
            logger.debug(f"Platform: {platform}, Followers: {followers}")


class TestPlaylist(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.song_uuid: str = "7d534228-5165-11e9-9375-549f35161576"
        cls.playlist_uuid: str = "86694fd0-cdce-11e8-8cff-549f35161576"
        cls.soundcharts = SoundCharts(app_id=app_id, api_key=api_key)

    def test_get_playlist_metadata(self):
        playlist: Playlist = self.soundcharts.get_playlist_metadata_from_uuid(self.playlist_uuid)
        assert playlist.get_name() is not None

    def test_all_get_methods(self):
        playlist: Playlist = self.soundcharts.get_playlist_metadata_from_uuid(self.playlist_uuid)
        methods = inspect.getmembers(playlist, predicate=inspect.ismethod)
        for name, method in methods:
            if "get_" in name:
                result = method()
                assert result is not None, f"Method {name}() returned None"
