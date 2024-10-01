import unittest

from soundchartspy.client import SoundCharts


class TestSongMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        KEY = "soundcharts"
        ID = "soundcharts"
        cls.sc = SoundCharts(app_id=ID, api_key=KEY)
        cls.demo_song_uuid = "7d534228-5165-11e9-9375-549f35161576"
        cls.isrc = "USAT22003425"
        cls.platform = "spotify"
        cls.spotify_identifier = "7A9rdAz2M6AjRwOa34jxIP"

    def test_get_song(self):
        song = self.sc.song(uuid=self.demo_song_uuid)
        assert song is not None, "Failed to get song from uuid"

    def test_get_song_by_isrc(self):
        song = self.sc.song_by_isrc(isrc=self.isrc)
        assert song is not None, "Failed to get song from isrc"

    def test_get_song_by_platform_id(self):
        song = self.sc.song_by_platform_id(platform=self.platform, identifier=self.spotify_identifier)
        assert song is not None, "Failed to get song from platform id"

    def test_get_song_ids(self):
        song_ids = self.sc.song_ids(uuid=self.demo_song_uuid, platform=self.platform)
        assert song_ids is not None, "Failed to get song ids"

    def test_get_song_albums(self):
        albums = self.sc.song_albums(uuid=self.demo_song_uuid)
        assert albums is not None, "Failed to get song albums"

    def test_get_song_audience(self):
        platforms = ["spotify"]
        for platform in platforms:
            audience = self.sc.song_audience(uuid=self.demo_song_uuid, platform=platform)
            assert audience is not None, "Failed to get song audience"

    def test_get_spotify_popularity(self):
        popularity = self.sc.song_spotify_popularity(uuid=self.demo_song_uuid)
        assert popularity is not None, "Failed to get spotify popularity"

    def test_get_song_chart_entries(self):
        entries = self.sc.song_chart_entries(uuid=self.demo_song_uuid)
        assert entries is not None, "Failed to get song chart entries"

    def test_get_song_playlist_entries(self):
        entries = self.sc.song_playlist_entries(uuid=self.demo_song_uuid)
        assert entries is not None, "Failed to get playlist entries"

#  def test_get_song_radio_spins(self):
#      spins = self.sc.song_radio_spins(uuid=self.demo_song_uuid)
#      assert spins is not None, "Failed to get radio spins"
#
# def test_get_song_radio_spin_countries(self):
#      countries = self.sc.song_radio_spin_countries(uuid=self.demo_song_uuid)
#      assert countries is not None, "Failed to get radio spin countries"
