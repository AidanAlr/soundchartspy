# Configuration file for the Sphinx documentation builder.
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import os
import sys

sys.path.insert(0, os.path.abspath('..'))  # Adjust as necessary
import soundchartspy  # Assuming your package is named this way

# -- Project information -----------------------------------------------------
project = 'soundchartspy'
author = 'Aidan Alrawi'
copyright = '2024, Aidan Alrawi'
release = '0.0.1'
version = '0.0.1'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = ['_build']

# -- Options for HTML output -------------------------------------------------

html_theme = 'furo'  # Use the Furo theme, like Django-Storages
html_static_path = ['_static']
# Set the HTML title explicitly
html_title = f"{project} {release} Documentation"

# -- Extension configuration -------------------------------------------------

# Autodoc settings
autodoc_member_order = 'bysource'

# -- Options for LaTeX output --------------------------------------------------

latex_documents = [
    ('index', 'soundchartspy.tex', 'soundchartspy Documentation', 'Aidan Alrawi', 'manual'),
]

# -- Options for manual page output --------------------------------------------

man_pages = [
    ('index', 'soundchartspy', 'soundchartspy Documentation', ['Aidan Alrawi'], 1)
]

# -- Options for Epub output ---------------------------------------------------

epub_title = 'soundchartspy'
epub_author = 'Aidan Alrawi'
epub_publisher = 'Aidan Alrawi'
epub_copyright = '2024, Aidan Alrawi'

# HTML options specific to Furo theme (optional, but can be customized)
# You can also add custom styles or logo if needed:
# html_logo = None
# html_favicon = None
# html_theme_options = {}
