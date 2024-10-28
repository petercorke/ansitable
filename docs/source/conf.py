# ansitable
# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

# sys.path.insert(0, os.path.abspath('.'))
# defined relative to configuration directory which is where this file conf.py lives
# sys.path.append(os.path.abspath("exts"))


# -- Project information -----------------------------------------------------

project = "Pretty tables and matrices for Python"
copyright = "2021-, Peter Corke"
author = "Peter Corke"

try:
    import ansitable

    version = ansitable.__version__
except AttributeError:
    import re

    with open("../../pyproject.toml", "r") as f:
        m = re.compile(r'version\s*=\s*"([0-9\.]+)"').search(f.read())
        version = m[1]

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.coverage",
    "sphinx.ext.intersphinx",
    "sphinx.ext.inheritance_diagram",
    "sphinx_autodoc_typehints",
    "sphinx_favicon",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["test_*"]

autodoc_member_order = "bysource"

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"
html_show_sourcelink = True

html_theme = "sphinx_rtd_theme"
# html_theme = 'alabaster'
# html_theme = 'pyramid'
# html_theme = 'sphinxdoc'

github_url = "https://github.com/petercorke/ansitable"

html_theme_options = {
    "github_host": "gitlab.com",
    "github_user": "petercorke",
    "github_repo": "bdsim",
    "display_github": True,
    "github_version": "HEAD",
    "logo_only": False,
    "display_version": True,
    "prev_next_buttons_location": "both",
    "analytics_id": "G-11Q6WJM565",
}

html_logo = "../../figs/ansi_logo.png"
html_last_updated_fmt = "%d-%b-%Y"
autoclass_content = "class"
html_show_sourcelink = True

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

# -------- RVC maths notation -------------------------------------------------------#


# -------- Options favicon -------------------------------------------------------#

html_static_path = ["_static"]
# create favicons online using https://favicon.io/favicon-converter/
favicons = [
    {
        "rel": "icon",
        "sizes": "16x16",
        "static-file": "favicon-16x16.png",
        "type": "image/png",
    },
    {
        "rel": "icon",
        "sizes": "32x32",
        "static-file": "favicon-32x32.png",
        "type": "image/png",
    },
    {
        "rel": "apple-touch-icon",
        "sizes": "180x180",
        "static-file": "apple-touch-icon.png",
        "type": "image/png",
    },
    {
        "rel": "android-chrome",
        "sizes": "192x192",
        "static-file": "android-chrome-192x192.png ",
        "type": "image/png",
    },
    {
        "rel": "android-chrome",
        "sizes": "512x512",
        "static-file": "android-chrome-512x512.png ",
        "type": "image/png",
    },
]

# -------- Options InterSphinx -------------------------------------------------------#

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("http://docs.scipy.org/doc/numpy/", None),
    "pandas": ("http://pandas.pydata.org/pandas-docs/dev", None),
}
