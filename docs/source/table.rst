Table classes
=============

This class creates a table that can be pretty printed in any terminal that supports ANSI escape sequences.

Creating a table
----------------

.. autoclass:: ansitable.ANSITable
   :members: Pandas, addcolumn
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

.. autoclass:: ansitable.Column
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

.. autoclass:: ansitable.Cell
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

Adding a row
------------

.. autoclass:: ansitable.ANSITable
   :members: row, rule
   :undoc-members:
   :show-inheritance:
   :no-index:

Display a table
---------------

.. autoclass:: ansitable.ANSITable
   :members: print, str
   :undoc-members:
   :show-inheritance:
   :no-index:

Render in markup formats
------------------------

These methods are used to export an ANSI table to different markup languages.

.. autoclass:: ansitable.table.ANSITable
   :members: latex, markdown, html, wikitable, csv, pandas, rest
   :undoc-members:
   :show-inheritance: