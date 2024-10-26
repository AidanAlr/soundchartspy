.. image:: https://raw.githubusercontent.com/AidanAlr/soundchartspy/main/docs/logo.png
   :alt: Soundchartspy
   :width: 100%

.. image:: https://img.shields.io/pypi/v/soundchartspy.svg
   :target: https://pypi.org/project/soundchartspy/
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/dm/soundchartspy
   :target: https://pypi.org/project/soundchartspy/
   :alt: PyPI Downloads

.. image:: https://github.com/AidanAlr/soundchartspy/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/AidanAlr/soundchartspy/actions/workflows/ci.yml
   :alt: Build Status

Installation
============
To install from PyPI, simply run:

.. code-block:: bash

    pip install soundchartspy

If you'd like to install the latest development version from source:

.. code-block:: bash

    pip install -e 'git+https://github.com/AidanAlr/soundchartspy.git#egg=soundchartspy'

Make sure to you have contacted SoundCharts and have purchased a plan providing the required app id and api key.

About
=====
`soundchartspy` is a wrapper package enabling easier pythonic interaction with the SoundCharts API (`SoundCharts API documentation <https://doc.api.soundcharts.com/api/v2/doc>`_).
It provides an easy interface to retrieve data about songs, artists, charts and more.
This package is not affiliated with or endorsed by SoundCharts, though an active SoundCharts API subscription is required to use the package.

For detailed information, consult the documentation hosted on Read the Docs.

Documentation
=============
Documentation for `soundchartspy` is located at https://soundchartspy.readthedocs.io/.

Example Usage
=============

Here's an example of how to use `soundchartspy`:

.. code-block:: python

    from soundchartspy.client import SoundCharts
    from soundchartspy.data import Song, Album

    # Initialize the SoundCharts client
    sc = SoundCharts(api_key='your_api_key', app_id='your_app_id')

    # Get the song by UUID
    song: Song = sc.song(song_uuid='7d534228-5165-11e9-9375-549f35161576')
    print("Song Name: {}, Artists: {}".format(song.name, song.artists))

    # Get the song audience on Spotify
    audience_data: dict = sc.song_audience(song.uuid, 'spotify')
    print("Spotify Audience: {}".format(audience_data))

    # Get the song albums
    albums: list[Album] = sc.song_albums(song.uuid)
    print("Albums: {}".format(albums))

API Implementation Status
==========================

✅ Completed Methods
--------------------
* Song Methods
    * ``SoundCharts.song()``
    * ``SoundCharts.song_by_isrc()``
    * ``SoundCharts.song_by_platform_id()``
    * ``SoundCharts.song_ids()``
    * ``SoundCharts.song_albums()``
    * ``SoundCharts.song_audience()``
    * ``SoundCharts.song_spotify_popularity()``
    * ``SoundCharts.song_chart_entries()``
    * ``SoundCharts.song_playlist_entries()``
    * ``SoundCharts.song_radio_spins()``
    * ``SoundCharts.song_radio_spin_count()``

* Artist Methods (Partially Implemented)
    * ``SoundCharts.artist()``
    * ``SoundCharts.artist_by_platform_id()``
    * ``SoundCharts.artist_ids()``
    * ``SoundCharts.artist_songs()``
    * ``SoundCharts.artist_albums()``
    * ``SoundCharts.artist_similar_artists()``
    * ``SoundCharts.artist_current_stats()``
    * ``SoundCharts.artist_audience()``
    * ``SoundCharts.artist_local_audience()``
    * ``SoundCharts.artist_listeners_streams_views()``
    * ``SoundCharts.artist_spotify_monthly_listeners_latest()``
    * ``SoundCharts.artist_spotify_monthly_listeners_by_month()``
    * ``SoundCharts.artist_retention()``
    * ``SoundCharts.artist_popularity()``
    * ``SoundCharts.artist_audience_report_latest()``
    * ``SoundCharts.artist_audience_report_dates()``
    * ``SoundCharts.artist_audience_report_by_date()``
    * ``SoundCharts.artist_short_videos()``
    * ``SoundCharts.artist_short_video_audience()``


📋 Pending Implementation
-------------------------
* Remaining Artist Methods
* Chart Methods
* Playlist Methods
* Search Methods
* Album Methods
* Radio Methods
* TikTok Methods
* User Methods

Development Notes
-----------------
* All implemented methods follow the official SoundCharts API specification
* Unit tests available for implemented methods

Found a Bug?
============
Issues are tracked via GitHub at the `project issue page <https://github.com/AidanAlr/soundchartspy/issues>`_.

Contributing
============
#. `Check for open issues <https://github.com/AidanAlr/soundchartspy/issues>`_ on the project issue page, or open a new issue to start a discussion about a feature or bug.
#. Fork the `soundchartspy repository on GitHub <https://github.com/AidanAlr/soundchartspy>`_ to start making changes.
#. Add a test case to ensure that the bug is fixed or the feature is implemented correctly.
#. Submit your pull request for review.