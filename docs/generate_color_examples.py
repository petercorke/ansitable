#!/usr/bin/env python3
"""Generate colored HTML table examples for documentation."""

import json
from pathlib import Path
from colored.library import Library
from ansitable import ANSITable, Column, Cell, options, table

# Enable colors and Unicode
options(True, color=True)

# Create output directory
output_dir = Path(__file__).parent / "_html_examples"
output_dir.mkdir(exist_ok=True)

# Example 1: Styled header
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

html1 = table.html(
    table="border-collapse: collapse; margin: 10px 0; border: 3px solid blue;",
    th="padding: 8px; border: 1px solid #ddd; font-weight: bold;",
    td="padding: 8px; border: 1px solid #ddd;",
)
(output_dir / "color_example_1.html").write_text(html1)
print("✓ Generated color_example_1.html")

# Example 2: Colored columns with styled header
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

html2 = table.html(
    table="border-collapse: collapse; margin: 10px 0; border: 3px solid blue;",
    th="padding: 8px; border: 1px solid #ddd; font-weight: bold;",
    td="padding: 8px; border: 1px solid #ddd;",
)
(output_dir / "color_example_2.html").write_text(html2)
print("✓ Generated color_example_2.html")

# Example 3: Colored rows, with colored columns and styled header
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

html3 = table.html(
    table="border-collapse: collapse; margin: 10px 0; border: 3px solid blue;",
    th="padding: 8px; border: 1px solid #ddd; font-weight: bold;",
    td="padding: 8px; border: 1px solid #ddd;",
)
(output_dir / "color_example_3.html").write_text(html3)
print("✓ Generated color_example_3.html")

# Example 4: Per-cell colors
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

html4 = table.html(
    table="border-collapse: collapse; margin: 10px 0; border: 3px solid #333;",
    th="padding: 8px; border: 1px solid #ddd; font-weight: bold;",
    td="padding: 8px; border: 1px solid #ddd;",
)
(output_dir / "color_example_4.html").write_text(html4)
print("✓ Generated color_example_4.html")

print(f"\nHTML examples saved to: {output_dir}")

# Color reference: a searchable swatch chart of all 256 colors colored
# accepts, embedded on its own docs page (colors.rst) via
# ".. raw:: html :file:". Generated from the installed colored package's
# own palette table rather than hand-maintained, so it can't drift out of
# sync with whatever colored version actually builds the docs.
#
# This is a raw HTML fragment meant to be embedded mid-page in an existing
# Sphinx document, not a standalone page -- unlike table.html()'s output,
# it carries its own <style>/<script>, so everything is scoped under the
# .ansitable-palette class rather than touching body/:root, which would
# otherwise leak into the rest of the docs site's styling.
_palette = sorted(
    (
        {"code": int(code), "name": name, "hex": Library.HEX_COLORS[code]}
        for name, code in Library.COLORS.items()
    ),
    key=lambda c: c["code"],
)

