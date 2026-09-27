CHANGELOG

1.1.1:

- **Fixed:** renaming the default branch `master` → `main` broke the README's logo image
  (a hardcoded `raw/master/...` GitHub URL, which 404s once the branch is gone — unlike
  `blob/master/...` page links, GitHub doesn't redirect raw-content URLs after a branch
  rename) and silently stopped CI/docs-deploy from running at all, since `master.yml`'s
  `push`/`pull_request` triggers still watched `branches: [master]`. Both now point at
  `main`. This release exists mainly to get a correctly-rendering README back onto PyPI,
  since 1.1.0's is permanently baked with the broken link.

1.1.0:

- Complete rewrite of the online documentation
- Added a searchable, click-to-copy 256-color swatch reference page, generated at
  doc-build time directly from `colored`'s own palette table so it can't go stale.
- Added a `{X}`/`{XY}` alignment shorthand prefix for column names, e.g.
  `ANSITable("{^<}col1", "{^}col2")`, no more needing full `Column` objects
  just to set alignment.
- Classifier and test for Python 3.14
- **Fixed:** a cell combining `fgcolor` with `bgcolor`/`style` lost its background
  color in the padding after the text — an inner ANSI reset fired before the padding
  was written, clearing formatting an outer wrap had just applied. Mainly visible on
  header cells, since `headcolor`/`headbgcolor`/`headstyle` are commonly combined
  together; data cells that only set `bgcolor` were unaffected.
- **Fixed:** `ANSITable.html()` wrote `colored`'s color specifiers (e.g. `"grey_37"`)
  straight into CSS unmodified — only the handful of names that happen to also be CSS
  keywords worked, everything else produced invalid CSS that browsers silently drop.
  Colors are now translated to real `#rrggbb` hex via `colored`'s own palette table.
  Also, `headstyle`/`colstyle`/per-cell `style` was never referenced anywhere in
  `html()` despite the docstring claiming style support; now mapped to CSS
  (`font-weight`, `text-decoration`, `opacity`), with `reverse` swapping the resolved
  foreground/background colors.
- All 110 unit tests passing.

1.0.1:

- **Fixed:** `rule()` rows crashed `csv()`/`html()`/`latex()` and rendered as garbled
  blank rows in `markdown()`/`rest()`/`wikitable()`. Now `latex()` renders a rule as
  `\hline` and `html()` as a spanning `<hr>`; the other formats cleanly skip the row,
  matching how `.sort()` already treats it.
- **Fixed:** `ANSITable.html()` ignored a `Column`'s `colcolor`/`colbgcolor` defaults,
  only ever applying per-row/`Cell` color overrides.
- **Fixed:** `ansitable.__version__` was undefined; now reads the installed package
  version via `importlib.metadata`.
- **Fixed:** the GitHub Pages documentation build — several examples in the "Getting
  Started" guide were rendering raw Python tracebacks (missing numpy/pandas in the
  docs build, a call to a nonexistent function, an unsupported directive option) and
  the "Color and styling" section was showing malformed HTML source instead of a
  rendered table.
- Removed two dead `border=` values (`"thick-thin"`, `"double-thin"`) that crashed
  with `IndexError` if used; never actually implemented.
- Modernized type hints across the public API: `Literal` types for `border=`,
  `style=`, and alignment parameters with their valid values now documented in the
  signature; removed docstring `:type:`/`:rtype:` fields made redundant by the
  annotations; converted docstring examples to `.. runblock::` directives (matching
  the other Peter Corke toolboxes), which also corrected several examples whose
  hand-written expected output no longer matched reality.
- All 86 unit tests passing.

1.0.0:

- **First stable release.** Backward compatible with 0.11.7.
- Modernized type hints: modern union syntax (X | Y), modern collections (list[], dict[])
- Added return type hints to all export methods and internal methods
- Added comprehensive Getting Started documentation (intro.rst)
- Improved README (now GitHub-optimized with detailed tutorial moved to docs)
- Full support for sorting tables by column (see `ANSITable.sort()`)
- All 28 unit tests passing. Code quality verified.
- Comprehensive Sphinx documentation with autodoc, multiple rendering formats

0.11.6:

- update project metadata
- improve documentation
- refactor color handling in table module

0.11.3:

- add repr methods for ANSITable and Column objects
- clarified imports in the README.md examples
- changed to src layout and hatch project manager


0.11.2:

- export a table in HTML format
- export a table in ReST format
- export a table in wikitable format
- improved format override for a single cell, using `Cell`

0.11.0:

- [Pandas integration](https://pandas.pydata.org). Convert a Pandas DataFrame to a table, or vice versa
- export a table in CSV format
- added unit tests for the various conversion methods

0.10.0:

- `colsep` is now the number of padding spaces on each side of the cell data.  `colsep=1` means one space on the left and one on the right, previously this was achieved by `colsep=2`.
- the padding now has `bgcolor`
- the method `rule()` adds a horizontal dividing line across the table (actually this is from a few releases ago)
- `row()` has arguments to override the fgcolor, bgcolor and style of all columns in the row, useful for highlighting a row.

0.9.10:

- fix problems due to changes with [`colored`](https://pypi.org/project/colored) 2.x
  
0.9.5:

- methods to format table as MarkDown or LaTeX
- work with Python 3.4

0.9.3:

- create matrices as well as tables
- option to suppress color output