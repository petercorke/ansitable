import unittest
import numpy as np
from ansitable import ANSITable, Column, ANSIMatrix

unittest.TestCase.maxDiff = None


class TestANSItable(unittest.TestCase):

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
if __name__ == "__main__":

    unittest.main()
