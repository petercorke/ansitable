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


class TestHTMLGeneration(unittest.TestCase):
    """Test HTML table generation with border attributes"""

    def test_html_no_border(self):
        """Test HTML generation without border"""
        table = ANSITable("col1", "col2")
        table.row("a", "b")
        html = table.html()
        self.assertIn("<table>", html)
        self.assertNotIn('border=', html)
        self.assertNotIn('bordercolor=', html)

    def test_html_thick_border(self):
        """Test HTML generation with thick border"""
        table = ANSITable("col1", "col2", border="thick")
        table.row("a", "b")
        html = table.html()
        self.assertIn('border="3"', html)

    def test_html_thin_border(self):
        """Test HTML generation with thin border"""
        table = ANSITable("col1", "col2", border="thin")
        table.row("a", "b")
        html = table.html()
        self.assertIn('border="1"', html)

    def test_html_double_border(self):
        """Test HTML generation with double border"""
        table = ANSITable("col1", "col2", border="double")
        table.row("a", "b")
        html = table.html()
        self.assertIn('border="2"', html)

    def test_html_round_border(self):
        """Test HTML generation with round border"""
        table = ANSITable("col1", "col2", border="round")
        table.row("a", "b")
        html = table.html()
        self.assertIn('border="1"', html)

    def test_html_ascii_border(self):
        """Test HTML generation with ascii border"""
        table = ANSITable("col1", "col2", border="ascii")
        table.row("a", "b")
        html = table.html()
        self.assertIn('border="1"', html)

    def test_html_bordercolor(self):
        """Test HTML generation with bordercolor"""
        table = ANSITable("col1", "col2", border="thick", bordercolor="blue")
        table.row("a", "b")
        html = table.html()
        self.assertIn('border="3"', html)
        self.assertIn('bordercolor="blue"', html)

    def test_html_bordercolor_without_border(self):
        """Test that bordercolor is included even without explicit border"""
        table = ANSITable("col1", "col2", bordercolor="red")
        table.row("a", "b")
        html = table.html()
        self.assertIn('bordercolor="red"', html)
        self.assertNotIn('border=', html)

    def test_html_with_style_parameter(self):
        """Test HTML generation with additional style parameter"""
        table = ANSITable("col1", "col2", border="thick", bordercolor="blue")
        table.row("a", "b")
        html = table.html(table='margin: 10px; padding: 5px;')
        self.assertIn('border="3"', html)
        self.assertIn('bordercolor="blue"', html)
        self.assertIn('style="margin: 10px; padding: 5px;"', html)

    def test_html_contains_table_tag(self):
        """Test that HTML contains proper table tag"""
        table = ANSITable("col1", "col2")
        table.row("a", "b")
        html = table.html()
        self.assertIn("<table", html)
        self.assertIn("</table>", html)

    def test_html_contains_tr_td_tags(self):
        """Test that HTML contains proper row and cell tags"""
        table = ANSITable("col1", "col2")
        table.row("a", "b")
        html = table.html()
        self.assertIn("<tr", html)
        self.assertIn("</tr>", html)
        self.assertIn("<th", html)
        self.assertIn("</th>", html)
        self.assertIn("<td", html)
        self.assertIn("</td>", html)

    def test_html_alignment_styles(self):
        """Test that HTML includes alignment styles"""
        table = ANSITable(
            Column("left", headalign="<"),
            Column("center", headalign="^"),
            Column("right", headalign=">")
        )
        table.row("a", "b", "c")
        html = table.html()
        # Should have text-align styles for each alignment
        self.assertIn('text-align:left;', html)
        self.assertIn('text-align:center;', html)
        self.assertIn('text-align:right;', html)

    def test_html_cell_styling(self):
        """Test that HTML cell styling parameters are included"""
        table = ANSITable("col1", "col2")
        table.row("a", "b")
        html = table.html(
            td='border: 1px solid; padding: 5px;',
            th='background: #f0f0f0;'
        )
        self.assertIn('border: 1px solid; padding: 5px;', html)
        self.assertIn('background: #f0f0f0;', html)

    def test_html_escape_ellipsis(self):
        """Test that ellipsis character is escaped in HTML"""
        table = ANSITable(Column("col", width=3))
        table.row("this is long")
        html = table.html()
        # Ellipsis should be replaced with &hellip; entity
        self.assertIn("&hellip;", html)
        self.assertNotIn("…", html)


