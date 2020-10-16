![PyPI - Downloads](https://img.shields.io/pypi/dm/ansitable)
[![PyPI version fury.io](https://badge.fury.io/py/ansitable.svg)](https://pypi.python.org/pypi/ansitable/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/petercorke/ansitable.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/petercorke/ansitable/context:python)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/ansitable)](https://pypi.python.org/pypi/ansitable/)
[![PyPI status](https://img.shields.io/pypi/status/ansitable.svg)](https://pypi.python.org/pypi/ansitable/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/petercorke/ansitable/graphs/commit-activity)
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/petercorke/ansitable/blob/master/LICENSE)

- GitHub repository: [https://github.com/petercorke/ansitable](https://github.com/petercorke/ansitable)
- Dependencies: [`colored`](https://pypi.org/project/colored)

# ANSI table

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
table.row("bbbbbbbbbbbbb", 5.5, 6)
table.row("ccccccc", 8.8, 9)
table.print()
```
yields

```
┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃col1          ┃ column 2 has a big header ┃ column 3 ┃
┣━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━┫
┃    aaaaaaaaa ┃            2.2            ┃ 3        ┃
┃bbbbbbbbbbbbb ┃            5.5            ┃ 6        ┃
┃      ccccccc ┃            8.8            ┃ 9        ┃
┗━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━┛
```
where we have left-justified the heading for column 1 and the data for column 3.

## Color
If you have the `colored` package installed then you can set the foreground and
background color and style (bold, reverse, underlined, dim) of the header and column data, as well as the border color.

```python
table = ANSITable(
    Column("col1", headalign="<", colcolor="red", headstyle="underlined"),  # CHANGE
    Column("column 2 has a big header", colalign="^", colstyle="reverse"),  # CHANGE
    Column("column 3", colalign="<", colbgcolor="green"),                   # CHANGE
    border="thick", bordercolor="blue"                                      # CHANGE
)
table.row("aaaaaaaaa", 2.2, 3)
table.row("bbbbbbbbbbbbb", 5.5, 6)
table.row("ccccccc", 8.8, 9)
table.print()
```

which yields

![colored table](https://github.com/petercorke/ansitable/raw/master/figs/colortable.png) 

It is also possible to change the color of individual cells in the table
by prefixing the value with a color enclosed in double angle brackets, for example `<<red>>`.

```python
table = ANSITable("col1", "column 2 has a big header", "column 3")
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("<<red>>bbbbbbbbbbbbb", 5.5, 6)
    table.row("<<blue>>ccccccc", 8.8, 9)
    table.print()
```

# All options

## ANSITable
These keyword arguments control the styling of the entire table.

| Keyword  | Default | Purpose |
|----      |----     |----    |
colsep | 2 | Gap between columns (in spaces)
offset | 0 | Gap at start of each row, shifts the table to the left
border | no border  | Border style
bordercolor | |Border color, see [possible values](https://pypi.org/project/colored)
ellipsis | True | Add an ellipsis if a wide column is truncated
header | True | Include the column header row
columns | | Specify the number of columns if `header=False` and no header name or `Column` arguments are given

## Column
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
