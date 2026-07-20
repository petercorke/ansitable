import importlib
import unittest
import numpy as np
from ansitable import ANSITable, Column, ANSIMatrix, options

pandas_available = importlib.util.find_spec("pandas") is not None
skip_no_pandas = unittest.skipUnless(pandas_available, "pandas not installed")

unittest.TestCase.maxDiff = None


class TestANSItable(unittest.TestCase):

    def test_column_headalign_none_falls_back_to_colalign(self):
        c = Column("col", colalign="<", headalign=None)
        self.assertEqual(c.headalign, "<")

    def test_addcolumn_sets_column_table(self):
        table = ANSITable(color=False)
        table.addcolumn("col1")
        self.assertIs(table.columns[0].table, table)

    def test_options_updates_existing_and_future_tables(self):
        try:
            # start from a known global state
            options(True, color=False)

            existing = ANSITable(Column("c1"), border="thin", color=False)
            existing.row("x")
            self.assertIn("┌", str(existing))

            # Existing tables should follow updated globals.
            options(False)
            self.assertIn("+", str(existing))

            # Future tables should also follow updated globals.
            future = ANSITable(Column("c1"), border="thin", color=False)
            future.row("x")
            self.assertIn("+", str(future))
        finally:
            # reset global defaults for any subsequent tests
            options(True, color=False)

    def test_table_1(self):

        ans = r"""          col1   column 2 has a big header   column 3  
     aaaaaaaaa                         2.2          3  
 bbbbbbbbbbbbb                        -5.5          6  
       ccccccc                         8.8         -9  
"""

        table = ANSITable("col1", "column 2 has a big header", "column 3", color=False)
        table.row("aaaaaaaaa", 2.2, 3)
        table.row("bbbbbbbbbbbbb", -5.5, 6)
        table.row("ccccccc", 8.8, -9)

        self.assertEqual(str(table), ans)

    def test_table_2(self):
        ans = r"""          col1   column 2 has a big header   column 3  
     aaaaaaaaa                         2.2          3  
 bbbbbbbbbbbbb                         5.5          6  
       ccccccc                         8.8         -9  
"""

        table = ANSITable(
            Column("col1"),
            Column("column 2 has a big header"),
            Column("column 3"),
            color=False,
        )
        table.row("aaaaaaaaa", 2.2, 3)
        table.row("bbbbbbbbbbbbb", 5.5, 6)
        table.row("ccccccc", 8.8, -9)

        self.assertEqual(str(table), ans)

    def test_table_3(self):
        ans = r"""          col1   column 2 has a big header   column 3  
     aaaaaaaaa                         2.2          3  
 bbbbbbbbbbbbb                        -5.5          6  
       ccccccc                         8.8         -9  
"""

        table = ANSITable(
            Column("col1"),
            Column("column 2 has a big header"),
            Column("column 3"),
            color=False,
        )
        table.row("aaaaaaaaa", 2.2, 3)
        table.row("bbbbbbbbbbbbb", -5.5, 6)
        table.row("ccccccc", 8.8, -9)

        self.assertEqual(str(table), ans)

    def test_table_4(self):
        ans = r"""          col1   column 2 has a big header     column 3  
     aaaaaaaaa                         2.2       3.0000  
 bbbbbbbbbbbbb                        -5.5       6.0000  
       ccccccc                         8.8      -9.0000  
"""

        table = ANSITable(
            Column("col1"),
            Column("column 2 has a big header", "{:.3g}"),
            Column("column 3", "{:-10.4f}"),
            color=False,
        )
        table.row("aaaaaaaaa", 2.2, 3)
        table.row("bbbbbbbbbbbbb", -5.5, 6)
        table.row("ccccccc", 8.8, -9)

        self.assertEqual(str(table), ans)

    def test_table_5(self):
        ans = r"""       col1   column 2 has a big header     column 3  
  aaaaaaaaa                         2.2       3.0000  
 bbbbbbbbb…                        -5.5       6.0000  
    ccccccc                         8.8      -9.0000  
"""

        table = ANSITable(
            Column("col1", width=10),
            Column("column 2 has a big header", "{:.3g}"),
            Column("column 3", "{:-10.4f}"),
            color=False,
        )
        table.row("aaaaaaaaa", 2.2, 3)
        table.row("bbbbbbbbbbbbb", -5.5, 6)
        table.row("ccccccc", 8.8, -9)

        self.assertEqual(str(table), ans)

    def test_table_ascii(self):
        ans = r"""+---------------+---------------------------+----------+
|          col1 | column 2 has a big header | column 3 |
+---------------+---------------------------+----------+
|     aaaaaaaaa |                       2.2 |        3 |
| bbbbbbbbbbbbb |                      -5.5 |        6 |
|       ccccccc |                       8.8 |       -9 |
+---------------+---------------------------+----------+
"""

        table = ANSITable(
            Column("col1"),
            Column("column 2 has a big header"),
            Column("column 3"),
            border="ascii",
            color=False,
        )
        table.row("aaaaaaaaa", 2.2, 3)
        table.row("bbbbbbbbbbbbb", -5.5, 6)
        table.row("ccccccc", 8.8, -9)

        self.assertEqual(str(table), ans)

    # table = ANSITable("col1", "column 2 has a big header", "column 3", color=False)
    # table.row("aaaaaaaaa", 2.2, 3)
    # table.row("<<red>>bbbbbbbbbbbbb", 5.5, 6)
    # table.row("<<blue>>ccccccc", 8.8, -9)
    # table.print()

    def test_table_border_1(self):

        ans = r"""┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃          col1 ┃ column 2 has a big header ┃ column 3 ┃
┣━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━┫
┃     aaaaaaaaa ┃                       2.2 ┃        3 ┃
┃ bbbbbbbbbbbbb ┃                      -5.5 ┃        6 ┃
┃       ccccccc ┃                       8.8 ┃       -9 ┃
┗━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━┛
"""
        table = ANSITable(
            Column("col1"),
            Column("column 2 has a big header"),
            Column("column 3"),
            border="thick",
            color=False,
        )
        table.row("aaaaaaaaa", 2.2, 3)
        table.row("bbbbbbbbbbbbb", -5.5, 6)
        table.row("ccccccc", 8.8, -9)

        self.assertEqual(str(table), ans)

    def test_table_border_2(self):

        ans = r"""┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃          col1 ┃ column 2 has a big header ┃ column 3 ┃
┣━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━┫
┃     aaaaaaaaa ┃            2.2            ┃        3 ┃
┃ bbbbbbbbbbbbb ┃           -5.5            ┃        6 ┃
┃       ccccccc ┃            8.8            ┃       -9 ┃
┗━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━┛
"""
        table = ANSITable(
            Column("col1"),
            Column("column 2 has a big header", colalign="^"),
            Column("column 3"),
            border="thick",
            color=False,
        )
        table.row("aaaaaaaaa", 2.2, 3)
        table.row("bbbbbbbbbbbbb", -5.5, 6)
        table.row("ccccccc", 8.8, -9)

        self.assertEqual(str(table), ans)

    def test_table_border_3(self):

        ans = r"""┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ col1          ┃ column 2 has a big header ┃ column 3 ┃
┣━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━┫
┃     aaaaaaaaa ┃            2.2            ┃ 3        ┃
┃ bbbbbbbbbbbbb ┃           -5.5            ┃ 6        ┃
┃       ccccccc ┃            8.8            ┃ -9       ┃
┗━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━┛
"""
        table = ANSITable(
            Column("col1", headalign="<"),
            Column("column 2 has a big header", colalign="^"),
            Column("column 3", colalign="<"),
            border="thick",
            color=False,
        )
        table.row("aaaaaaaaa", 2.2, 3)
        table.row("bbbbbbbbbbbbb", -5.5, 6)
        table.row("ccccccc", 8.8, -9)

        self.assertEqual(str(table), ans)

    # ----------------------------------------------------------------------- #

    def test_matrix_1(self):

        m = np.arange(16).reshape((4, 4)) / 10 - 0.8
        m[0, 0] = 1.23456e-14

        ans = r"""┏                                           ┓
┃ 0         -0.7       -0.6       -0.5      ┃
┃-0.4       -0.3       -0.2       -0.1      ┃
┃ 0          0.1        0.2        0.3      ┃
┃ 0.4        0.5        0.6        0.7      ┃
┗                                           ┛"""
        formatter = ANSIMatrix(style="thick")
        self.assertEqual(formatter.str(m), ans)

        m[0, 0] = -1.23456e-14
        formatter = ANSIMatrix(style="thick")
        self.assertEqual(formatter.str(m), ans)

        m[0, 0] = 1.23456e-14

        ans = r"""┏                                           ┓
┃ 1.23e-14  -0.7       -0.6       -0.5      ┃
┃-0.4       -0.3       -0.2       -0.1      ┃
┃ 0          0.1        0.2        0.3      ┃
┃ 0.4        0.5        0.6        0.7      ┃
┗                                           ┛"""
        formatter = ANSIMatrix(style="thick", squish=10)
        self.assertEqual(formatter.str(m), ans)

    def test_matrix_2(self):

        m = np.arange(16).reshape((4, 4)) / 10 - 0.8
        m[0, 0] = 1.23456e-14

        ans = r"""┏                                           ┓T
┃ 0         -0.7       -0.6       -0.5      ┃
┃-0.4       -0.3       -0.2       -0.1      ┃
┃ 0          0.1        0.2        0.3      ┃
┃ 0.4        0.5        0.6        0.7      ┃
┗                                           ┛3"""
        formatter = ANSIMatrix(style="thick")

        self.assertEqual(formatter.str(m, suffix_super="T", suffix_sub="3"), ans)

    def test_matrix_3(self):

        m = np.arange(16).reshape((4, 4)) / 10 - 0.8
        m[0, 0] = 1.23456e-14

        ans = r"""┏                                           ┓T
┃-0.5       -0.25       0          0.25     ┃
┗                                           ┛"""
        formatter = ANSIMatrix(style="thick", squish=True)

        m = np.arange(4) / 4 - 0.5
        self.assertEqual(formatter.str(m, "T"), ans)

    def test_table_convert(self):

        table = ANSITable("col1", "column 2 has a big header", "column 3")
        table.row("aaaaaaaaa", 2.2, 3)
        table.row("bbbbbbbbbbbbb", -5.5, 6)
        table.row("ccccccc", 8.8, -9)

        ans = r"""\begin{tabular}{ |r|r|r| }\hline
\multicolumn{1}{|r|}{col1} & \multicolumn{1}{|r|}{column 2 has a big header} & \multicolumn{1}{|r|}{column 3}\\\hline\hline
aaaaaaaaa & 2.2 & 3 \\
bbbbbbbbbbbbb & -5.5 & 6 \\
ccccccc & 8.8 & -9 \\
\hline
\end{tabular}
"""
        self.assertEqual(table.latex(), ans)

        ans = r"""|           col1  |  column 2 has a big header  |  column 3  |
| ------------: | ------------------------: | -------: |
|      aaaaaaaaa  |                        2.2  |         3  |
|  bbbbbbbbbbbbb  |                       -5.5  |         6  |
|        ccccccc  |                        8.8  |        -9  |
"""
        self.assertEqual(table.markdown(), ans)

        ans = r"""col1,column 2 has a big header,column 3
aaaaaaaaa,2.2,3
bbbbbbbbbbbbb,-5.5,6
ccccccc,8.8,-9
"""
        self.assertEqual(table.csv(), ans)

        # df = table.pandas()
        # print(df)

    @skip_no_pandas
    def test_table_pandas(self):

        import pandas as pd

        table = ANSITable("col1", "column 2 has a big header", "column 3")
        table.row("aaaaaaaaa", 2.2, 3)
        table.row("bbbbbbbbbbbbb", -5.5, 6)
        table.row("ccccccc", 8.8, -9)
        table.row("dd", 9.9, -11)

        df = table.pandas()
        self.assertEqual(len(df), 4)
        self.assertEqual(len(df.columns), 3)
        self.assertEqual(df.columns[0], "col1")
        self.assertEqual(df.columns[1], "column_2_has_a_big_header")
        self.assertEqual(df.columns[2], "column_3")
        self.assertEqual(df.iloc[0, 0], "aaaaaaaaa")
        self.assertEqual(df.iloc[0, 1], "2.2")
        self.assertEqual(df.iloc[0, 2], "3")
        self.assertEqual(df.iloc[1, 0], "bbbbbbbbbbbbb")
        self.assertEqual(df.iloc[1, 1], "-5.5")
        self.assertEqual(df.iloc[1, 2], "6")

        df = table.pandas(underscores=False)
        self.assertEqual(len(df), 4)
        self.assertEqual(len(df.columns), 3)
        self.assertEqual(df.columns[0], "col1")
        self.assertEqual(df.columns[1], "column 2 has a big header")
        self.assertEqual(df.columns[2], "column 3")
        self.assertEqual(df.iloc[0, 0], "aaaaaaaaa")
        self.assertEqual(df.iloc[0, 1], "2.2")
        self.assertEqual(df.iloc[0, 2], "3")
        self.assertEqual(df.iloc[1, 0], "bbbbbbbbbbbbb")
        self.assertEqual(df.iloc[1, 1], "-5.5")
        self.assertEqual(df.iloc[1, 2], "6")

        df = pd.DataFrame({"calories": [420, 380, 390], "duration": [50, 40, 45]})
        table = ANSITable.Pandas(df, border="thin")
        self.assertEqual(len(table.columns), 2)
        self.assertEqual(len(table), 3)
        self.assertEqual(table.columns[0].name, "calories")
        self.assertEqual(table.columns[1].name, "duration")