class TestMarkdownExport(unittest.TestCase):
    """Test Markdown table export format"""

    def test_markdown_header_row(self):
        """Test that markdown output includes header row"""
        table = ANSITable("col1", "col2", "col3")
        table.row("a", "b", "c")
        md = table.markdown()
        lines = md.strip().split('\n')
        # First line should be header with pipes
        self.assertIn('col1', lines[0])
        self.assertIn('|', lines[0])

    def test_markdown_alignment_row(self):
        """Test that markdown alignment row is generated correctly"""
        table = ANSITable(
            Column("left", headalign="<"),
            Column("center", headalign="^"),
            Column("right", headalign=">")
        )
        table.row("a", "b", "c")
        md = table.markdown()
        lines = md.strip().split('\n')
        # Second line should be alignment with colons and dashes
        self.assertIn(':', lines[1])  # Alignment markers
        self.assertIn('-', lines[1])  # Dashes

    def test_markdown_data_rows(self):
        """Test that markdown includes data rows"""
        table = ANSITable("col1", "col2")
        table.row("a", "b")
        table.row("c", "d")
        md = table.markdown()
        # Should have header + alignment + 2 data rows = 4 lines
        lines = [line for line in md.strip().split('\n') if line.strip()]
        self.assertEqual(len(lines), 4)

    def test_markdown_proper_pipe_delimiters(self):
        """Test that all rows use pipe delimiters"""
        table = ANSITable("col1", "col2")
        table.row("a", "b")
        md = table.markdown()
        # All non-empty lines should start and end with |
        for line in md.strip().split('\n'):
            if line.strip():
                self.assertTrue(line.strip().startswith('|'))
                self.assertTrue(line.strip().endswith('|'))

    def test_markdown_escape_characters(self):
        """Test that markdown handles special characters"""
        table = ANSITable("col|1", "col2")
        table.row("a|b", "c")
        md = table.markdown()
        # Should still be valid markdown
        self.assertIn('|', md)
        self.assertIn('col|1', md)  # Column header contains the pipe

    def test_markdown_numeric_formatting(self):
        """Test markdown with numeric data"""
        table = ANSITable("value")
        table.row(3.14159)
        md = table.markdown()
        self.assertIn("3.14159", md)


class TestReSTPExport(unittest.TestCase):
    """Test ReST (reStructuredText) table export format"""

    def test_rest_header_row(self):
        """Test that ReST output includes header row"""
        table = ANSITable("col1", "col2")
        table.row("a", "b")
        rest = table.rest()
        lines = rest.strip().split('\n')
        # Should have divider, header, divider, data, divider
        self.assertGreaterEqual(len(lines), 5)

    def test_rest_has_dividers(self):
        """Test that ReST includes top/middle/bottom dividers"""
        table = ANSITable("col1", "col2")
        table.row("a", "b")
        rest = table.rest()
        # Should have lines with equals signs
        self.assertIn('=', rest)
        divider_count = rest.count('=')
        self.assertGreater(divider_count, 3)  # Multiple divider rows

    def test_rest_column_alignment(self):
        """Test ReST output structure"""
        table = ANSITable(
            Column("left", headalign="<"),
            Column("right", headalign=">")
        )
        table.row("a", "b")
        rest = table.rest()
        # Should have proper structure
        lines = rest.strip().split('\n')
        self.assertGreater(len(lines), 0)
        # First line should be divider
        self.assertIn('=', lines[0])

    def test_rest_multiple_rows(self):
        """Test ReST with multiple data rows"""
        table = ANSITable("col1", "col2")
        table.row("a", "b")
        table.row("c", "d")
        table.row("e", "f")
        rest = table.rest()
        # Should have all data
        self.assertIn('a', rest)
        self.assertIn('c', rest)
        self.assertIn('e', rest)

    def test_rest_no_column_alignment_info(self):
        """Test that ReST does not include column alignment classes"""
        table = ANSITable(
            Column("left", headalign="<"),
            Column("right", headalign=">")
        )
        table.row("a", "b")
        rest = table.rest()
        # ReST simple tables don't support alignment in the output
        # (per the docstring)
        self.assertNotIn('class=', rest)


