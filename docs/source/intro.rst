Getting Started
****************

Tables
========

Painless creation of nice-looking tables of data for Python.

Starting simple
----------------

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable

    table = ANSITable("Name", "Age", "Admission score")
    table.row("Alice", 25, 95.1)
    table.row("Bob", 30, 87.3)
    table.row("Carol", 28, 92.1)
    table.row("Michelangelo", 35, 88.0)
    table.print()

.. note:: The lines prefixed by ``# →`` indicate the **output**  of the preceding code block.
    They are commented to distinguish them from lines of executable code.
    This also means that if you
    copy and paste this code, using the icon in the top-right corner of the code block,  these
    output lines will not be executed.


The result is a table with column widths automatically chosen, headings and column
data all right-justified (default).

By default output is written to the console (``stdout``), but you can also:

- write to a specific file by passing the ``file`` option to ``.print()``
- obtain the table as a multi-line string using ``str(table)``

Borders
--------

You can add borders made up of regular ASCII characters:

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable

    table = ANSITable("Name", "Age", "Admission score", border="ascii")
    table.row("Alice", 25, 95.1)
    table.row("Bob", 30, 87.3)
    table.row("Carol", 28, 92.1)
    table.row("Michelangelo", 35, 88.0)
    table.print()

Or use ANSI box-drawing characters (supported by most terminal emulators):

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable

    table = ANSITable("Name", "Age", "Admission score", border="thick")
    table.row("Alice", 25, 95.1)
    table.row("Bob", 30, 87.3)
    table.row("Carol", 28, 92.1)
    table.row("Michelangelo", 35, 88.0)
    table.print()

Other border options: ``"thin"``, ``"round"`` (thin with rounded corners), and ``"double"``.

Column options
---------------

To gain additional control, you can create a table with ``Column`` objects, which allow
you to specify formatting, alignment, and width constraints for each column:

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable, Column

    table = ANSITable(
        Column("Name", headalign="^", colalign="<"),
        Column("Age", headalign="^", colalign="<"),
        Column("Admission score", headalign="^", colalign=">"),
        border="thin")
    table.row("Alice", 25, 95.1)
    table.row("Bob", 30, 87.3)
    table.row("Carol", 28, 92.1)
    table.row("Michelangelo", 35, 88.0)
    table.print()

Control alignment with ``colalign`` (data) and ``headalign`` (heading):

- ``"<"`` - left
- ``">"`` - right (default)
- ``"^"`` - center

There is also a shorthand way to control header and column alignment using a format string in the column headers.

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable, Column

    table = ANSITable("{<}Name", "{^<}Age", "{^>}Admission score", border="thin")
    table.row("Alice", 25, 95.1)
    table.row("Bob", 30, 87.3)
    table.row("Carol", 28, 92.1)
    table.row("Michelangelo", 35, 88.0)
    table.print()

If the header string starts with ``{XY}`` where ``X`` and ``Y`` are alignment
characters, these apply to the header and column alignment respectively.
If the header string starts with ``{X}`` then ``X`` is used as the alignment character for both the header and the column.  

Width constraints
------------------

Column width can be limited using the ``width`` argument:

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable, Column

    table = ANSITable(
        Column("Name", headalign="^", colalign="<", width=10),
        Column("Age", headalign="^", colalign="<"),
        Column("Admission score", headalign="^", colalign=">"),
        border="thin")
    table.row("Alice", 25, 95.1)
    table.row("Bob", 30, 87.3)
    table.row("Carol", 28, 92.1)
    table.row("Michelangelo", 35, 88.0)
    table.print()

Excess text is truncated with an ellipsis (U+2026). Disable with ``ellipsis=False`` which simply
truncates the field.


Field formatting
-----------------

For numeric columns we can specify Python format strings that control how
the cell values are rendered. Here we display age in hexadecimal and the score 
with 2 digits of precision.

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable, Column

    table = ANSITable(
        Column("Name", headalign="^", colalign="<", width=10),
        Column("Age", "0x{:x}", headalign="^", colalign="<"),
        Column("Admission score", "{:.3f}", headalign="^", colalign=">"),
        border="thin")
    table.row("Alice", 25, 95.1)
    table.row("Bob", 30, 87.3)
    table.row("Carol", 28, 92.1)
    table.row("Michelangelo", 35, 88.0)
    table.print()

Dividing lines
---------------

