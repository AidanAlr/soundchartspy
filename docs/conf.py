# Configuration file for the Sphinx documentation builder.
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import os
import sys

sys.path.insert(0, os.path.abspath('..'))  # Adjust as necessary

# -- Project information -----------------------------------------------------

project = 'soundchartspy'
author = 'Aidan Alrawi'
copyright = '2024, Aidan Alrawi'
release = '0.0.1'
version = '0.0.1'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.todo',
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

html_theme = 'alabaster'  # You can switch this to 'sphinx_rtd_theme' for Read the Docs
html_static_path = ['_static']

# -- Extension configuration -------------------------------------------------

# Autodoc settings
autodoc_member_order = 'bysource'
