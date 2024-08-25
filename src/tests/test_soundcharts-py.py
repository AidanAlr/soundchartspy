import os
import unittest
from types import SimpleNamespace

from dotenv import load_dotenv

from src.soundchartspy.soundchartspy import SoundCharts
from src.soundchartspy.song import Song
from src.soundchartspy.logging_config import test_logger


class TestSongMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        app_id: str = os.getenv("ID")
        api_key: str = os.getenv("KEY")

        cls.soundcharts = SoundCharts(app_id=app_id, api_key=api_key)

    def test_get_song_data(self):
        song_uuid: str = "7d534228-5165-11e9-9375-549f35161576"
        song = self.soundcharts.get_song_metadata_from_uuid(uuid=song_uuid)
        assert isinstance(song, Song)
        assert song.get_uuid() == song_uuid
        assert song.get_name() == "bad guy"
        test_logger.info(f"Song: {song.__dict__()}")
