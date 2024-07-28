[![PyPI version fury.io](https://badge.fury.io/py/ansitable.svg)](https://pypi.python.org/pypi/ansitable/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/ansitable)](https://pypistats.org/packages/ansitable)
[![Anaconda version](https://anaconda.org/conda-forge/ansitable/badges/version.svg)](https://anaconda.org/conda-forge/ansitable)
[![pyversions](https://img.shields.io/pypi/pyversions/ansitable)](https://pypi.python.org/pypi/ansitable/)
[![PyPI status](https://img.shields.io/pypi/status/ansitable.svg)](https://pypi.python.org/pypi/ansitable/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/petercorke/ansitable/graphs/commit-activity)
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/petercorke/ansitable/blob/master/LICENSE)

- GitHub repository: [https://github.com/petercorke/ansitable](https://github.com/petercorke/ansitable)
- Dependencies: [`colored`](https://pypi.org/project/colored)

# Synopsis

Painless creation of nice-looking [tables of data](#tables) or [matrices](#matrices) in Python.

What's new:

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

# Tables

Painless creation of nice-looking tables of data for Python.

![colored table](https://github.com/petercorke/ansitable/raw/master/figs/colortable.png) 

## Starting simple

```python
 1 | from ansitable import ANSITable, Column
 2 |
 3 | table = ANSITable("col1", "column 2 has a big header", "column 3")
 4 | table.row("aaaaaaaaa", 2.2, 3)
 5 | table.row("bbbbbbbbbbbbb", 5.5, 6)
 6 | table.row("ccccccc", 8.8, 9)
 7 | table.print()

```
Line 3 constructs an `ANSITable` object and the arguments are a sequence of 
column names followed by `ANSITable` keyword arguments - there are none in this first example.  Since there are three column names this this will be 
a 3-column table.
Lines 4-6 add rows, 3 data values for each row.

Line 7 prints the table and yields a tabular display
with column widths automatically chosen, and headings and column 
data all right-justified (default)

```
         col1  column 2 has a big header  column 3  
    aaaaaaaaa                        2.2         3  
bbbbbbbbbbbbb                        5.5         6  
      ccccccc                        8.8         9  
```

By default output is printed to the console (`stdout`) but we can also:

- provide a `file` option to `.print()` to allow writing to a specified output stream, the
default is `stdout`.
- obtain a multi-line string version of the entire table as `str(table)`.

The more general solution is to provide a sequence of `Column` objects which 
allows many column specific options to be given, as we shall see later. 
For now though, we could rewrite the example above as:

```python
table = ANSITable(
        Column("col1"),
        Column("column 2 has a big header"),
        Column("column 3")
    )
```

or as

```python
table = ANSITable()
table.addcolumn("col1")
table.addcolumn("column 2 has a big header")
table.addcolumn("column 3")
```
where the keyword arguments to `.addcolumn()` are the same as those for
`Column` and are given below.

***
We can specify a [Python `format()` style format string](https://docs.python.org/3/library/string.html#formatspec) for any column - by default it
is the general formatting option `"{}"`.
You may choose to left or right justify values via the format string, `ansitable` provides control over how those resulting strings are justified within the column.

```python
table = ANSITable(
        Column("col1"),
        Column("column 2 has a big header", "{:.3g}"),  # CHANGE
        Column("column 3", "{:-10.4f}")
    )
table.row("aaaaaaaaa", 2.2, 3)
table.row("bbbbbbbbbbbbb", 5.5, 6)
table.row("ccccccc", 8.8, 9)
table.print()
```
which yields

```
         col1  column 2 has a big header    column 3  
    aaaaaaaaa                        2.2      3.0000  
bbbbbbbbbbbbb                        5.5      6.0000  
      ccccccc                        8.8      9.0000  
      
```
Alternatively we can specify the format argument as a function that converts
the value to a string.


***
The data in column 1 is quite long, we might wish to set a maximum column width which
we can do using the `width` argument

```python
table = ANSITable(
        Column("col1", width=10),                      # CHANGE
        Column("column 2 has a big header", "{:.3g}"),
        Column("column 3", "{:-10.4f}")
    )
table.row("aaaaaaaaa", 2.2, 3)
table.row("bbbbbbbbbbbbb", 5.5, 6)
table.row("ccccccc", 8.8, 9)
table.print()
```
which yields


```
      col1  column 2 has a big header    column 3  
 aaaaaaaaa                        2.2      3.0000  
bbbbbbbbb…                        5.5      6.0000  
   ccccccc                        8.8      9.0000  

```
where we see that the data in column 1 has been truncated.

If you don't like the ellipsis you can turn it off, and get to see one more
character, with the `ANSITable` option `ellipsis=False`.  The Unicode ellipsis
character u+2026 is used.

## Borders
We can add a table border made up of regular ASCII characters

```python
table = ANSITable(
        Column("col1"),
        Column("column 2 has a big header"),
        Column("column 3"),
        border="ascii"                          # CHANGE
    )
table.row("aaaaaaaaa", 2.2, 3)
table.row("bbbbbbbbbbbbb", 5.5, 6)
table.row("ccccccc", 8.8, 9)
table.print()
```
which yields

```
+--------------+---------------------------+----------+
|         col1 | column 2 has a big header | column 3 |
+--------------+---------------------------+----------+
|    aaaaaaaaa |                       2.2 |        3 |
|bbbbbbbbbbbbb |                       5.5 |        6 |
|      ccccccc |                       8.8 |        9 |
+--------------+---------------------------+----------+
```
***
Or we can construct a border using the [ANSI box-drawing characters](https://en.wikipedia.org/wiki/Box-drawing_character) which are supported by most terminal
emulators

```python
table = ANSITable(
        Column("col1"),
        Column("column 2 has a big header"),
        Column("column 3"),
        border="thick"                           # CHANGE
    )
table.row("aaaaaaaaa", 2.2, 3)
table.row("bbbbbbbbbbbbb", 5.5, 6)
table.row("ccccccc", 8.8, 9)
table.print()
```
which yields

```
┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃         col1 ┃ column 2 has a big header ┃ column 3 ┃
┣━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━┫
┃    aaaaaaaaa ┃                       2.2 ┃        3 ┃
┃bbbbbbbbbbbbb ┃                       5.5 ┃        6 ┃
┃      ccccccc ┃                       8.8 ┃        9 ┃
┗━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━┛
```
_Note: this actually looks better on the console than it does in GitHub markdown._

Other border options include "thin", "rounded" (thin with round corners) and "double".

## Header and column alignment
We can change the alignment of data and heading for any column with the alignment flags `"<"` (left), 
`">"` (right) and `"^"` (centered).

```python
table = ANSITable(
        Column("col1"),
        Column("column 2 has a big header", colalign="^"),  # CHANGE
        Column("column 3"),
        border="thick"
    )
table.row("aaaaaaaaa", 2.2, 3)
table.row("bbbbbbbbbbbbb", 5.5, 6)
table.row("ccccccc", 8.8, 9)
table.print()
```
which yields


```
┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃         col1 ┃ column 2 has a big header ┃ column 3 ┃
┣━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━┫
┃    aaaaaaaaa ┃            2.2            ┃        3 ┃
┃bbbbbbbbbbbbb ┃            5.5            ┃        6 ┃
┃      ccccccc ┃            8.8            ┃        9 ┃
┗━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━┛
```
where the data for column 2 has been centered.
***
Heading and data alignment for any column can be set independently

```python
table = ANSITable(
        Column("col1", headalign="<"),                      # CHANGE
        Column("column 2 has a big header", colalign="^"),
        Column("column 3", colalign="<"),                   # CHANGE
        border="thick"
    )
table.row("aaaaaaaaa", 2.2, 3)
table.row("bbbbbbbbbbbbb", -5.5, 6)
table.row("ccccccc", 8.8, -9)
table.print()
```
yields

```
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃          col1 ┃ column 2 has a big header ┃ column 3 ┃
┣━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━┫
┃     aaaaaaaaa ┃                       2.2 ┃        3 ┃
┃ bbbbbbbbbbbbb ┃                      -5.5 ┃        6 ┃
┃       ccccccc ┃                       8.8 ┃       -9 ┃
┗━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━┛
```
where we have left-justified the heading for column 1 and the data for column 3.

We can easily add a dividing line
```python
table = ANSITable(
        Column("col1", headalign="<"),
        Column("column 2 has a big header", colalign="^"),
        Column("column 3", colalign="<"),
        border="thick"
    )
table.row("aaaaaaaaa", 2.2, 3)
table.row("bbbbbbbbbbbbb", -5.5, 6)
table.rule()                                                # CHANGE
table.row("ccccccc", 8.8, -9)
table.print()
```
yields

```
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃          col1 ┃ column 2 has a big header ┃ column 3 ┃
┣━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━┫
┃     aaaaaaaaa ┃                       2.2 ┃        3 ┃
┃ bbbbbbbbbbbbb ┃                      -5.5 ┃        6 ┃
┣━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━┫
┃       ccccccc ┃                       8.8 ┃       -9 ┃
┗━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━┛
```


## Color
If you have the `colored` package installed then you can set the foreground and
background color and style (bold, reverse, underlined, dim) of the header and column data, as well as the border color.

```python
table = ANSITable(
    Column("col1", headalign="<", colcolor="red", headstyle="underlined"),      # CHANGE
    Column("column 2 has a big header", colalign="^", colstyle="reverse"),      # CHANGE
    Column("column 3", colalign="<", colbgcolor="green"),                       # CHANGE
    border="thick", bordercolor="blue"                                          # CHANGE
)
   table = ANSITable(
        Column("col1", headalign="^", colcolor="red", headstyle="underlined"),  # CHANGE
        Column("column 2 has a big header", colalign="^"),                      # CHANGE
        Column("column 3", colalign="<", colbgcolor="green", fmt="{: d}"),      # CHANGE
        border="thick",
        bordercolor="blue",
        colsep=2,
    )
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6, bgcolor="yellow")                        # CHANGE
    table.row("ccccccc", 8.8, -9)
    table.print()
```

which yields

![colored table](https://github.com/petercorke/ansitable/raw/master/figs/colortable.png) 

It is possible the change the color of a single row of the table by

```python
table.row("aaaaaaaaa", 2.2, 3)
table.row("bbbbbbbbbbbbb", 5.5, 6, bgcolor="red")
table.row("ccccccc", 8.8, 9)
```

which yields

![colored table](https://github.com/petercorke/ansitable/raw/master/figs/colortable2.png) 

It is also possible to change the color of individual cells in the table
by prefixing the value with a color enclosed in double angle brackets, for example `<<red>>`.

```python
table = ANSITable("col1", "column 2 has a big header", "column 3")
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("<<red>>bbbbbbbbbbbbb", 5.5, 6)
    table.row("<<blue>>ccccccc", 8.8, 9)
    table.print()
```

## All options

### ANSITable
These keyword arguments control the styling of the entire table.

| Keyword  | Default | Purpose |
|----      |----     |----    |
colsep | 2 | Gap between columns (in spaces)
offset | 0 | Gap at start of each row, shifts the table to the left
border | no border  | Border style: 'ascii', 'thin', 'thick', 'double'
bordercolor | |Border color, see [possible values](https://pypi.org/project/colored)
ellipsis | True | Add an ellipsis if a wide column is truncated
header | True | Include the column header row
columns | | Specify the number of columns if `header=False` and no header name or `Column` arguments are given
color | True | Enable color 

- Color is only possible if the `colored` package is installed
- If `color` is False then no color escape sequences will be emitted, useful 
  override for tables included in Sphinx documentation.

### Column
These keyword arguments control the styling of a single column.

| Keyword  | Default | Purpose |
|----      |----     |----    |
fmt | `"{}"` | format string for the column value, or a callable that maps the column value to a string
width || maximum column width, excess will be truncated
colcolor || Text color, see [possible values](https://pypi.org/project/colored)
colbgcolor || Text background color, see [possible values](https://pypi.org/project/colored)
colstyle  || Text style: "bold", "underlined", "reverse", "dim", "blink"
colalign | `">"` | Text alignment: `">"` (left), `"<"` (right), `"^"` (centered)
headcolor || Heading text color, see [possible values](https://pypi.org/project/colored)
headbgcolor || Heading text background color, see [possible values](https://pypi.org/project/colored)
headstyle || Heading text style: "bold", "underlined", "reverse", "dim", "blink"
headalign | `">"` | Heading text alignment: `">"` (left), `"<"` (right), `"^"` (centered)

Note that many terminal emulators do not support the "blink" style.

### Row
These keyword arguments control the styling of a single row.

| Keyword  | Default | Purpose |
|----      |----     |----    |
fgcolor || Text color, see [possible values](https://pypi.org/project/colored)
bgcolor || Text background color, see [possible values](https://pypi.org/project/colored)
style  || Text style: "bold", "underlined", "reverse", "dim", "blink"

# Output in other tabular formats

The main use for this package is to generate tables on the console that are easy to read, but
sometimes you might want the table in a different format to include in
documentation.

```python
table = ANSITable("col1", "column 2 has a big header", "column 3")
table.row("aaaaaaaaa", 2.2, 3)
table.row("bbbbbbbbbbbbb", -5.5, 6)
table.row("ccccccc", 8.8, -9)
table.print()
```

can be rendered into Markdown

```
table.markdown()

|          col1 | column 2 has a big header | column 3 |
| ------------: | ------------------------: | -------: |
|     aaaaaaaaa |                       2.2 |        3 |
| bbbbbbbbbbbbb |                      -5.5 |        6 |
|       ccccccc |                       8.8 |       -9 |
```
or LaTex

```
table.latex()

\begin{tabular}{ |r|r|r| }\hline
\multicolumn{1}{|r|}{col1} & \multicolumn{1}{|r|}{column 2 has a big header} & \multicolumn{1}{|r|}{column 3}\\\hline\hline
aaaaaaaaa & 2.2 & 3 \\
bbbbbbbbbbbbb & -5.5 & 6 \\
ccccccc & 8.8 & -9 \\
\hline
\end{tabular}
```
or CSV format

```
table.csv()

col1,column 2 has a big header,column 3
aaaaaaaaa,2.2,3
bbbbbbbbbbbbb,-5.5,6
ccccccc,8.8,-9
```
The delimter character can be set, but defaults to comma.

In all cases the method returns a string. Column alignment is supported for the LaTeX
and markdown cases.
MarkDown doesn't allow the header to have different alignment to the data.

## Pandas integration

Pandas is THE tool to use for tabular data so we support conversions in both directions.

To convert a Pandas DataFrame to an ANSItable is just

```
import pandas as pd

df = pd.DataFrame({"calories": [420, 380, 390], "duration": [50, 40, 45]})
table = ANSITable.Pandas(df, border="thin")
table.print()

┌──────────┬──────────┐
│ calories │ duration │
├──────────┼──────────┤
│      420 │       50 │
│      380 │       40 │
│      390 │       45 │
└──────────┴──────────┘
```
``Pandas()`` is a static method that acts like a constructor. This is the simplest way to display CSV format data in an ANSItable by using Pandas ``read_csv()`` to load the data into a ``DataFrame``.

To export an ANSItable as a Pandas DataFrame is simply

```
table = ANSITable("col1", "column 2 has a big header", "column 3")
table.row("aaaaaaaaa", 2.2, 3)
table.row("bbbbbbbbbbbbb", -5.5, 6)
table.row("ccccccc", 8.8, -9)

df = table.pandas()
print(df)

            col1 column_2_has_a_big_header column_3
0      aaaaaaaaa                       2.2        3
1  bbbbbbbbbbbbb                      -5.5        6
2        ccccccc                       8.8       -9
```
Note that the column names have been modified, spaces changed to underscores, which
allows the columns to be accessed as attributes:

```
print(df.column_2_has_a_big_header.to_string())

0     2.2
1    -5.5
2     8.8
```
which shows the column as a Pandas `Series` object. This column name-changing behaviour can be disabled by passing ``underscores=False``.


# Matrices

Painless creation of nice-looking matrices for Python.


We can create a formatter for NumPy arrays (1D or 2D)

```python
from ansitable import ANSIMatrix
formatter = ANSIMatrix(style='thick')
```

and then use it to format a NumPy array

```python
m = np.random.rand(4,4) - 0.5
m[0,0] = 1.23456e-14
formatter.print(m)
```

yields

```
┏                                           ┓
┃ 0         -0.385     -0.106      0.296    ┃
┃ 0.0432     0.339      0.119     -0.468    ┃
┃ 0.405     -0.306      0.0165    -0.439    ┃
┃ 0.203      0.4       -0.499     -0.487    ┃
┗                                           ┛
```

we can also add suffixes


```python
formatter.print(m, suffix_super='T', suffix_sub='3')
```

yields

```
┏                                           ┓T
┃ 0         -0.239      0.186     -0.414    ┃
┃ 0.49       0.215     -0.0148     0.0529   ┃
┃ 0.0473     0.0311     0.45       0.394    ┃
┃-0.192      0.193     -0.455      0.0302   ┃
┗                                           ┛3
```

By default output is printed to the console (stdout) but we can also:

* provide a `file` option to `.print()` to allow writing to a specified output stream, the default is `stdout`.
* obtain a multi-line string version of the entire table using the `.str()` method
instead of `.print()`.

The formatter takes additional arguments to control the numeric format and to 
control the suppression of very small values.

### ANSIMatrix
These keyword arguments control the overall styling and operation of the formatter.

| Keyword  | Default | Purpose |
|----      |----     |----    |
style | `"thin"` | `"thin"`, `"round"`, `"thick"`, `"double"`
fmt | `"{:< 10.3g}"` | format for each element
squish | True | set small elements to zero
squishtol | 100 | elements less than `squishtol * eps` are set to zero

### Formatter
A formatter takes additional arguments to the styling for a particular call.

| Keyword  | Default | Purpose |
|----      |----     |----    |
suffix_super | `""` | superscript suffix text
suffix_sub | `""` | subscript suffix text