A dividing line, spanning the entire table, can be added between rows using ``.rule()``.

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable, Column

    table = ANSITable(
        Column("Name", headalign="^", colalign="<"),
        Column("Age", headalign="^", colalign="<"),
        Column("Admission score", headalign="^", colalign=">"),
        border="thin")
    table.row("Alice", 25, 95.1)
    table.row("Bob", 30, 87.3)
    table.rule() # dividing line
    table.row("Carol", 28, 92.1)
    table.row("Michelangelo", 35, 88.0)
    table.print()

Sorting
--------

A table can be sorted on any heading string, and the result is a new table
with its rows sorted.

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable, Column

    table = ANSITable(
        Column("Name", headalign="^", colalign="<"),
        Column("Age", headalign="^", colalign="<"),
        Column("Admission score", headalign="^", colalign=">"),
        border="thin")
    table.row("Alice", 25, 95.1)
    table.row("Bob", 30, 87.3)
    table.row("Carol", 28, 92.1)
    table.row("Michelangelo", 35, 88.0)
    newtable = table.sort("Age", key=int)
    newtable.print()

Parameters to the ``.sort()`` method include:

- ``column`` - column name (str) or index (int)
- ``key`` - optional function to transform values before comparison
- ``reverse`` - sort in descending order (default: False)

Horizontal rules (added with ``.rule()``) are silently dropped from sorted output.


Color and styling
------------------

If the `colored <https://pypi.org/project/colored>`_ package is installed,
you can set foreground/background colors and text styles (bold, reverse, underlined, dim) for
header cells, data rows or data cells.

See :doc:`colors` for a searchable, swatch-illustrated reference of all 256 color names this package
accepts (or ``colored``'s 
`own list <https://dslackw.gitlab.io/colored/tables/colors/#full-chart-256-foreground-and-background-colors>`_).

Header cell color and format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here we use a dict to set the style for the header cells: bold white text on a dark grey
background.

.. code-block:: python

    from ansitable import ANSITable, Column

    heading = dict(headstyle="bold", headcolor="white", headbgcolor="grey_53")
    table = ANSITable(
        Column("Name", headalign="^", colalign="<", **heading),
        Column("Age", headalign="^", colalign="<", **heading),
        Column("Admission score", headalign="^", colalign=">", **heading),
        border="thin")
    table.row("Alice", 25, 95.1)
    table.row("Bob", 30, 87.3)
    table.row("Carol", 28, 92.1)
    table.row("Michelangelo", 35, 88.0)
    table.print()

The color escape characters can't be displayed from an inline documentation
code block, they are separately rendered to HTML and included here:

.. raw:: html
   :file: ../_html_examples/color_example_1.html

Column format
~~~~~~~~~~~~~~~

Extending the above example so that the *Name* column has its background color set to light blue

.. code-block:: python

    from ansitable import ANSITable, Column

    heading = dict(headstyle="bold", headcolor="white", headbgcolor="grey_53")
    table = ANSITable(
        Column("Name", headalign="^", colalign="<", colbgcolor="sky_blue_3", **heading),
        Column("Age", headalign="^", colalign="<", **heading),
        Column("Admission score", headalign="^", colalign=">", **heading),
        border="thin")
    table.row("Alice", 25, 95.1)
    table.row("Bob", 30, 87.3)
    table.row("Carol", 28, 92.1)
    table.row("Michelangelo", 35, 88.0)
    table.print()

.. raw:: html
   :file: ../_html_examples/color_example_2.html

Row format
~~~~~~~~~~~~

We can apply the format flags to an entire row.  Here we set rows where the score is greater than 90
to red background with white text.

.. code-block:: python

    from ansitable import ANSITable, Column

    heading = dict(headstyle="bold", headcolor="white", headbgcolor="grey_53")
    table = ANSITable(
        Column("Name", headalign="^", colalign="<", colbgcolor="sky_blue_3", **heading),
        Column("Age", headalign="^", colalign="<", **heading),
        Column("Admission score", headalign="^", colalign=">", **heading),
        border="thin")
    table.row("Alice", 25, 95.1, bgcolor="red_3b", fgcolor="white")
    table.row("Bob", 30, 87.3)
    table.row("Carol", 28, 92.1, bgcolor="red_3b", fgcolor="white")
    table.row("Michelangelo", 35, 88.0)
    table.print()

.. raw:: html
   :file: ../_html_examples/color_example_3.html

These row formats take priority over formats set for a column.  

Cell format
~~~~~~~~~~~~

We can override the styling of a particular cell using ``Cell`` instances.
Extending the example above, we highlight score cells over 90 with a red background and white text.

