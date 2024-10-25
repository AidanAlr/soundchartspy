import logging
import unittest

from soundchartspy.client import SoundCharts
from tests.logging_config import setup_logging

logger = setup_logging(log_level=logging.DEBUG)


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
        song = self.sc.song_by_platform_id(
            platform=self.platform, identifier=self.spotify_identifier
        )
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
            audience = self.sc.song_audience(
                uuid=self.demo_song_uuid, platform=platform
            )
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

    def test_get_song_radio_spins(self):
        spins = self.sc.song_radio_spins(
            uuid=self.demo_song_uuid, radio_slugs=["bbc-2", "bbc-london"]
        )
        assert spins is not None, "Failed to get radio spins"

    def test_get_song_radio_spin_count(self):
        countries = self.sc.song_radio_spin_count(
            uuid=self.demo_song_uuid, radio_slugs=["bbc-2", "bbc-london"]
        )
        assert countries is not None, "Failed to get radio spin countries"


class TestArtistMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        KEY = "soundcharts"
        ID = "soundcharts"
        cls.sc = SoundCharts(app_id=ID, api_key=KEY)
        cls.demo_artist_uuid = "11e81bcc-9c1c-ce38-b96b-a0369fe50396"

    def test_get_artist(self):
        artist = self.sc.artist(uuid=self.demo_artist_uuid)
        assert artist is not None, "Failed to get artist from uuid"

    def test_get_artist_by_platform_id(self):
        artist = self.sc.artist_by_platform_id(
            platform="spotify", identifier="6qqNVTkY8uBg9cP3Jd7DAH"
        )
        assert artist is not None, "Failed to get artist from platform id"

    def test_get_artist_ids(self):
        artist_ids = self.sc.artist_ids(uuid=self.demo_artist_uuid, platform="spotify")
        logger.debug(artist_ids)
        assert artist_ids is not None, "Failed to get artist ids"

    def test_get_artist_songs(self):
        songs = self.sc.artist_songs(uuid=self.demo_artist_uuid)
        assert songs is not None, "Failed to get artist songs"

    def test_get_artist_albums(self):
        albums = self.sc.artist_albums(uuid=self.demo_artist_uuid)
        assert albums is not None, "Failed to get artist albums"

    def test_get_artist_similar_artists(self):
        similar_artists = self.sc.artist_similar_artists(uuid=self.demo_artist_uuid)
        assert similar_artists is not None, "Failed to get similar artists"

    def test_get_artist_current_stats(self):
        stats = self.sc.artist_current_stats(uuid=self.demo_artist_uuid)
        assert stats is not None, "Failed to get current stats"

    def test_get_artist_audience(self):
        audience = self.sc.artist_audience(uuid=self.demo_artist_uuid)
        assert audience is not None, "Failed to get artist audience"

    def test_get_artist_local_audience(self):
        audience = self.sc.artist_local_audience(uuid=self.demo_artist_uuid)
        assert audience is not None, "Failed to get artist audience local"

    def test_get_artist_listeners_streams_views(self):
        listeners_streams_views = self.sc.artist_listeners_streams_views(
            uuid=self.demo_artist_uuid,
            platform="spotify",
        )
        assert (
            listeners_streams_views is not None
        ), "Failed to get artist listeners streams views"

    def test_get_artist_spotify_monthly_listeners_latest(self):
        listeners = self.sc.artist_spotify_monthly_listeners_latest(
            uuid=self.demo_artist_uuid
        )
        assert listeners is not None, "Failed to get artist spotify monthly listeners"

    def test_get_artist_spotify_listeners_by_month(self):
        listeners = self.sc.artist_spotify_monthly_listeners_by_month(
            uuid=self.demo_artist_uuid, year="2020", month="10"
        )
        assert listeners is not None, "Failed to get artist spotify listeners by month"

    def test_get_artist_retention(self):
        retention = self.sc.artist_retention(
            uuid=self.demo_artist_uuid,
        )
        assert retention is not None, "Failed to get artist retention"

    def test_get_artist_popularity(self):
        popularity = self.sc.artist_popularity(
            uuid=self.demo_artist_uuid,
        )
        assert popularity is not None, "Failed to get artist popularity"

    def test_get_artist_audience_report_latest(self):
        report = self.sc.artist_audience_report_latest(
            uuid=self.demo_artist_uuid,
        )
        assert report is not None, "Failed to get artist audience report latest"

    def test_get_artist_audience_report_dates(self):
        report = self.sc.artist_audience_report_dates(
            uuid=self.demo_artist_uuid,
        )
        assert report is not None, "Failed to get artist audience report dates"

    def test_get_artist_audience_report_by_date(self):
        report = self.sc.artist_audience_report_by_date(
            uuid=self.demo_artist_uuid,
            date="2020-09-20",
        )
        assert report is not None, "Failed to get artist audience report by date"

    def test_get_artist_short_videos(self):
        short_videos = self.sc.artist_short_videos(
            uuid=self.demo_artist_uuid,
        )
        assert short_videos is not None, "Failed to get artist short videos"

    def test_get_artist_short_video_audience(self):
        audience = self.sc.artist_short_video_audience(identifier="C74VMlhOf6K")
        assert audience is not None, "Failed to get artist short video audience"
