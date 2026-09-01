Getting Started
===============

Tables
------

Painless creation of nice-looking tables of data for Python.

Starting simple
~~~~~~~~~~~~~~~

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable

    table = ANSITable("col1", "column 2 has a big header", "column 3")
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", 5.5, 6)
    table.row("ccccccc", 8.8, 9)
    table.print()

This produces a table with column widths automatically chosen, headings and column
data all right-justified (default).

By default output is printed to the console (``stdout``), but you can:

- Provide a ``file`` option to ``.print()`` to write to a specified output stream
- Obtain a multi-line string version with ``str(table)``

Borders
~~~~~~~

You can add borders made up of regular ASCII characters:

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable, Column
    table = ANSITable(
            Column("col1"),
            Column("column 2 has a big header"),
            Column("column 3"),
            border="ascii"
        )
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", 5.5, 6)
    table.row("ccccccc", 8.8, 9)
    table.print()

Or use ANSI box-drawing characters (supported by most terminal emulators):

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable, Column
    table = ANSITable(
            Column("col1"),
            Column("column 2 has a big header"),
            Column("column 3"),
            border="thick"
        )
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", 5.5, 6)
    table.row("ccccccc", 8.8, 9)
    table.print()

Other border options: ``"thin"``, ``"round"`` (thin with rounded corners), and ``"double"``.

Formatting and alignment
~~~~~~~~~~~~~~~~~~~~~~~~

Specify Python format strings for columns:

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable, Column
    table = ANSITable(
            Column("col1"),
            Column("column 2 has a big header", "{:.3g}"),
            Column("column 3", "{:-10.4f}")
        )
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", 5.5, 6)
    table.row("ccccccc", 8.8, 9)
    table.print()

Control alignment with ``colalign`` (data) and ``headalign`` (heading):
- ``"<"`` — left
- ``">"`` — right (default)
- ``"^"`` — center

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable, Column
    table = ANSITable(
            Column("col1", headalign="<"),
            Column("column 2 has a big header", colalign="^"),
            Column("column 3", colalign="<"),
            border="thick"
        )
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.row("ccccccc", 8.8, 9)
    table.print()

Add dividing lines with ``.rule()``:

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable, Column
    table = ANSITable(
            Column("col1", headalign="<"),
            Column("column 2 has a big header", colalign="^"),
            Column("column 3", colalign="<"),
            border="thick"
        )
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.rule()
    table.row("ccccccc", 8.8, -9)
    table.print()

Width constraints
~~~~~~~~~~~~~~~~~

Limit column width with the ``width`` argument:

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable, Column
    table = ANSITable(
            Column("col1", width=10),
            Column("column 2 has a big header", "{:.3g}"),
            Column("column 3", "{:-10.4f}")
        )
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", 5.5, 6)
    table.row("ccccccc", 8.8, 9)
    table.print()

Excess text is truncated with an ellipsis (U+2026). Disable with ``ellipsis=False``.

Color and styling
~~~~~~~~~~~~~~~~~

If you have the `colored <https://pypi.org/project/colored>`_ package installed,
you can set foreground/background colors and text styles (bold, reverse, underlined, dim):

.. code-block:: python

    from ansitable import ANSITable, Column, Cell
    table = ANSITable(
        Column("col1", headalign="<", colcolor="red", headstyle="underlined"),
        Column("column 2 has a big header", colalign="^", colstyle="bold"),
        Column("column 3", colalign="<", colbgcolor="green"),
        border="thick", bordercolor="blue"
    )
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.row("ccccccc", 8.8, -9)
    print(table)

Rendered output with colors:

.. raw:: html
   :file: ../_html_examples/color_example_1.html

Override styles per-row or per-cell:

.. code-block:: python

    from ansitable import ANSITable, Column, Cell
    table = ANSITable(
        Column("col1", headalign="<"),
        Column("column 2 has a big header", colalign="^"),
        Column("column 3", colalign="<"),
        border="thick"
    )
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", Cell(-5.5, bgcolor="blue"), 6, bgcolor="yellow")
    table.row("ccccccc", 8.8, 9)
    print(table)

Rendered output with per-cell colors:

.. raw:: html
   :file: ../_html_examples/color_example_2.html

Sorting
~~~~~~~

Sort table rows by a column:

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable
    table = ANSITable("name", "score")
    table.row("alice", 3)
    table.row("bob", 1)
    table.row("carol", 2)
    table.sort("score", key=int)
    table.print()

The ``.sort()`` method supports:

- ``column`` — column name (str) or index (int)
- ``key`` — optional function to transform values before comparison
- ``reverse`` — sort in descending order (default: False)

Horizontal rules (added with ``.rule()``) are silently dropped from sorted output.

Export formats
~~~~~~~~~~~~~~

Export tables to markup languages for use in documents:

**Markdown:**

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable
    table = ANSITable("col1", "column 2 has a big header", "column 3")
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.row("ccccccc", 8.8, -9)
    print(table.markdown())

**HTML:**

Supports CSS styling of cells and colors.

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable
    table = ANSITable("col1", "column 2 has a big header", "column 3")
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.row("ccccccc", 8.8, -9)
    print(table.html()[:200] + "...")

**reStructuredText (ReST) "simple table":**

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable
    table = ANSITable("col1", "column 2 has a big header", "column 3")
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.row("ccccccc", 8.8, -9)
    print(table.rest())

**LaTeX:**

Alignment options supported.

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable
    table = ANSITable("col1", "column 2 has a big header", "column 3")
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.row("ccccccc", 8.8, -9)
    print(table.latex()[:150] + "...")

**Wikitable (Wikipedia):**

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable
    table = ANSITable("col1", "column 2 has a big header", "column 3")
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.row("ccccccc", 8.8, -9)
    print(table.wikitable())

**CSV:**

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable
    table = ANSITable("col1", "column 2 has a big header", "column 3")
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.row("ccccccc", 8.8, -9)
    print(table.csv())

Matrices
--------

Display NumPy arrays as formatted matrices:

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSIMatrix
    import numpy as np

    np.random.seed(42)
    formatter = ANSIMatrix(style='thick')
    m = np.random.rand(4, 4) - 0.5
    formatter.print(m)

Add superscript and subscript suffixes:

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSIMatrix
    import numpy as np

    np.random.seed(42)
    formatter = ANSIMatrix(style='thick')
    m = np.random.rand(4, 4) - 0.5
    formatter.print(m, suffix_super='T', suffix_sub='3')

Pandas integration
------------------

Convert Pandas DataFrames to ANSITable:

.. runblock:: plain_python
    :no-prompt:

    import pandas as pd
    from ansitable import ANSITable

    df = pd.DataFrame({"calories": [420, 380, 390], "duration": [50, 40, 45]})
    table = ANSITable.Pandas(df, border="thin")
    table.print()

Convert ANSITable back to DataFrame:

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable
    import pandas as pd

    table = ANSITable("col1", "column 2 has a big header", "column 3")
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.row("ccccccc", 8.8, -9)

    df = table.pandas()
    print(df)

Column names are converted to valid Python identifiers (spaces → underscores),
allowing attribute access like ``df.column_2_has_a_big_header``.
Disable this with ``underscores=False``.