.. code-block:: python

    from ansitable import ANSITable, Column, Cell

    heading = dict(headstyle="bold", headcolor="white", headbgcolor="grey_53")
    table = ANSITable(
        Column("Name", headalign="^", colalign="<", colbgcolor="sky_blue_3", **heading),
        Column("Age", headalign="^", colalign="<", **heading),
        Column("Admission score", headalign="^", colalign=">", **heading),
        border="thin")
    table.row("Alice", 25, Cell(95.1, bgcolor="red_3b", fgcolor="white"))
    table.row("Bob", 30, 87.3)
    table.row("Carol", 28, Cell(92.1, bgcolor="red_3b", fgcolor="white"))
    table.row("Michelangelo", 35, 88.0)
    table.print()

.. raw:: html
   :file: ../_html_examples/color_example_4.html

Cell formats will take priority over formats set for a row or a column.  


Export formats
---------------

Tables can be exported, as a string, in a number of common markup languages for use in documents.
Capabilities for alignment, text formatting and color vary across these markup formats.

Markdown
~~~~~~~~~

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable
    table = ANSITable("Name", "Age", "Admission score")
    table.row("Alice", 25, 95.1)
    table.row("Bob", 30, 87.3)
    table.row("Carol", 28, 92.1)
    table.row("Michelangelo", 35, 88.0)
    print(table.markdown())


HTML
~~~~~

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable
    table = ANSITable("Name", "Age", "Admission score")
    table.row("Alice", 25, 95.1)
    table.row("Bob", 30, 87.3)
    table.row("Carol", 28, 92.1)
    table.row("Michelangelo", 35, 88.0)
    print(table.html())

The table will be rendered according to the document's CSS settings.
We can override them for this table by passing additional parameters
to ``html()``

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable
    table = ANSITable("Name", "Age", "Admission score")
    table.row("Alice", 25, 95.1)
    table.row("Bob", 30, 87.3)
    table.row("Carol", 28, 92.1)
    table.row("Michelangelo", 35, 88.0)
    html = table.html(
        table="border-collapse: collapse; margin: 10px 0; border: 3px solid blue;",
        th="padding: 8px; border: 1px solid #ddd; font-weight: bold;",
        td="padding: 8px; border: 1px solid #ddd;",
    )
    print(html)

reStructuredText (ReST) "simple table"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable
    table = ANSITable("Name", "Age", "Admission score")
    table.row("Alice", 25, 95.1)
    table.row("Bob", 30, 87.3)
    table.row("Carol", 28, 92.1)
    table.row("Michelangelo", 35, 88.0)
    print(table.rest())

LaTeX
~~~~~~~


.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable
    table = ANSITable("Name", "Age", "Admission score")
    table.row("Alice", 25, 95.1)
    table.row("Bob", 30, 87.3)
    table.row("Carol", 28, 92.1)
    table.row("Michelangelo", 35, 88.0)
    print(table.latex())

Alignment options are supported.


Wikitable (Wikipedia)
~~~~~~~~~~~~~~~~~~~~~~~

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable
    table = ANSITable("Name", "Age", "Admission score")
    table.row("Alice", 25, 95.1)
    table.row("Bob", 30, 87.3)
    table.row("Carol", 28, 92.1)
    table.row("Michelangelo", 35, 88.0)
    print(table.wikitable())

CSV
~~~~~

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable
    table = ANSITable("Name", "Age", "Admission score")
    table.row("Alice", 25, 95.1)
    table.row("Bob", 30, 87.3)
    table.row("Carol", 28, 92.1)
    table.row("Michelangelo", 35, 88.0)
    print(table.csv())

Matrices
=========

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
===================

Convert Pandas ``DataFrames`` to ``ANSITable``:

.. runblock:: plain_python
    :no-prompt:

    import pandas as pd
    from ansitable import ANSITable

    df = pd.DataFrame({"calories": [420, 380, 390], "duration": [50, 40, 45]})
    table = ANSITable.Pandas(df, border="thin")
    table.print()

Convert ``ANSITable`` back to ``DataFrame``:

.. runblock:: plain_python
    :no-prompt:

    from ansitable import ANSITable
    import pandas as pd

    table = ANSITable("Name", "Age", "Admission score", border="ascii")
    table.row("Alice", 25, 95.1)
    table.row("Bob", 30, 87.3)
    table.row("Carol", 28, 92.1)
    table.row("Michelangelo", 35, 88.0)

    df = table.pandas()
    print(df)

Column names are converted to valid Python identifiers (spaces → underscores),
allowing attribute access like ``df.Admission_score``.
Disable this with ``underscores=False``.
