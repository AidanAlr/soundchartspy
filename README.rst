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

Make sure to set up your API key and app ID in order to access the SoundCharts API. Detailed setup instructions can be found in the documentation.

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

Found a Bug?
============
Issues are tracked via GitHub at the `project issue page <https://github.com/AidanAlr/soundchartspy/issues>`_.

Contributing
============
#. `Check for open issues <https://github.com/AidanAlr/soundchartspy/issues>`_ on the project issue page, or open a new issue to start a discussion about a feature or bug.
#. Fork the `soundchartspy repository on GitHub <https://github.com/AidanAlr/soundchartspy>`_ to start making changes.
#. Add a test case to ensure that the bug is fixed or the feature is implemented correctly.
#. Submit your pull request for review.

Please do not update the library version in `CHANGELOG.rst` or `soundchartspy/__init__.py`. The maintainer will handle this during release.
