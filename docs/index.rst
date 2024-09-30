soundchartspy
=============

soundchartspy is a Python wrapper package for the paid API from SoundCharts. This package is not affiliated with SoundCharts and is not endorsed by them. However, it is built upon their API and can be used assuming you have a paid subscription to their service.

.. toctree::
   :maxdepth: 2
   :titlesonly:

   usage
   installation
   data
   client

Installation
************

To install the `soundchartspy` package, use pip:

.. code-block:: bash

    pip install soundchartspy

Ensure you have a valid API key and app ID from SoundCharts to use this package.

Usage
*****

To use the `soundchartspy` package, initialize the SoundCharts client with your credentials:

.. code-block:: python

    from soundchartspy.client import SoundCharts
    from soundchartspy.data import Song, Album

    # Initialize the SoundCharts client
    sc = SoundCharts(api_key='your_api_key', app_id='your_app_id')

    # Get the song by uuid
    song: Song = sc.song(song_uuid='7d534228-5165-11e9-9375-549f35161576')
    print("Song Name: {}, Artists: {}".format(song.name, song.artists))

    # Get the song audience on spotify
    audience_data: dict = sc.song_audience(song.uuid, 'spotify')
    print("Spotify Audience: {}".format(audience_data))

    # Get the song albums
    albums: list[Album] = sc.song_albums(song.uuid)
    print("Albums: {}".format(albums))

Contributing
************

To contribute to `soundchartspy`, `create a fork`_ on GitHub. Clone your fork, make some changes, and submit a pull request.

.. _create a fork: https://github.com/AidanAlr/soundchartspy

Issues
******

Use the GitHub `issue tracker`_ for `soundchartspy` to submit bugs, issues, and feature requests.

.. _issue tracker: https://github.com/AidanAlr/soundchartspy/issues

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
