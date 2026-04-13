CHANGELOG


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