class TestWikitableExport(unittest.TestCase):
    """Test wikitable (Wikipedia) table export format"""

    def test_wikitable_opening_tag(self):
        """Test that wikitable output starts with proper opening"""
        table = ANSITable("col1", "col2")
        table.row("a", "b")
        wiki = table.wikitable()
        self.assertIn('{| class="wikitable"', wiki)

    def test_wikitable_closing_tag(self):
        """Test that wikitable output has proper closing"""
        table = ANSITable("col1", "col2")
        table.row("a", "b")
        wiki = table.wikitable()
        self.assertIn('|}', wiki)

    def test_wikitable_alignment_classes(self):
        """Test that wikitable includes alignment classes"""
        table = ANSITable(
            Column("left", headalign="<"),
            Column("center", headalign="^"),
            Column("right", headalign=">")
        )
        table.row("a", "b", "c")
        wiki = table.wikitable()
        # Should have alignment classes
        self.assertIn('col1left', wiki)
        self.assertIn('col2center', wiki)
        self.assertIn('col3right', wiki)

    def test_wikitable_header_delimiter(self):
        """Test that wikitable uses ! for header cells"""
        table = ANSITable("col1", "col2")
        table.row("a", "b")
        wiki = table.wikitable()
        self.assertIn('!', wiki)  # Header cell marker

    def test_wikitable_data_delimiter(self):
        """Test that wikitable uses | for data cells"""
        table = ANSITable("col1", "col2")
        table.row("a", "b")
        wiki = table.wikitable()
        self.assertIn('||', wiki)  # Data cell separator

    def test_wikitable_row_separator(self):
        """Test that wikitable has row separators"""
        table = ANSITable("col1", "col2")
        table.row("a", "b")
        table.row("c", "d")
        wiki = table.wikitable()
        # Should have multiple |- row separators
        row_sep_count = wiki.count('|-')
        self.assertGreater(row_sep_count, 1)

    def test_wikitable_header_operator(self):
        """Test that wikitable header cells use !! separator"""
        table = ANSITable("col1", "col2", "col3")
        table.row("a", "b", "c")
        wiki = table.wikitable()
        # Multiple header columns should use !! separator
        self.assertIn('!!', wiki)


