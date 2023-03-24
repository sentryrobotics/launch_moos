"""Sphinx configuration."""
project = "launch.moos"
author = "Russ Webber"
copyright = "2022, Russ Webber"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