_PALETTE_TEMPLATE = """\
<div class="ansitable-palette">
<style>
  .ansitable-palette {{
    --ap-border: #d7dbe2;
    --ap-surface: #f7f8fa;
    --ap-text-dim: #5b6270;
    --ap-accent: #2a6fdb;
    --ap-mono: ui-monospace, SFMono-Regular, "SF Mono", Consolas, "Liberation Mono", monospace;
    margin: 1.5em 0;
  }}
  .ansitable-palette * {{ box-sizing: border-box; }}
  .ansitable-palette .ap-toolbar {{
    display: flex;
    gap: 10px;
    align-items: center;
    flex-wrap: wrap;
    margin-bottom: 6px;
  }}
  .ansitable-palette .ap-search {{
    flex: 1 1 260px;
    min-width: 0;
    font-family: var(--ap-mono);
    font-size: 14px;
    padding: 7px 10px;
    border-radius: 6px;
    border: 1px solid var(--ap-border);
    background: #fff;
  }}
  .ansitable-palette .ap-search:focus {{
    outline: 2px solid var(--ap-accent);
    outline-offset: 1px;
  }}
  .ansitable-palette .ap-count {{
    font-family: var(--ap-mono);
    font-size: 12px;
    color: var(--ap-text-dim);
    white-space: nowrap;
  }}
  .ansitable-palette .ap-hint {{
    font-size: 13px;
    color: var(--ap-text-dim);
    margin: 0 0 14px;
  }}
  .ansitable-palette section {{ margin-top: 20px; }}
  .ansitable-palette .ap-section-title {{
    font-family: var(--ap-mono);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--ap-text-dim);
    margin: 0 0 8px;
  }}
  .ansitable-palette .ap-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(112px, 1fr));
    gap: 6px;
  }}
  .ansitable-palette .ap-cube {{ display: flex; flex-wrap: wrap; gap: 12px; }}
  .ansitable-palette .ap-cube-block {{
    background: var(--ap-surface);
    border: 1px solid var(--ap-border);
    border-radius: 8px;
    padding: 8px;
  }}
  .ansitable-palette .ap-cube-block-label {{
    font-family: var(--ap-mono);
    font-size: 10px;
    color: var(--ap-text-dim);
    margin: 0 0 6px;
  }}
  .ansitable-palette .ap-cube-grid {{
    display: grid;
    grid-template-columns: repeat(6, 22px);
    grid-template-rows: repeat(6, 22px);
    gap: 2px;
  }}
  .ansitable-palette .ap-cube-grid .ap-swatch {{ border-radius: 3px; min-height: 0; }}
  .ansitable-palette .ap-cube-grid .ap-swatch .ap-label {{ display: none; }}
  .ansitable-palette .ap-strip {{ display: flex; flex-wrap: wrap; gap: 5px; }}
  .ansitable-palette .ap-strip .ap-swatch {{ width: 56px; height: 56px; flex: 0 0 auto; }}
  .ansitable-palette .ap-swatch {{
    position: relative;
    border-radius: 6px;
    border: 1px solid rgba(0,0,0,0.12);
    min-height: 64px;
    cursor: pointer;
    display: flex;
    align-items: flex-end;
    padding: 5px;
  }}
  .ansitable-palette .ap-swatch:focus-visible {{
    outline: 2px solid var(--ap-accent);
    outline-offset: 2px;
  }}
  .ansitable-palette .ap-swatch .ap-label {{
    font-family: var(--ap-mono);
    font-size: 10px;
    line-height: 1.3;
    width: 100%;
    word-break: break-word;
  }}
  .ansitable-palette .ap-swatch .ap-name {{ display: block; font-weight: 600; }}
  .ansitable-palette .ap-swatch .ap-hex {{ display: block; opacity: 0.75; font-size: 9px; }}
  .ansitable-palette .ap-swatch .ap-copied {{
    position: absolute;
    inset: 0;
    display: none;
    align-items: center;
    justify-content: center;
    background: rgba(20, 22, 26, 0.72);
    color: #fff;
    font-family: var(--ap-mono);
    font-size: 10.5px;
    font-weight: 600;
    border-radius: 6px;
  }}
  .ansitable-palette .ap-swatch.ap-copied .ap-copied {{ display: flex; }}
  .ansitable-palette .ap-empty {{
    color: var(--ap-text-dim);
    font-family: var(--ap-mono);
    font-size: 13px;
    padding: 16px 0;
  }}
</style>

<div class="ap-toolbar">
  <input class="ap-search" id="ansitable-palette-search" type="text"
         placeholder="Filter by name, e.g. sea_green, grey, orchid..."
         autocomplete="off" spellcheck="false">
  <span class="ap-count" id="ansitable-palette-count"></span>
</div>
<p class="ap-hint">Click a swatch to copy its name.</p>
<div id="ansitable-palette-main"></div>

<script id="ansitable-palette-data" type="application/json">{data}</script>
<script>
(function () {{
  "use strict";
  var palette = JSON.parse(document.getElementById("ansitable-palette-data").textContent);
  var standard = palette.filter(function (c) {{ return c.code <= 15; }});
  var cube = palette.filter(function (c) {{ return c.code >= 16 && c.code <= 231; }});
  var grayscale = palette.filter(function (c) {{ return c.code >= 232; }});

  function luminance(hex) {{
    var r = parseInt(hex.slice(1, 3), 16) / 255;
    var g = parseInt(hex.slice(3, 5), 16) / 255;
    var b = parseInt(hex.slice(5, 7), 16) / 255;
    function lin(c) {{ return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); }}
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
  }}

  function fallbackCopy(text, done) {{
    try {{
      var ta = document.createElement("textarea");
      ta.value = text;
      ta.style.position = "fixed";
      ta.style.opacity = "0";
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
      done();
    }} catch (e) {{
      // clipboard unavailable; the name is still visible as text to select
    }}
  }}

  function copyText(text, el) {{
    function flash() {{
      el.classList.add("ap-copied");
      setTimeout(function () {{ el.classList.remove("ap-copied"); }}, 1100);
    }}
    if (navigator.clipboard && navigator.clipboard.writeText) {{
      navigator.clipboard.writeText(text).then(flash, function () {{ fallbackCopy(text, flash); }});
    }} else {{
      fallbackCopy(text, flash);
    }}
  }}

  function makeSwatch(c, withLabel) {{
    var el = document.createElement("div");
    el.className = "ap-swatch";
    el.style.background = c.hex;
    el.style.color = luminance(c.hex) > 0.42 ? "#14161a" : "#f2f4f7";
    el.tabIndex = 0;
    el.setAttribute("role", "button");
    el.setAttribute("aria-label", c.name + ", " + c.hex + ", copy name");
    el.title = c.name + "  " + c.hex + "  #" + c.code;
    if (withLabel) {{
      var label = document.createElement("span");
      label.className = "ap-label";
      var name = document.createElement("span");
      name.className = "ap-name";
      name.textContent = c.name;
      var hex = document.createElement("span");
      hex.className = "ap-hex";
      hex.textContent = c.hex;
      label.appendChild(name);
      label.appendChild(hex);
      el.appendChild(label);
    }}
    var copied = document.createElement("span");
    copied.className = "ap-copied";
    copied.textContent = "\\u2713 copied";
    el.appendChild(copied);

    function activate() {{ copyText(c.name, el); }}
    el.addEventListener("click", activate);
    el.addEventListener("keydown", function (e) {{
      if (e.key === "Enter" || e.key === " ") {{ e.preventDefault(); activate(); }}
    }});
    return el;
  }}

  var main = document.getElementById("ansitable-palette-main");
  var searchInput = document.getElementById("ansitable-palette-search");
  var countEl = document.getElementById("ansitable-palette-count");

  function render(filter) {{
    var q = (filter || "").trim().toLowerCase();
    main.innerHTML = "";
    var shown = 0;

    function matches(c) {{ return !q || c.name.indexOf(q) !== -1; }}

    var standardMatches = standard.filter(matches);
    if (standardMatches.length) {{
      var s1 = document.createElement("section");
      s1.innerHTML = '<p class="ap-section-title">Standard &middot; 0&ndash;15</p>';
      var g1 = document.createElement("div");
      g1.className = "ap-grid";
      standardMatches.forEach(function (c) {{ g1.appendChild(makeSwatch(c, true)); shown++; }});
      s1.appendChild(g1);
      main.appendChild(s1);
    }}

    var cubeMatches = cube.filter(matches);
    if (cubeMatches.length) {{
      var s2 = document.createElement("section");
      s2.innerHTML = '<p class="ap-section-title">216-color cube &middot; 16&ndash;231</p>';
      if (q) {{
        var gq = document.createElement("div");
        gq.className = "ap-grid";
        cubeMatches.forEach(function (c) {{ gq.appendChild(makeSwatch(c, true)); shown++; }});
        s2.appendChild(gq);
      }} else {{
        var wrap = document.createElement("div");
        wrap.className = "ap-cube";
        for (var block = 0; block < 6; block++) {{
          var blockEl = document.createElement("div");
          blockEl.className = "ap-cube-block";
          blockEl.innerHTML = '<p class="ap-cube-block-label">red level ' + block + "</p>";
          var cg = document.createElement("div");
          cg.className = "ap-cube-grid";
          for (var k = 0; k < 36; k++) {{
            var c = cube[block * 36 + k];
            cg.appendChild(makeSwatch(c, false));
            shown++;
          }}
          blockEl.appendChild(cg);
          wrap.appendChild(blockEl);
        }}
        s2.appendChild(wrap);
      }}
      main.appendChild(s2);
    }}

    var grayMatches = grayscale.filter(matches);
    if (grayMatches.length) {{
      var s3 = document.createElement("section");
      s3.innerHTML = '<p class="ap-section-title">Grayscale ramp &middot; 232&ndash;255</p>';
      var strip = document.createElement("div");
      strip.className = "ap-strip";
      grayMatches.forEach(function (c) {{ strip.appendChild(makeSwatch(c, !!q)); shown++; }});
      s3.appendChild(strip);
      main.appendChild(s3);
    }}

    if (!shown) {{
      var empty = document.createElement("p");
      empty.className = "ap-empty";
      empty.textContent = 'No colors match "' + q + '".';
      main.appendChild(empty);
    }}

    countEl.textContent = shown + " / 256 colors";
  }}

  var raf = null;
  searchInput.addEventListener("input", function () {{
    if (raf) cancelAnimationFrame(raf);
    raf = requestAnimationFrame(function () {{ render(searchInput.value); }});
  }});

  render("");
}})();
</script>
</div>
"""

(output_dir / "color_palette.html").write_text(
    _PALETTE_TEMPLATE.format(data=json.dumps(_palette))
)
print("✓ Generated color_palette.html")