class TestLaTeXExport(unittest.TestCase):
    """Test LaTeX table export format"""

    def test_latex_begin_tabular(self):
        """Test that LaTeX output has proper opening"""
        table = ANSITable("col1", "col2")
        table.row("a", "b")
        latex = table.latex()
        self.assertIn(r'\begin{tabular}', latex)

    def test_latex_end_tabular(self):
        """Test that LaTeX output has proper closing"""
        table = ANSITable("col1", "col2")
        table.row("a", "b")
        latex = table.latex()
        self.assertIn(r'\end{tabular}', latex)

    def test_latex_alignment_specification(self):
        """Test that LaTeX includes column alignment spec"""
        table = ANSITable(
            Column("left", headalign="<"),
            Column("right", headalign=">")
        )
        table.row("a", "b")
        latex = table.latex()
        # Should have alignment spec like {|l|r|}
        self.assertIn('{', latex)
        self.assertIn('|', latex)

    def test_latex_hline_markers(self):
        """Test that LaTeX includes hline markers"""
        table = ANSITable("col1", "col2")
        table.row("a", "b")
        latex = table.latex()
        self.assertIn(r'\hline', latex)

    def test_latex_row_separator(self):
        """Test that LaTeX uses \\ for row separator"""
        table = ANSITable("col1", "col2")
        table.row("a", "b")
        table.row("c", "d")
        latex = table.latex()
        # Multiple rows should have \\ separator
        self.assertIn(r'\\', latex)

    def test_latex_ampersand_column_separator(self):
        """Test that LaTeX uses & for column separator"""
        table = ANSITable("col1", "col2", "col3")
        table.row("a", "b", "c")
        latex = table.latex()
        # Should have & between columns
        self.assertIn('&', latex)

    def test_latex_multicolumn_header(self):
        """Test that LaTeX uses multicolumn for headers"""
        table = ANSITable("col1", "col2")
        table.row("a", "b")
        latex = table.latex()
        # Headers often use multicolumn
        self.assertIn(r'\multicolumn', latex)

    def test_latex_escape_special_chars(self):
        """Test that LaTeX escapes special characters if needed"""
        table = ANSITable("col_1", "col 2")
        table.row("a&b", "c")
        latex = table.latex()
        # Should have ampersand escaped or handled
        self.assertIn('col_1', latex)


class TestCSVExport(unittest.TestCase):
    """Test CSV table export format"""

    def test_csv_header_row(self):
        """Test that CSV includes header row"""
        table = ANSITable("col1", "col2", "col3")
        table.row("a", "b", "c")
        csv = table.csv()
        lines = csv.strip().split('\n')
        self.assertGreater(len(lines), 1)
        # First line should be headers
        self.assertIn('col1', lines[0])
        self.assertIn('col2', lines[0])

    def test_csv_data_rows(self):
        """Test that CSV includes data rows"""
        table = ANSITable("col1", "col2")
        table.row("a", "b")
        table.row("c", "d")
        csv = table.csv()
        # Should have at least header + 2 data rows
        lines = csv.strip().split('\n')
        self.assertEqual(len(lines), 3)

    def test_csv_default_comma_delimiter(self):
        """Test that CSV uses comma delimiter by default"""
        table = ANSITable("col1", "col2")
        table.row("a", "b")
        csv = table.csv()
        self.assertIn(',', csv)

    def test_csv_custom_delimiter(self):
        """Test that CSV respects custom delimiter"""
        table = ANSITable("col1", "col2")
        table.row("a", "b")
        csv = table.csv(delimiter=';')
        self.assertIn(';', csv)
        # Default delimiter should still be present in separator, but data separated by ;
        lines = csv.strip().split('\n')
        self.assertGreater(len(lines[0].split(';')), 1)

    def test_csv_quoting_if_comma_in_data(self):
        """Test that CSV handles data containing the delimiter"""
        table = ANSITable("col1", "col2")
        table.row("a,b", "c")
        csv = table.csv()
        # Should still be parseable (either quoted or escaped)
        self.assertIn('a', csv)
        self.assertIn('b', csv)
        self.assertIn('c', csv)

    def test_csv_numeric_data(self):
        """Test CSV with numeric values"""
        table = ANSITable("value")
        table.row(3.14159)
        table.row(-5.5)
        csv = table.csv()
        self.assertIn('3.14159', csv)
        self.assertIn('-5.5', csv)

    def test_csv_all_columns_present(self):
        """Test that all columns appear in each CSV row"""
        table = ANSITable("A", "B", "C")
        table.row(1, 2, 3)
        csv = table.csv()
        lines = csv.strip().split('\n')
        # Each line (header and data) should have 2 commas (3 fields)
        for line in lines:
            self.assertEqual(line.count(','), 2)

    def test_csv_escape_quotes(self):
        """Test CSV handling of quoted strings"""
        table = ANSITable("col1")
        table.row('value"with"quotes')
        csv = table.csv()
        # Should contain the value (possibly escaped or quoted)
        self.assertIn('value', csv)


# ----------------------------------------------------------------------- #
if __name__ == "__main__":

    unittest.main()
