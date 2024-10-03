# -- Path setup --------------------------------------------------------------
import os
import sys


sys.path.insert(0, os.path.abspath(".."))

import soundchartspy

# -- Project information -----------------------------------------------------
project = "soundchartspy"
author = "Aidan Alrawi"
copyright = "2024, Aidan Alrawi"
release = soundchartspy.__version__
version = soundchartspy.__version__

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",  # Include autodoc extension for auto-generating documentation
    "sphinx.ext.viewcode",  # View the source code in the generated docs
    "sphinx.ext.napoleon",  # Support for Google-style and NumPy-style docstrings
]

templates_path = ["_templates"]
exclude_patterns = ["_build"]

# -- Options for HTML output -------------------------------------------------

html_theme = "furo"  # Use the Furo theme, like Django-Storages
html_static_path = ["_static"]
html_title = f"{project} {release} Documentation"

# -- Autodoc settings --------------------------------------------------------

autodoc_member_order = "bysource"  # Keep member order the same as in source code
autodoc_typehints = "description"  # Show type hints in the description of parameters
autodoc_inherit_docstrings = True  # Inherit docstrings from parent classes

# Napoleon settings (for better docstring format)
napoleon_google_docstring = True
napoleon_numpy_docstring = False

# -- Options for LaTeX output --------------------------------------------------

latex_documents = [
    (
        "index",
        "soundchartspy.tex",
        "soundchartspy Documentation",
        "Aidan Alrawi",
        "manual",
    ),
]

# -- Options for manual page output --------------------------------------------

man_pages = [
    ("index", "soundchartspy", "soundchartspy Documentation", ["Aidan Alrawi"], 1)
]

# -- Options for Epub output ---------------------------------------------------

epub_title = "soundchartspy"
epub_author = "Aidan Alrawi"
epub_publisher = "Aidan Alrawi"
epub_copyright = "2024, Aidan Alrawi"
