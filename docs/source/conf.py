# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys
import re
from datetime import date

# Defined relative to configuration directory which is where this file conf.py lives
# sys.path.append(os.path.abspath("exts"))

# -------- Project information -------------------------------------------------------#

project = "ANSITable"
copyright = f"{date.today().year}, Peter Corke"
author = "Peter Corke"

# Parse version number out of pyproject.toml
_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
with open(os.path.join(_root, "pyproject.toml"), encoding="utf-8") as f:
    pyproject_src = f.read()
    m = re.search(r'^version\s*=\s*"([0-9.]*)"', pyproject_src, re.MULTILINE)
    version = m.group(1) if m else "unknown"

# -------- General configuration -----------------------------------------------------#

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.mathjax",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx_favicon",
    "sphinx_autorun",
    "sphinx_copybutton",
]

autosummary_generate = True
autodoc_member_order = "bysource"

# sphinx-autorun configuration
autorun_languages = {
    "pycon": "python3",
    "pycon_prefix_chars": 4,
    "pycon_show_source": False,
    "plain_python": "python3",
    "plain_python_prefix_chars": 0,
    "plain_python_show_source": False,
    "plain_python_runfirst": "from ansitable import set_options\nset_options(color=True, unicode=True)",
}

# copybutton configuration: strip >>> and ... prompts when copying
copybutton_prompt_text = r">>> |\.\.\. "

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

exclude_patterns = ["test_*"]

# -------- Options for HTML output ---------------------------------------------------#

html_theme = "sphinx_rtd_theme"

html_theme_options = {
    "logo_only": False,
    "prev_next_buttons_location": "None",
    "analytics_id": "G-11Q6WJM565",
    "style_external_links": False,
    "navigation_depth": 5,
}

html_logo = "../../figs/ansi_logo.png"
html_last_updated_fmt = "%d-%b-%Y"
html_show_sourcelink = False
show_authors = True
html_show_sphinx = False

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
default_role = "py:obj"

# -------- Options for LaTeX/PDF output ----------------------------------------------#

latex_engine = "xelatex"

latex_elements = {
    "papersize": "a4paper",
    "fncychap": "\\usepackage{fncychap}",
}

# -------- Options favicon -------------------------------------------------------#

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
        "static-file": "android-chrome-192x192.png",
        "type": "image/png",
    },
    {
        "rel": "android-chrome",
        "sizes": "512x512",
        "static-file": "android-chrome-512x512.png",
        "type": "image/png",
    },
]

# -------- Options InterSphinx -------------------------------------------------------#

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "pandas": ("https://pandas.pydata.org/docs", None),
}


# -------- Post-build processing: Render HTML table output -------------------#

def render_html_output(app, exception):
    """Render HTML table output from runblock directives."""
    if exception or app.builder.name != "html":
        return

    import re
    import html as html_module
    from pathlib import Path

    # Process all HTML files in the build output
    outdir = Path(app.outdir)
    for html_file in outdir.rglob("*.html"):
        content = html_file.read_text(encoding="utf-8")
        modified = False

        # Find code blocks that contain HTML table output (from print(table.html()))
        # Look for pattern: >>&gt;&gt;&gt; print(table.html(...))
        # followed by the HTML table output (starting with &lt;table)
        def replace_html_output(match):
            nonlocal modified
            full_block = match.group(0)

            # Extract the content between <pre><span></span> and </pre>
            match_inner = re.search(r"<span></span>(.*?)</pre>", full_block, re.DOTALL)
            if not match_inner:
                return full_block

            inner = match_inner.group(1)

            # Unescape HTML entities
            unescaped = html_module.unescape(inner)

            # Check if there's an HTML table in the output
            if "<table" not in unescaped:
                return full_block

            # Extract the HTML table from the output
            # Pattern: >>> print(table.html(...)) followed by <table>...</table>
            table_match = re.search(r"(<table.*?</table>)", unescaped, re.DOTALL)
            if not table_match:
                return full_block

            html_table = table_match.group(1)
            modified = True

            # Replace the entire code block with the rendered HTML table
            wrapper = f'<div style="margin: 20px 0;">{html_table}</div>'
            return wrapper

        # Replace code blocks with rendered HTML tables
        content = re.sub(
            r'<div class="highlight-plain_python[^>]*>.*?<pre>.*?</pre></div>',
            replace_html_output,
            content,
            flags=re.DOTALL,
        )

        if modified:
            html_file.write_text(content, encoding="utf-8")


def setup(app):
    """Register the post-build event handler."""
    app.connect("build-finished", render_html_output)
