ansitable prints tabular data and NumPy matrices in a terminal with optional Unicode borders and ANSI color, and exports the same table to Markdown, HTML, LaTeX, reStructuredText, wikitable, CSV and Pandas. It is a small, pure-Python package (one module, `ansitable.table`) whose only dependency is the `colored` package, which provides the color names. It requires Python 3.9 or later. Install with `pip install ansitable`.

## When to use it

Reach for ansitable when a program needs to show **rows of values or a NumPy matrix as a neat table in a terminal**, optionally with color and box-drawing borders, and especially when the *same* table must also go into a document (Markdown, LaTeX, HTML, reStructuredText, wikitable, CSV) or a Pandas DataFrame. It is small and has one dependency, `colored`, which is optional for output without color.

It is not a general terminal UI toolkit (use `rich` or `textual` for live layouts, progress bars, panels), and it is not a data-wrangling library (use Pandas). It is a good fit when you want a plain, dependable table with a few lines of code.

## Quick start

```python
from ansitable import ANSITable, Column

table = ANSITable(
    Column("Name", headalign="<", colalign="<"),   # left-aligned
    Column("Score", fmt="{:.1f}", colcolor="blue"),
    border="thin",
)
table.row("Alice", 95)
table.row("Bob", 87.25)
table.row("Carol", 92, fgcolor="red")               # color override for one row
table.sort("Score", key=float, reverse=True)        # in place; returns the table
table.print()                                       # to a terminal, or table.print(file=f)
```

## Recipes

- **Print a table of results**: `t = ANSITable("name", "value", border="thin")`, then `t.row("a", 1.5)` for each row, then `t.print()`.
- **Show a NumPy matrix neatly**: `ANSIMatrix().print(A)`, or `str_ = ANSIMatrix(fmt="{:8.3f}").str(A)` for a string.
- **Show a Pandas DataFrame as a table**: `ANSITable.Pandas(df).print()`.
- **Put the same table in a Markdown or LaTeX document**: `t.markdown()`, `t.latex()`, or `t.export(file="results.md")`, which picks the format from the file extension.
- **Turn color and Unicode off for log files**: `ansitable.options(use_unicode=False, color=False)`.
- **Color one row or cell**: `t.row(..., fgcolor="red")`, or wrap a value in `Cell("text", fgcolor="red")`.

## Key points

- **Creating a table.** `ANSITable("a", "b", "c")` makes columns from strings (right-aligned, formatted with `"{}"`). Pass `Column(name, fmt=..., width=..., colcolor=..., colalign=..., headstyle=...)` objects instead for formatting and styling, or call `table.addcolumn(name, **kwargs)`. An alignment marker at the start of a column name, such as `"{<}Name"`, `"{^}Name"`, sets alignment in the string form.
- **Adding data.** `table.row(v1, v2, ...)` takes exactly one value per column and formats each with its column's `fmt` (a format string or a callable). `table.rule()` inserts a horizontal rule. `row()` accepts `fgcolor`, `bgcolor` and `style` overrides for the whole row; wrap a value in `Cell(text, fgcolor=..., bgcolor=..., style=...)` to override a single cell, or prefix a string value with `"<<red>>"` for an inline color.
- **Borders.** `border=` is one of `"ascii"`, `"thin"`, `"round"`, `"thick"`, `"double"`; the default is no border. `bordercolor=` colors it.
- **Colors and styles.** Colors are any of the 256 names accepted by the `colored` package (e.g. `"red"`, `"dodger_blue_1"`) or a `"#rrggbb"` hex string. Styles are `"bold"`, `"dim"`, `"underlined"`, `"blink"`, `"reverse"`. Colors and styles are validated when the `Column`, `Cell` or row is created, and raise `ValueError` there, not later at print time.
- **Output.** `table.print()` writes to stdout (or `file=`); `str(table)` gives the rendered text. Export methods return strings: `.markdown()`, `.rest()`, `.wikitable()`, `.html()`, `.latex()`, `.csv()`, and `.pandas()` which returns a DataFrame. `table.export(format, file=None, **kwargs)` is a single entry point to them: it returns the string, or writes to a path or open stream, and infers `format` from the file extension if omitted. Missing values (`None`) are shown as `na_rep` (default blank, set on the table or per `Column`) and `fmt` is not applied to them. `width=` on a `Column` truncates over-wide cells (with an ellipsis unless `ellipsis=False`); columns without a width never truncate. `ANSITable.Pandas(df, **kwargs)` goes the other way.
- **Global switches.** `ansitable.options(use_unicode, color=None)` turns Unicode box-drawing and ANSI color off (or on) for all tables; with Unicode off, borders fall back to `"ascii"`. Use it when output goes to a log file or a terminal that can't render them. Each table also has its own `color=` argument. If `colored` is not installed, color is silently disabled.
- **Sorting.** `table.sort(column, key=None, reverse=False)` sorts rows in place by column name or zero-based index. The default key compares the *formatted strings*, so pass `key=float` (or similar) to sort numerically. Rules inserted with `rule()` are dropped by a sort.
- **Matrices.** `ANSIMatrix(style="thin", fmt="{:< 10.3g}", squish=100)` is a formatter for NumPy arrays: `ANSIMatrix().print(m)` or `.str(m)` draws the array inside brackets. Elements smaller than `squish` times machine epsilon are shown as zero.

## Common mistakes

- `row()` must be given exactly as many values as there are columns, otherwise it raises `ValueError`.
- A `fmt` string is applied with `fmt.format(value)`, so it must suit the value's type (`"{:.1f}"` on a string fails).
- The text style and alignment arguments are strings (`"bold"`, `"<"`), not constants or enums.
- `ANSIMatrix` needs NumPy; `.pandas()` and `ANSITable.Pandas()` need Pandas. Neither is a dependency of the package.
