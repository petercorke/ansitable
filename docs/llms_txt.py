"""Write llms.txt and llms-full.txt for the documentation site.

``llms.txt`` (see https://llmstxt.org) is a short Markdown file that tells AI assistants
what the package is, how to use it, and where its documentation lives. ``llms-full.txt``
is the whole documentation as plain text, so an assistant can read it in a single fetch.

The package is small, so ``llms.txt`` is mostly prose: the hand-written ``llms_intro.md``
(what it does, a quick start, key points, common mistakes) followed by a generated list
of links. ``llms-full.txt`` is this Sphinx site rendered by Sphinx's ``text`` builder, so
the autodoc API reference is included, in the order of the toctree in ``index.rst``.
Run after the HTML build::

    make html llms          # from docs/

The files are written into ``build/html`` so they are published with the site.
"""

from __future__ import annotations

import os
import re
import shutil

# Used only to re-invoke `sphinx-build`, resolved via shutil.which() below; this is a
# local/CI docs-build script, not code that runs against untrusted input.
import subprocess  # nosec B404
import sys
from importlib.metadata import metadata
from pathlib import Path

DOCS = Path(__file__).resolve().parent
SOURCE = DOCS / "source"
BUILD = DOCS / "build"
TEXT = BUILD / "text"
HTML = BUILD / "html"
INTRO = DOCS / "llms_intro.md"

# One-line descriptions of the pages listed in the toctree
PAGE_NOTES = {
    "index": "overview",
    "intro": "tutorial: creating tables, columns, rows, borders, sorting and export formats",
    "table": "API reference for ANSITable, Column, Cell and options()",
    "matrix": "API reference for ANSIMatrix, which pretty-prints NumPy arrays",
    "colors": "chart of the color names that can be used for text, backgrounds and borders",
}

# Links that belong in llms.txt but are not pages of this site
EXTRA_LINKS = [
    ("Source code", "https://github.com/petercorke/ansitable", "GitHub repository"),
    ("PyPI", "https://pypi.org/project/ansitable/", "install with pip install ansitable"),
    ("Changelog", "https://github.com/petercorke/ansitable/blob/main/CHANGELOG.md", "release history"),
    ("RVC ecosystem", "https://github.com/petercorke/rvc-ecosystem", "how ansitable relates to the Robotics and Machine Vision Toolboxes"),
    ("Contributing", "https://github.com/petercorke/ansitable/blob/main/AGENTS.md", "repo conventions and workflow, for agents working on ansitable's source code"),
]


def toctree_pages(index: Path) -> list[str]:
    """Document names listed in the toctrees of the master document, in order.

    :param index: the master document, ``index.rst``
    :return: document names such as ``"table"``
    """
    pages, in_toctree = [], False
    for line in index.read_text().splitlines():
        if line.startswith(".. toctree::"):
            in_toctree = True
        elif in_toctree and line.strip() and not line.startswith((" ", "\t")):
            in_toctree = False  # the directive's indented body has ended
        elif in_toctree and line.strip() and not line.strip().startswith(":"):
            pages.append(line.strip())
    return pages


def title(text: str) -> str:
    """The page title: the first non-blank line that isn't an overline of punctuation."""
    for line in text.splitlines():
        if line.strip() and not re.fullmatch(r"[*=\-~#^]+", line.strip()):
            return line.strip()
    return ""


def main() -> None:
    # Read the name, summary and documentation URL from the installed package's metadata
    # (built from pyproject.toml). Reading pyproject.toml directly would need tomllib,
    # which is Python 3.11+, and the Pages workflow builds the docs on 3.9.
    meta = metadata("ansitable")
    urls = dict(u.split(", ", 1) for u in meta.get_all("Project-URL"))
    base = urls["Documentation"].rstrip("/") + "/"
    name, summary = meta["Name"], meta["Summary"]

    # SPHINXBUILD matches the override convention of docs/Makefile's
    # `SPHINXBUILD ?= sphinx-build` -- resolved via shutil.which() to a full path.
    sphinxbuild_name = os.environ.get("SPHINXBUILD", "sphinx-build")
    sphinxbuild = shutil.which(sphinxbuild_name)
    if sphinxbuild is None:
        raise SystemExit(f"sphinx-build not found: {sphinxbuild_name!r}")
    subprocess.run(  # nosec B603 -- sphinxbuild resolved via shutil.which() above  # nosemgrep: python.lang.security.audit.dangerous-subprocess-use-audit.dangerous-subprocess-use-audit
        [sphinxbuild, "-q", "-b", "text", str(SOURCE), str(TEXT)],  # nosemgrep: python.lang.security.audit.dangerous-subprocess-use-tainted-env-args.dangerous-subprocess-use-tainted-env-args
        check=True,
    )
    pages = ["index"] + toctree_pages(SOURCE / "index.rst")
    texts = {p: (TEXT / f"{p}.txt").read_text() for p in pages}

    # llms.txt: prose introduction, then links
    index = [
        f"# {name}",
        "",
        f"> {summary}.",
        "",
        INTRO.read_text().strip(),
        "",
        "## Documentation",
        "",
        f"The whole documentation, including the API reference, is available as a single text file: [llms-full.txt]({base}llms-full.txt).",
        "",
        *(f"- [{title(texts[p])}]({base}{p}.html): {PAGE_NOTES.get(p, '')}" for p in pages),
        "",
        "## Optional",
        "",
        *(f"- [{label}]({url}): {note}" for label, url, note in EXTRA_LINKS),
        "",
    ]
    HTML.mkdir(parents=True, exist_ok=True)
    (HTML / "llms.txt").write_text("\n".join(index))

    # llms-full.txt: the prose introduction, then every page
    def block(url: str, body: str) -> str:
        return f"\n{'=' * 72}\nPage: {url}\n{'=' * 72}\n\n{body.strip()}\n"

    parts = [f"# {name}: {summary}\n\nDocumentation: {base}\n\n{INTRO.read_text().strip()}\n"]
    parts += [block(f"{base}{p}.html", texts[p]) for p in pages]
    full = re.sub(r"\n{3,}", "\n\n", "".join(parts))  # the text builder leaves runs of blank lines
    (HTML / "llms-full.txt").write_text(full)
    print(f"llms.txt: {len(pages)} pages; llms-full.txt: {len(full) // 1000} kB", file=sys.stderr)


if __name__ == "__main__":
    main()
