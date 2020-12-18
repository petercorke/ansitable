
import unittest
import numpy as np
from ansitable import ANSITable, Column, ANSIMatrix

unittest.TestCase.maxDiff = None

class TestANSItable(unittest.TestCase):

    def test_table_1(self):

        ans = r"""         col1  column 2 has a big header  column 3  
    aaaaaaaaa                        2.2         3  
bbbbbbbbbbbbb                       -5.5         6  
      ccccccc                        8.8        -9  
"""

        table = ANSITable("col1", "column 2 has a big header", "column 3", color=False)
        table.row("aaaaaaaaa", 2.2, 3)
        table.row("bbbbbbbbbbbbb", -5.5, 6)
        table.row("ccccccc", 8.8, -9)

        self.assertEqual(str(table), ans)

    def test_table_2(self):
        ans = r"""         col1  column 2 has a big header  column 3  
    aaaaaaaaa                        2.2         3  
bbbbbbbbbbbbb                        5.5         6  
      ccccccc                        8.8        -9  
"""

        table = ANSITable(
            Column("col1"),
            Column("column 2 has a big header"),
            Column("column 3"),
            color=False
        )
        table.row("aaaaaaaaa", 2.2, 3)
        table.row("bbbbbbbbbbbbb", 5.5, 6)
        table.row("ccccccc", 8.8, -9)

        self.assertEqual(str(table), ans)

    def test_table_3(self):
        ans = r"""         col1  column 2 has a big header  column 3  
    aaaaaaaaa                        2.2         3  
bbbbbbbbbbbbb                       -5.5         6  
      ccccccc                        8.8        -9  
"""

        table = ANSITable(
            Column("col1"),
            Column("column 2 has a big header"),
            Column("column 3"),
            color=False
        )
        table.row("aaaaaaaaa", 2.2, 3)
        table.row("bbbbbbbbbbbbb", -5.5, 6)
        table.row("ccccccc", 8.8, -9)

        self.assertEqual(str(table), ans)

    def test_table_4(self):
        ans = r"""         col1  column 2 has a big header    column 3  
    aaaaaaaaa                        2.2      3.0000  
bbbbbbbbbbbbb                       -5.5      6.0000  
      ccccccc                        8.8     -9.0000  
"""

        table = ANSITable(
            Column("col1"),
            Column("column 2 has a big header", "{:.3g}"),
            Column("column 3", "{:-10.4f}"),
            color=False
        )
        table.row("aaaaaaaaa", 2.2, 3)
        table.row("bbbbbbbbbbbbb", -5.5, 6)
        table.row("ccccccc", 8.8, -9)

        self.assertEqual(str(table), ans)

    def test_table_5(self):
        ans = r"""      col1  column 2 has a big header    column 3  
 aaaaaaaaa                        2.2      3.0000  
bbbbbbbbb…                       -5.5      6.0000  
   ccccccc                        8.8     -9.0000  
"""

        table = ANSITable(
            Column("col1", width=10),
            Column("column 2 has a big header", "{:.3g}"),
            Column("column 3", "{:-10.4f}"),
            color=False
        )
        table.row("aaaaaaaaa", 2.2, 3)
        table.row("bbbbbbbbbbbbb", -5.5, 6)
        table.row("ccccccc", 8.8, -9)

        self.assertEqual(str(table), ans)

    def test_table_ascii(self):
        ans = r"""+--------------+---------------------------+----------+
|         col1 | column 2 has a big header | column 3 |
+--------------+---------------------------+----------+
|    aaaaaaaaa |                       2.2 |        3 |
|bbbbbbbbbbbbb |                      -5.5 |        6 |
|      ccccccc |                       8.8 |       -9 |
+--------------+---------------------------+----------+
"""

        table = ANSITable(
            Column("col1"),
            Column("column 2 has a big header"),
            Column("column 3"),
            border="ascii",
            color=False
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

        ans = r"""┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃         col1 ┃ column 2 has a big header ┃ column 3 ┃
┣━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━┫
┃    aaaaaaaaa ┃                       2.2 ┃        3 ┃
┃bbbbbbbbbbbbb ┃                      -5.5 ┃        6 ┃
┃      ccccccc ┃                       8.8 ┃       -9 ┃
┗━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━┛
"""
        table = ANSITable(
            Column("col1"),
            Column("column 2 has a big header"),
            Column("column 3"),
            border="thick",
            color=False
        )
        table.row("aaaaaaaaa", 2.2, 3)
        table.row("bbbbbbbbbbbbb", -5.5, 6)
        table.row("ccccccc", 8.8, -9)

        self.assertEqual(str(table), ans)


    def test_table_border_2(self):

        ans = r"""┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃         col1 ┃ column 2 has a big header ┃ column 3 ┃
┣━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━┫
┃    aaaaaaaaa ┃            2.2            ┃        3 ┃
┃bbbbbbbbbbbbb ┃           -5.5            ┃        6 ┃
┃      ccccccc ┃            8.8            ┃       -9 ┃
┗━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━┛
"""
        table = ANSITable(
            Column("col1"),
            Column("column 2 has a big header", colalign="^"),
            Column("column 3"),
            border="thick",
            color=False
        )
        table.row("aaaaaaaaa", 2.2, 3)
        table.row("bbbbbbbbbbbbb", -5.5, 6)
        table.row("ccccccc", 8.8, -9)

        self.assertEqual(str(table), ans)

    def test_table_border_3(self):

        ans = r"""┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃col1          ┃ column 2 has a big header ┃ column 3 ┃
┣━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━┫
┃    aaaaaaaaa ┃            2.2            ┃ 3        ┃
┃bbbbbbbbbbbbb ┃           -5.5            ┃ 6        ┃
┃      ccccccc ┃            8.8            ┃ -9       ┃
┗━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━┛
"""
        table = ANSITable(
            Column("col1", headalign="<"),
            Column("column 2 has a big header", colalign="^"),
            Column("column 3", colalign="<"),
            border="thick",
            color=False
        )
        table.row("aaaaaaaaa", 2.2, 3)
        table.row("bbbbbbbbbbbbb", -5.5, 6)
        table.row("ccccccc", 8.8, -9)

        self.assertEqual(str(table), ans)

    # ----------------------------------------------------------------------- #

    def test_matrix_1(self):

        m = np.arange(16).reshape((4,4)) /10 - 0.8
        m[0,0] = 1.23456e-14

        ans = r"""┏                                           ┓
┃ 0         -0.7       -0.6       -0.5      ┃
┃-0.4       -0.3       -0.2       -0.1      ┃
┃ 0          0.1        0.2        0.3      ┃
┃ 0.4        0.5        0.6        0.7      ┃
┗                                           ┛"""
        formatter = ANSIMatrix(style='thick', squish=True)

        self.assertEqual(formatter.str(m), ans)

    def test_matrix_2(self):

        m = np.arange(16).reshape((4,4)) /10 - 0.8
        m[0,0] = 1.23456e-14

        ans = r"""┏                                           ┓T
┃ 0         -0.7       -0.6       -0.5      ┃
┃-0.4       -0.3       -0.2       -0.1      ┃
┃ 0          0.1        0.2        0.3      ┃
┃ 0.4        0.5        0.6        0.7      ┃
┗                                           ┛3"""
        formatter = ANSIMatrix(style='thick', squish=True)

        self.assertEqual(formatter.str(m, suffix_super='T', suffix_sub='3'), ans)

    def test_matrix_3(self):

        m = np.arange(16).reshape((4,4)) /10 - 0.8
        m[0,0] = 1.23456e-14

        ans = r"""┏                                           ┓T
┃-0.5       -0.25       0          0.25     ┃
┗                                           ┛"""
        formatter = ANSIMatrix(style='thick', squish=True)

        m = np.arange(4) / 4 - 0.5
        self.assertEqual(formatter.str(m, 'T'), ans)



# ----------------------------------------------------------------------- #
if __name__ == '__main__':

    unittest.main()