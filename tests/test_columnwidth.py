import unittest

from ansitable import ANSITable


class TestColumnWidth(unittest.TestCase):

    def test_autofit_width_is_widest_of_header_and_cells(self):
        table = ANSITable("name", "x", color=False)
        table.row("a", "123456")
        table.row("longer cell", "1")
        table.print()  # forces width resolution
        self.assertEqual([c.width for c in table.columns], [11, 6])


if __name__ == "__main__":
    unittest.main()
