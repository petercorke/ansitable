[![PyPI version fury.io](https://badge.fury.io/py/ansitable.svg)](https://pypi.python.org/pypi/ansitable/)
[![Anaconda version](https://anaconda.org/conda-forge/ansitable/badges/version.svg)](https://anaconda.org/conda-forge/ansitable)
[![pyversions](https://img.shields.io/pypi/pyversions/ansitable)](https://pypi.python.org/pypi/ansitable/)
[![Build Status](https://github.com/petercorke/ansitable/actions/workflows/master.yml/badge.svg)](https://github.com/petercorke/ansitable/actions?query=workflow%3Abuild)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/petercorke/ansitable/graphs/commit-activity)
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/petercorke/ansitable/blob/master/LICENSE)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/ansitable)](https://pypistats.org/packages/ansitable)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/e43d7415ba234101be49128fd0d354fa)](https://app.codacy.com/gh/petercorke/ansitable/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

![ANSITable logo](https://github.com/petercorke/ansitable/raw/master/figs/ansi_logo.png)

# ANSITable

Pretty tables and matrices for Python

- [GitHub repository](https://github.com/petercorke/ansitable)
- [Documentation](https://petercorke.github.io/ansitable)
- [PyPI](https://pypi.org/project/ansitable)
- [Conda](https://anaconda.org/conda-forge/ansitable)

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
