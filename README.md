[![PyPI version fury.io](https://badge.fury.io/py/ansitable.svg)](https://pypi.python.org/pypi/ansitable/)
[![PyPI status](https://img.shields.io/pypi/status/ansicolortags.svg)](https://pypi.python.org/pypi/ansitable/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/petercorke/ansitable/graphs/commit-activity)
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/petercorke/ansitable/blob/master/LICENSE)

- GitHub repository: [https://github.com/petercorke/ansitable](https://github.com/petercorke/ansitable)
- Dependencies: [`colored`](https://pypi.org/project/colored)

# ANSI table

This Python package allows you to simply create nice looking tables of data.

## Starting simple

```python
 1 |  table = TableFormat(
 2 |            Column("col1"),
 3 |            Column("column 2 has a big header"),
 4 |            Column("column 3")
 5 |          )
 6 | table.add("aaaaaaaaa", 2.2, 3)
 7 | table.add("bbbbbbbbbbbbb", 5.5, 6)
 8 | table.add("ccccccc", 8.8, 9)
 9 | table.print()

```
Lines 1-5 construct a `TableFormat` object and the arguments are a sequence of 
`Column` objects followed by `TableFormat` keyword arguments - there are none in this first example.  Since there are three column objects this this will be a 3-column table.
Lines 6-8 add rows, 3 data values for each row.

Line 9 prints the table and yields a tabular display
with column widths automatically chosen, and headings and column 
data all left-justified (default)

```
         col1  column 2 has a big header  column 3  
    aaaaaaaaa                        2.2         3  
bbbbbbbbbbbbb                        5.5         6  
      ccccccc                        8.8         9  
```

***
We can specify a Python `format()` style format string for any column - by default it
is the general formatting option `"{}"`

```python
table = TableFormat(
        Column("col1"),
        Column("column 2 has a big header", "{:.3g}"),  # CHANGE
        Column("column 3", "{:-10.4f}")
    )
table.add("aaaaaaaaa", 2.2, 3)
table.add("bbbbbbbbbbbbb", 5.5, 6)
table.add("ccccccc", 8.8, 9)
table.print()
```
which yields

```
         col1  column 2 has a big header    column 3  
    aaaaaaaaa                        2.2      3.0000  
bbbbbbbbbbbbb                        5.5      6.0000  
      ccccccc                        8.8      9.0000  
      
```
Alternatively we can specify a `formatter` argument which is a function that converts
the value to a string.


***
The data in column 1 is quite long, we might wish to set a maximum column width which
we can do using the `width` argument

```python
table = TableFormat(
        Column("col1", width=10),                      # CHANGE
        Column("column 2 has a big header", "{:.3g}"),
        Column("column 3", "{:-10.4f}")
    )
table.add("aaaaaaaaa", 2.2, 3)
table.add("bbbbbbbbbbbbb", 5.5, 6)
table.add("ccccccc", 8.8, 9)
table.print()
```
which yields


```
      col1  column 2 has a big header    column 3  
 aaaaaaaaa                        2.2      3.0000  
bbbbbbb...                        5.5      6.0000  
   ccccccc                        8.8      9.0000  

```
where we see that the data in column 1 has been truncated.

If you don't like the ellipsis you can turn it off, and get to see three more
charaters, with the `TableFormat` option `ellipsis=False`.

## Borders
We can add a table border made up of regular ASCII characters

```python
table = TableFormat(
        Column("col1"),
        Column("column 2 has a big header"),
        Column("column 3"),
        border="ascii"                          # CHANGE
    )
table.add("aaaaaaaaa", 2.2, 3)
table.add("bbbbbbbbbbbbb", 5.5, 6)
table.add("ccccccc", 8.8, 9)
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
table = TableFormat(
        Column("col1"),
        Column("column 2 has a big header"),
        Column("column 3"),
        border="thick"                           # CHANGE
    )
table.add("aaaaaaaaa", 2.2, 3)
table.add("bbbbbbbbbbbbb", 5.5, 6)
table.add("ccccccc", 8.8, 9)
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
which actually looks better on the console than it does in GitHub markdown.

Other border options include "thin", "rounded" (thin with round corners) and "double".

## Header and column alignment
We can change the alignment of data and heading for any column with the alignment flags "<" (left), 
">" (right) and "^" (centered).

```
table = TableFormat(
        Column("col1"),
        Column("column 2 has a big header", colalign="^"),  # CHANGE
        Column("column 3"),
        border="thick"
    )
table.add("aaaaaaaaa", 2.2, 3)
table.add("bbbbbbbbbbbbb", 5.5, 6)
table.add("ccccccc", 8.8, 9)
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
table = TableFormat(
        Column("col1", headalign="<"),                      # CHANGE
        Column("column 2 has a big header", colalign="^"),
        Column("column 3", colalign="<"),                   # CHANGE
        border="thick"
    )
table.add("aaaaaaaaa", 2.2, 3)
table.add("bbbbbbbbbbbbb", 5.5, 6)
table.add("ccccccc", 8.8, 9)
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
table = TableFormat(
    Column("col1", headalign="<", colcolor="red", headstyle="underlined"),  # CHANGE
    Column("column 2 has a big header", colalign="^", colstyle="reverse"),  # CHANGE
    Column("column 3", colalign="<", colbgcolor="green"),                   # CHANGE
    border="thick", bordercolor="blue"                                      # CHANGE
)
table.add("aaaaaaaaa", 2.2, 3)
table.add("bbbbbbbbbbbbb", 5.5, 6)
table.add("ccccccc", 8.8, 9)
table.print()
```

which yields

![colored table](https://github.com/petercorke/ansitable/raw/master/figs/colortable.png) 

# All options

## TableFormat
These keyword arguments control the styling of the entire table.

| Keyword  | Default | Purpose |
|----      |----     |----    |
colsep | 2 | Gap between columns (in spaces)
offset | 0 | Gap at start of each row, shifts the table to the left
border | no border  | Border style
bordercolor | |Border color, see [possible values](https://pypi.org/project/colored)
ellipsis | True | Add an ellipsis if a wide column is truncated

## Column
These keyword arguments control the styling of a single column.

| Keyword  | Default | Purpose |
|----      |----     |----    |
fmt | "{}" | format string for data in this column
width || maximum width 
colcolor || Text color 
colbgcolor || Text background color, see [possible values](https://pypi.org/project/colored)
colstyle  || Text style: "bold", "underlined", "reverse", "dim", "blink"
colalign | ">" | Text alignment: ">" (left), "<" (right), "^" (centered)
headcolor || Heading text color 
headbgcolor || Heading text background color, see [possible values](https://pypi.org/project/colored)
headstyle || Heading text style: "bold", "underlined", "reverse", "dim", "blink"
headalign | ">" | Heading text alignment: ">" (left), "<" (right), "^" (centered)
formatter | | A callable that maps the column value to a string
 
Note that many terminal emulators do not support the "blink" style.