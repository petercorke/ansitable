# ANSITable

<div align="center">
  <img src="https://github.com/petercorke/ansitable/raw/master/figs/ansi_logo.png" width="300">
  <br>
  <strong>Pretty tables and matrices for Python</strong>
  <br><br>

[![PyPI version](https://img.shields.io/pypi/v/ansitable?style=for-the-badge&color=blue)](https://pypi.org/project/ansitable/)
  [![Documentation](https://img.shields.io/badge/Docs-View_Online-blue?style=for-the-badge)](https://petercorke.github.io/ansitable)

  <p>
    <a href="https://github.com/petercorke/ansitable">GitHub</a> •
    <a href="https://anaconda.org/conda-forge/ansitable">Conda</a> •
    <a href="#quick-example">Quick example</a>
  </p>
</div>

---

### Status & Project Health
[![Build Status](https://github.com/petercorke/ansitable/actions/workflows/master.yml/badge.svg)](https://github.com/petercorke/ansitable/actions/workflows/master.yml)
[![Downloads](https://static.pepy.tech/badge/ansitable/month)](https://pepy.tech/projects/ansitable)
![Python Version](https://img.shields.io/pypi/pyversions/ansitable.svg)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/e43d7415ba234101be49128fd0d354fa)](https://app.codacy.com/gh/petercorke/ansitable/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

### Ecosystem & Dependencies
[![A Python Robotics Package](https://raw.githubusercontent.com/petercorke/robotics-toolbox-python/main/.github/svg/py_collection.min.svg)](https://github.com/petercorke/robotics-toolbox-python)
[![QUT Centre for Robotics Open Source](https://github.com/qcr/qcr.github.io/raw/master/misc/badge.svg)](https://qcr.github.io)

## Quick example

```python
from ansitable import ANSITable

table = ANSITable("Name", "Score", border="thin")
table.row("Alice", 95)
table.row("Bob", 87)
table.row("Carol", 92)
table.print()
```

Output:

```
┌───────┬───────┐
│ Name  │ Score │
├───────┼───────┤
│ Alice │    95 │
│   Bob │    87 │
│ Carol │    92 │
└───────┴───────┘
```

## Features

- **Unicode and ANSI colors** — Beautiful output in any ANSI-capable terminal
- **7 export formats** — Markdown, HTML, LaTeX, reStructuredText, Wikitable, CSV, Pandas
- **Rich styling** — Colors, backgrounds, text styles (bold, underlined, etc.), alignment, width control
- **Sorting** — Sort tables by any column, with optional key function
- **Pandas integration** — Convert DataFrames to/from ANSITable
- **Matrix formatting** — Pretty-print NumPy arrays with brackets and styles
- **Flexible API** — Simple string-based or detailed Column-based column specification

## Installation

```bash
pip install ansitable
```

Optional dependency for colors:

```bash
pip install colored
```

## Documentation

See the [comprehensive documentation](https://petercorke.github.io/ansitable) for tutorials,
examples, and API reference.
