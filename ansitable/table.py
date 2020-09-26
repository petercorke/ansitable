#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 21:43:18 2020

@author: corkep
"""
import copy

try:
    from colored import fg, bg, attr
    _color = True
    print('using colored output')
except ImportError:
    print('colored not found')
    _color = False

def FG(c): return fg(c) if _color else ''
def BG(c): return bg(c) if _color else ''
def ATTR(c): return attr(c) if _color else ''

class Column():
    def __init__(self, name, fmt="{}", width=None,
        colcolor=None, colbgcolor=None, colstyle=None, colalign=">", 
        headcolor=None, headbgcolor=None, headstyle=None, headalign=">",
        formatter=None):
        self.name = name
        self.fmt = fmt

        if headalign is None:
            self.headalign = colalign
        self.colcolor = colcolor
        self.colbgcolor = colbgcolor
        self.colstyle = colstyle
        self.colalign = colalign

        self.headcolor = headcolor
        self.headbgcolor = headbgcolor
        self.headstyle = headstyle
        self.headalign = headalign


        self.width = width
        
        self.formatter = formatter
        self.maxwidth = len(name)

    def _settyle(self, header):
        if header:
            color = self.headcolor
            bgcolor = self.headbgcolor
            style = self.headstyle
        else:
            color = self.colcolor
            bgcolor = self.colbgcolor
            style = self.colstyle

        text = ""
        if color is not None:
            text += FG(color)
        if bgcolor is not None:
            text += BG(bgcolor)
        if style is not None:
            text += ATTR(styledict[style])
        return text

def _spaces(n):
    return " " * n

def _aligntext(opt, text, n):
    gap = n - len(text)
    if  opt == '<':
        return text + _spaces(gap)
    elif opt == '>':
        return _spaces(gap) + text
    elif opt == '^':
        g1 = gap // 2
        g2 = gap - g1
        return _spaces(g1) + text + _spaces(g2)

# thin, thin+round, thick, double
_tl = [ord('+'), 0x250c, 0x256d, 0x250f, 0x2554]
_tr = [ord('+'), 0x2510, 0x256e, 0x2513, 0x2557]
_bl = [ord('+'), 0x2514, 0x2570, 0x2517, 0x255a]
_br = [ord('+'), 0x2518, 0x256f, 0x251b, 0x255c]
_lj = [ord('+'), 0x251c, 0x251c, 0x2523, 0x2560]
_rj = [ord('+'), 0x2524, 0x2524, 0x252b, 0x2563]
_tj = [ord('+'), 0x252c, 0x252c, 0x2533, 0x2566]
_bj = [ord('+'), 0x2534, 0x2534, 0x253b, 0x2569]
_xj = [ord('+'), 0x253c, 0x253c, 0x254b, 0x256c]
_hl = [ord('-'), 0x2500, 0x2500, 0x2501, 0x2550]
_vl = [ord('|'), 0x2502, 0x2502, 0x2503, 0x2551]

borderdict = {"ascii": 0, "thin": 1, "round": 2, "thick": 3, "double": 4, "thick-thin": 5, "double-thin":6}
styledict = {"bold": 1, "dim": 2, "underlined": 4, "blink": 5, "reverse":7}
class TableFormat:
    
    def __init__(self, *pos, colsep = 2, offset=0, border=None, bordercolor=None, ellipsis=True):
 
        self.columns = pos
        self.colsep = colsep
        self.offset = offset
        self.ellipsis = ellipsis
        self.rows = []
        self.bordercolor = bordercolor
        if border is not None:
            # printing borderes, adjust some other parameters
            if self.offset == 0:
                self.offset = 1
            self.colsep |= 1  # make it odd

            self.border = borderdict[border]
        else:
            self.border = None
            

        for c in self.columns:
            if not isinstance(c, Column):
                raise TypeError('expecting a lists of Column objects')

    def add(self, *data):
        assert len(data) == len(self.columns), 'wrong number of data items added'
        row = []
        for d, c in zip(data, self.columns):

            if c.formatter is not None:
                s = c.formatter(d)
            else:
                s = c.fmt.format(d)
            if c.width is not None and len(s) > c.width:
                if self.ellipsis:
                    s = s[:c.width - 3] + "..."
                else:
                    s = s[:c.width]
            c.maxwidth = max(c.maxwidth, len(s))
            row.append(s)
        
        self.rows.append(row)
            
    def _topline(self):
        self._line(_tl, _tj, _tr)

    def _midline(self):
        self._line(_lj, _xj, _rj)

    def _bottomline(self):
        self._line(_bl, _bj, _br)

    def _line(self, left, mid, right):
        if self.border is not None:
            b = self.border
            c2 = self.colsep // 2
            text = _spaces(self.offset - 1)
            if self.bordercolor is not None:
                text += FG(self.bordercolor)
            text += chr(left[b])
            for c in self.columns:
                text += chr(_hl[b]) * (c.width + c2)
                if not c.last:
                    text += chr(mid[b]) + chr(_hl[b]) * c2 
            text += chr(right[b])
            if self.bordercolor is not None:
                text += ATTR(0)
            print(text)

    def _vline(self):
        if self.border is not None:
            text = ""
            b = self.border
            if self.bordercolor is not None:
                text += FG(self.bordercolor)
            text += chr(_vl[b])
            if self.bordercolor is not None:
                text += ATTR(0)
            return text


    def _printline(self, header=False, row=None):
        if self.border is not None:
            b = self.border
            text = _spaces(self.offset - 1) + self._vline()
            for i, c in enumerate(self.columns):

                ansi = c._settyle(header)
                text += ansi
                if header:
                    text += _aligntext(c.headalign, c.name, c.width)
                else:
                    text += _aligntext(c.colalign, row[i], c.width)
                if len(ansi) > 0:
                    text += ATTR(0)

                c2 = self.colsep // 2
                if not c.last:
                    text += _spaces(c2) + self._vline() +  _spaces(c2)
                else:
                    text += _spaces(c2) + self._vline()
        else:
            # no border
            text = _spaces(self.offset)

            for i, c in enumerate(self.columns):
                ansi = c._settyle(header)
                text += ansi
                if header:
                    text += _aligntext(c.headalign, c.name, c.width)
                else:
                    text += _aligntext(c.colalign, row[i], c.width)
                if len(ansi) > 0:
                    text += ATTR(0)
                text +=  _spaces(self.colsep)

        print(text)

    def print(self):
        for i, c in enumerate(self.columns):
            c.width = c.width or c.maxwidth
            c.last = i == len(self.columns) - 1

        # heading
        self._topline()

        self._printline(header=True)

        self._midline()

        # rows

        for row in self.rows:
            self._printline(header=False, row=row)
        
        # footer
        self._bottomline()
            
            
if __name__ == "__main__":
    
    # table = TableFormat(
    #     Column("Axis", "{:d}", colalign="^", colcolor="red", headstyle="reverse"),
    #     Column("q", "{}", width=10, colcolor="blue"),
    #     Column("d", "{:.2f}"),
    #     Column("a", "{:.2f}"),
    #     Column("⍺", "{:.2f}"), offset=4, colsep=3, border="thick", bordercolor="green")

    # table.add(1, "q1", 0, 0, 1)
    # table.add(2456789, "q2 + 90", 0, 0, 1)
    # table.add(3, "q3", 0, 0, 1)
    # table.add(3, "q3abcdefghihklmnop", 0, 0, 1)

    # table.print()

    table = TableFormat(
        Column("col1"),
        Column("column 2 has a big header"),
        Column("column 3")
    )
    table.add("aaaaaaaaa", 2.2, 3)
    table.add("bbbbbbbbbbbbb", 5.5, 6)
    table.add("ccccccc", 8.8, 9)
    table.print()

    table = TableFormat(
        Column("col1"),
        Column("column 2 has a big header", "{:.3g}"),
        Column("column 3", "{:-10.4f}")
    )
    table.add("aaaaaaaaa", 2.2, 3)
    table.add("bbbbbbbbbbbbb", 5.5, 6)
    table.add("ccccccc", 8.8, 9)
    table.print()

    table = TableFormat(
        Column("col1", width=10),
        Column("column 2 has a big header", "{:.3g}"),
        Column("column 3", "{:-10.4f}")
    )
    table.add("aaaaaaaaa", 2.2, 3)
    table.add("bbbbbbbbbbbbb", 5.5, 6)
    table.add("ccccccc", 8.8, 9)
    table.print()

    table = TableFormat(
        Column("col1"),
        Column("column 2 has a big header"),
        Column("column 3"),
        border="ascii"
    )
    table.add("aaaaaaaaa", 2.2, 3)
    table.add("bbbbbbbbbbbbb", 5.5, 6)
    table.add("ccccccc", 8.8, 9)
    table.print()

    table = TableFormat(
        Column("col1"),
        Column("column 2 has a big header"),
        Column("column 3"),
        border="thick"
    )
    table.add("aaaaaaaaa", 2.2, 3)
    table.add("bbbbbbbbbbbbb", 5.5, 6)
    table.add("ccccccc", 8.8, 9)
    table.print()

    table = TableFormat(
        Column("col1"),
        Column("column 2 has a big header", colalign="^"),
        Column("column 3"),
        border="thick"
    )
    table.add("aaaaaaaaa", 2.2, 3)
    table.add("bbbbbbbbbbbbb", 5.5, 6)
    table.add("ccccccc", 8.8, 9)
    table.print()

    table = TableFormat(
        Column("col1", headalign="<"),
        Column("column 2 has a big header", colalign="^"),
        Column("column 3", colalign="<"),
        border="thick"
    )
    table.add("aaaaaaaaa", 2.2, 3)
    table.add("bbbbbbbbbbbbb", 5.5, 6)
    table.add("ccccccc", 8.8, 9)
    table.print()

    table = TableFormat(
        Column("col1", headalign="<"),
        Column("column 2 has a big header", colalign="^", colstyle="reverse"),
        Column("column 3", colalign="<"),
        border="thick"
    )
    table.add("aaaaaaaaa", 2.2, 3)
    table.add("bbbbbbbbbbbbb", 5.5, 6)
    table.add("ccccccc", 8.8, 9)
    table.print()

    table = TableFormat(
        Column("col1", headalign="<", colcolor="red", headstyle="underlined"),
        Column("column 2 has a big header", colalign="^", colstyle="reverse"),
        Column("column 3", colalign="<", colbgcolor="green"),
        border="thick", bordercolor="blue"
    )
    table.add("aaaaaaaaa", 2.2, 3)
    table.add("bbbbbbbbbbbbb", 5.5, 6)
    table.add("ccccccc", 8.8, 9)
    table.print()  