# ----------------------------------------------------------------------- #

class TestANSITableSort(unittest.TestCase):

    def _make_table(self):
        """Three-row table with string and numeric columns."""
        table = ANSITable("name", "score", color=False)
        table.row("charlie", 3)
        table.row("alice", 1)
        table.row("bob", 2)
        return table

    def test_sort_by_column_name_lexicographic(self):
        table = self._make_table()
        table.sort("name")
        self.assertEqual(table.columns[0].formatted, ["alice", "bob", "charlie"])

    def test_sort_by_column_index(self):
        table = self._make_table()
        table.sort(0)
        self.assertEqual(table.columns[0].formatted, ["alice", "bob", "charlie"])

    def test_sort_with_key(self):
        table = self._make_table()
        table.sort("score", key=int)
        self.assertEqual(table.columns[1].formatted, ["1", "2", "3"])
        # companion column should follow
        self.assertEqual(table.columns[0].formatted, ["alice", "bob", "charlie"])

    def test_sort_reverse(self):
        table = self._make_table()
        table.sort("name", reverse=True)
        self.assertEqual(table.columns[0].formatted, ["charlie", "bob", "alice"])

    def test_sort_reverse_with_key(self):
        table = self._make_table()
        table.sort("score", key=int, reverse=True)
        self.assertEqual(table.columns[1].formatted, ["3", "2", "1"])

    def test_sort_drops_rule_rows_silently(self):
        table = ANSITable("name", "score", color=False)
        table.row("charlie", 3)
        table.rule()
        table.row("alice", 1)
        table.rule()
        table.row("bob", 2)
        table.sort("name")
        self.assertEqual(table.nrows, 3)
        self.assertEqual(table.columns[0].formatted, ["alice", "bob", "charlie"])

    def test_sort_preserves_row_attributes(self):
        table = ANSITable("name", "score", color=False)
        table.row("charlie", 3, fgcolor="red")
        table.row("alice", 1, fgcolor="blue")
        table.row("bob", 2, fgcolor="green")
        table.sort("name")
        self.assertEqual(table.columns[0].fgcolor, ["blue", "green", "red"])
        self.assertEqual(table.columns[1].fgcolor, ["blue", "green", "red"])

    def test_sort_returns_self_for_chaining(self):
        table = self._make_table()
        result = table.sort("name")
        self.assertIs(result, table)

    def test_sort_invalid_column_name_raises(self):
        table = self._make_table()
        with self.assertRaises(ValueError):
            table.sort("nonexistent")

    def test_sort_invalid_column_index_raises(self):
        table = self._make_table()
        with self.assertRaises(IndexError):
            table.sort(99)

    def test_sort_stable(self):
        # equal keys should preserve original relative order (Python sort is stable)
        table = ANSITable("group", "val", color=False)
        table.row("b", 10)
        table.row("a", 20)
        table.row("a", 30)
        table.sort("group")
        self.assertEqual(table.columns[0].formatted, ["a", "a", "b"])
        self.assertEqual(table.columns[1].formatted, ["20", "30", "10"])


# ----------------------------------------------------------------------- #
if __name__ == "__main__":

    unittest.main()
