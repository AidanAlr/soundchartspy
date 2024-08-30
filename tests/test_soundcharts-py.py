import unittest

from sounchartspy.soundchartspy.soundcharts import SoundCharts

KEY = "soundcharts"
ID = "soundcharts"


class TestSongMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sc = SoundCharts(app_id=ID, api_key=KEY)
        cls.uuid = "7d534228-5165-11e9-9375-549f35161576"
        cls.isrc = "USAT22003425"

    def test_get_song_from_uuid(self):
        song = self.sc.get_song_metadata_from_uuid(song_uuid=self.uuid)
        assert song is not None, "Failed to get song from uuid"

    def test_get_song_from_isrc(self):
        song = self.sc.get_song_metadata_from_isrc(isrc=self.isrc)
        assert song is not None, "Failed to get song from isrc"

    def test_get_song_from_platform_id(self):
        platform = "spotify"
        platform_id = "7A9rdAz2M6AjRwOa34jxIP"
        song = self.sc.get_song_by_platform_id(platform=platform, platform_id=platform_id)
        assert song is not None, "Failed to get song from platform id"

    def test_get_song_platform_ids(self):
        offset = 0
        limit = 10
        song_platform_ids = self.sc.get_song_platform_ids(song_uuid=self.uuid, offset=offset, limit=limit)
        assert song_platform_ids is not None, "Failed to get song platform ids"

    def test_get_song_albums(self):
        albums = self.sc.get_song_albums(song_uuid=self.uuid, type="all", offset=0, limit=10, sort_by="releaseDate",
                                         sort_order="desc")
        assert albums is not None, "Failed to get song albums"

    def test_get_song_audience(self):
        audience = self.sc.get_song_audience(song_uuid=self.uuid, platform="spotify")
        assert audience is not None, "Failed to get song audience"

        audience = self.sc.get_song_audience(song_uuid=self.uuid, platform="spotify", end_date="2021-07-01")
        assert audience is not None, "Failed to get song audience with end date"

    def test_get_artist_follower_count_from_uuid(self):
        artist_uuid = "11e81bcc-9c1c-ce38-b96b-a0369fe50396"
        platform = "spotify"
        follower_count = self.sc.get_artist_follower_count_from_uuid(artist_uuid=artist_uuid, platform=platform)
        assert follower_count is not None, "Failed to get artist follower count"