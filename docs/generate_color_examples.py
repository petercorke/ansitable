#!/usr/bin/env python3
"""Generate colored HTML table examples for documentation."""

from pathlib import Path
from ansitable import ANSITable, Column, Cell, options

# Enable colors and Unicode
options(True, color=True)

# Create output directory
output_dir = Path(__file__).parent / "_html_examples"
output_dir.mkdir(exist_ok=True)

# Example 1: Colored columns with styled header
table1 = ANSITable(
    Column("col1", headalign="<", colcolor="red", headstyle="underlined"),
    Column("column 2 has a big header", colalign="^", colstyle="bold"),
    Column("column 3", colalign="<", colbgcolor="green"),
    border="thick", bordercolor="blue"
)
table1.row("aaaaaaaaa", 2.2, 3)
table1.row("bbbbbbbbbbbbb", -5.5, 6)
table1.row("ccccccc", 8.8, -9)

html1 = table1.html(
    table="border-collapse: collapse; margin: 10px 0; border: 3px solid blue;",
    th="background: #f0f0f0; padding: 8px; border: 1px solid #ddd; font-weight: bold;",
    td="padding: 8px; border: 1px solid #ddd;",
)
(output_dir / "color_example_1.html").write_text(html1)
print("✓ Generated color_example_1.html")

# Example 2: Per-cell colors
table2 = ANSITable(
    Column("col1", headalign="<"),
    Column("column 2 has a big header", colalign="^"),
    Column("column 3", colalign="<"),
    border="thick"
)
table2.row("aaaaaaaaa", 2.2, 3)
table2.row("bbbbbbbbbbbbb", Cell(-5.5, bgcolor="blue"), 6, bgcolor="yellow")
table2.row("ccccccc", 8.8, 9)

html2 = table2.html(
    table="border-collapse: collapse; margin: 10px 0; border: 3px solid #333;",
    th="background: #f0f0f0; padding: 8px; border: 1px solid #ddd; font-weight: bold;",
    td="padding: 8px; border: 1px solid #ddd;",
)
(output_dir / "color_example_2.html").write_text(html2)
print("✓ Generated color_example_2.html")

print(f"\nHTML examples saved to: {output_dir}")
