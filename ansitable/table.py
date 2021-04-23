#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 21:43:18 2020

@author: corkep
"""
import sys

try:
    from colored import fg, bg, attr
    _colored = True
    # print('using colored output')
except ImportError:
    # print('colored not found')
    _colored = False

# ------------------------------------------------------------------------- #

class Column():
    def __init__(self, name, fmt="{}", width=None,
        colcolor=None, colbgcolor=None, colstyle=None, colalign=">", 
        headcolor=None, headbgcolor=None, headstyle=None, headalign=">"
        ):
        """
        [summary]

        :param name: Name of column, also the column heading
        :type name: str
        :param fmt: Python format string, defaults to "{}"
        :type fmt: str, optional
        :param width: Column width, defaults to auto-fit
        :type width: int, optional
        :param colcolor: Color of column text, defaults to None
        :type colcolor: str, optional
        :param colbgcolor: Color of column background, defaults to None
        :type colbgcolor: str, optional
        :param colstyle: Column text style, see table below, defaults to None
        :type colstyle: str, optional
        :param colalign: Column data alignement, see table below, defaults to ">"
        :type colalign: str, optional
        :param headcolor: Color of heading text, defaults to None
        :type headcolor: str, optional
        :param headbgcolor: Color of heading background, defaults to None
        :type headbgcolor: str, optional
        :param headstyle: Heading text style, see table below, defaults to None
        :type headstyle: str, optional
        :param headalign: Heading text alignement, see table below, defaults to ">"
        :type headalign: str, optional

        ===========   =======================
        Alignment     Description
        ===========   =======================
        "<"           Left
        "^"           Centre
        ">"           Right (default)
        ===========   =======================


        ===========   ==========================================================
        Border        Description
        ===========   ==========================================================
        ascii         Use ASCII +-| characters
        thin          Use ANSI thin box-drawing characters
        thin+round    Use ANSI thin box-drawing characters with rounded corners
        thick         Use ANSI thick box-drawing characters
        double        Use ANSI double-line box-drawing characters
        ===========   ==========================================================


        ===========   =============================================
        Style         Description
        ===========   =============================================
        bold          bold font
        dim           low brightness font
        underlined    text is underlined
        blink         text is blinking
        reverse       text and background colors are reversed
        ===========   =============================================

        Implementation of these options depends heavily on the terminal emulator
        used.
        
        """

        self.name = name
        self.fmt = fmt
        self.formatted = []
        self.fgcolor = []
        self.table = None

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
            text += self.table.FG(color)
        if bgcolor is not None:
            text += self.table.BG(bgcolor)
        if style is not None:
            text += self.table.ATTR(styledict[style])
        return text

def _spaces(n):
    return " " * n

def _aligntext(opt, text, n, color=None):
    gap = n - len(text)
    if color:
        # text = FG(color) + text + ATTR(0)
        text = color[0] + text + color[1]
    if  opt == '<':
        return text + _spaces(gap)
    elif opt == '>':
        return _spaces(gap) + text
    elif opt == '^':
        g1 = gap // 2
        g2 = gap - g1
        return _spaces(g1) + text + _spaces(g2)

#       ascii, thin, thin+round, thick, double
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

# ------------------------------------------------------------------------- #

class ANSIMatrix:

    def __init__(self, style='thin', fmt='{:< 10.3g}', squish=True, squishtol=100):
        """
        [summary]

        :param style: Bracket format, defaults to 'thin'
        :type style: str, optional
        :param fmt: [description], defaults to '{:< 10.3g}'
        :type fmt: str, optional
        :param squish: [description], defaults to True
        :type squish: bool, optional
        :param squishtol: [description], defaults to 100
        :type squishtol: int, optional
        """

        import numpy as np  # only import if matrix is used
        self.style = borderdict[style]
        self.fmt = fmt
        self.width = len(fmt.format(1))
        if squish:
            self.squish = squishtol * np.finfo(float).eps
        else:
            self.squish = None

    def str(self, matrix, suffix_super='', suffix_sub=''):
        """
        Output the table as a string

        :param matrix: NumPy matrix to format
        :type matrix: 1d or 2d ndarray
        :param suffix_super: Right superscript, defaults to ''
        :type suffix_super: str, optional
        :param suffix_sub: Right subscript, defaults to ''
        :type suffix_sub: str, optional
        :raises ValueError: [description]
        :return: ANSI string
        :rtype: str
        """

        import numpy as np  # only import if matrix is used

        if len(matrix.shape) == 1:
            ncols = matrix.shape[0]
            matrix = matrix.reshape((1, -1))
        elif len(matrix.shape) == 2:
            ncols = matrix.shape[1]
        else:
            raise ValueError('Only 1D and 2D arrays supported')

        mwidth = ncols * self.width + (ncols - 1)
        if self.squish is None:
            m2 = matrix
        else:
            m2 = np.where(abs(matrix) < self.squish, 0, matrix)
        b = self.style

        s = chr(_tl[b]) + ' ' * mwidth + chr(_tr[b]) + suffix_super + '\n'
        for row in m2:
            s += chr(_vl[b]) + ' '.join([self.fmt.format(x) for x in row]) + chr(_vl[b]) + '\n'
        s += chr(_bl[b]) + ' ' * mwidth + chr(_br[b]) + suffix_sub
        return s

    def print(self, matrix, *pos, file=sys.stdout, **kwargs):
        """
        Print the matrix

        :param file: Print the matrix to this file, defaults to stdout
        :type file: writeable object, optional

        .. note:: Accepts the same arguments as ``str``.

        """

        print(self.str(matrix, *pos, **kwargs), file=file)

# ------------------------------------------------------------------------- #

class ANSITable:
    _color = _colored

    def __init__(self, *pos, colsep = 2, offset=0, border=None, bordercolor=None, ellipsis=True, columns=None, header=True, color=True):
        """
        Create a table object

        :param colsep: Separation between columns, defaults to 2
        :type colsep: int, optional
        :param offset: Horizontal offset of the whole table, defaults to 0
        :type offset: int, optional
        :param border: Type of border, defaults to None
        :type border: [type], optional
        :param bordercolor: Name of color to draw border in, defaults to None
        :type bordercolor: str, optional
        :param ellipsis: truncated lines are shown with an ellipsis, defaults to True
        :type ellipsis: bool, optional
        :param columns: [description], defaults to None
        :type columns: [type], optional
        :param header: Show table header, defaults to True
        :type header: bool, optional
        :param color: [description], defaults to True
        :type color: bool, optional
        :raises TypeError: [description]

        A table can be created in several different ways::

            table = ANSITable("col1", "column 2 has a big header", "column 3")

            table = ANSITable(
                Column("col1"),
                Column("column 2 has a big header", "{:.3g}"),
                Column("column 3", "{:-10.4f}")
            )

            table = ANSITable()
            table.addcolumnColumn("col1"),
            table.addcolumnColumn("column 2 has a big header", "{:.3g}"),
            table.addcolumnColumn("column 3", "{:-10.4f}")

        The first option is quick and easy but does not allow any control of
        formatting or alignment.
        """
        self.colsep = colsep
        self.offset = offset
        self.ellipsis = ellipsis
        self.rows = []
        self.bordercolor = bordercolor
        self.header = header
        self.color = color and self._color



        self.border = border
        
        self.nrows = 0
        self.columns = []
        for c in pos:
            if isinstance(c, str):
                c = Column(c)
                c.table = self
                self.columns.append(c)
            elif isinstance(c, Column):
                c.table = self
                self.columns.append(c)
            else:
                raise TypeError('expecting a lists of Column objects')
        if len(self.columns) == 0 and columns is not None:
            for _ in range(columns):
                self.columns.append("")

    def addcolumn(self, name, **kwargs):
        """
        Add a column to the table

        :param name: column heading
        :type name: str

        An alternative way to create a table, column at a time.

        Example::

            table = ANSITable()
            table.addcolumnColumn("col1"),
            table.addcolumnColumn("column 2 has a big header", "{:.3g}"),
            table.addcolumnColumn("column 3", "{:-10.4f}")

        .. note:: Additional arguments are passed directly to ``Column``.
    
        """
        self.columns.append(Column(name, **kwargs))

    def row(self, *values):
        """
        Add a row of data

        :raises ValueError: invalid format string for the data provided

        ``table.row(d1, d2, ... dN)`` add data items that comprise a row of the
        table.  ``N`` is the number of columns.

        The data items can be any type, but the format string specified at
        table creation must be compatible.
        """
        assert len(values) == len(self.columns), 'wrong number of data items added'

        for value, c in zip(values, self.columns):
            if c.fmt is None:
                s = value
            elif isinstance(c.fmt, str):
                s = c.fmt.format(value)
            elif callable(c.fmt):
                s = c.fmt(value)
            else:
                raise ValueError('fmt must be valid format string or callable')

            # handle a FG color specifier
            if s.startswith('<<'):
                # color specifier is given
                end = s.find('>>')
                color = s[2:end]
                s = s[end+2:]
            else:
                color = None

            if c.width is not None and len(s) > c.width:
                if self.ellipsis:
                    s = s[:c.width - 1] + "\u2026"
                else:
                    s = s[:c.width]
            c.maxwidth = max(c.maxwidth, len(s))

            c.formatted.append(s)
            c.fgcolor.append(color)
        self.nrows += 1

    def rule(self):
        """
        Add a rule to the table

        This is a horizontal line across all columns, used to delineate parts
        of the table.
        """
        for c in self.columns:
            c.formatted.append(None)
            c.fgcolor.append(None)
        self.nrows += 1

    def _topline(self):
        return self._line(_tl, _tj, _tr)

    def _midline(self):
        return self._line(_lj, _xj, _rj)

    def _bottomline(self):
        return self._line(_bl, _bj, _br)

    def _line(self, left, mid, right):
        if self.borderdict is  None:
            return ""
        else:
            b = self.borderdict
            c2 = self.colsep // 2
            text = _spaces(self.offset - 1)
            if self.bordercolor is not None:
                text += self.FG(self.bordercolor)
            text += chr(left[b])
            for c in self.columns:
                text += chr(_hl[b]) * (c.width + c2)
                if not c.last:
                    text += chr(mid[b]) + chr(_hl[b]) * c2 
            text += chr(right[b])
            if self.bordercolor is not None:
                text += self.ATTR(0)
            return text + "\n"

    def _vline(self):
        if self.borderdict is not None:
            text = ""
            b = self.borderdict
            if self.bordercolor is not None:
                text += self.FG(self.bordercolor)
            text += chr(_vl[b])
            if self.bordercolor is not None:
                text += self.ATTR(0)
            return text


    def _row(self, row=None):

        if row is not None and self.columns[0].formatted[row] is None:
            # it's a horizontal rule
            return self._midline()

        if self.borderdict is not None:
            # has border
            text = _spaces(self.offset - 1) + self._vline()
            for c in self.columns:

                ansi = c._settyle(row is None)
                text += ansi
                if row is None:
                    # header
                    text += _aligntext(c.headalign, c.name, c.width)
                else:
                    # table row proper
                    text += _aligntext(c.colalign, c.formatted[row], c.width, 
                        (self.FG(c.fgcolor[row]), self.ATTR(0)))
                if len(ansi) > 0:
                    text += self.ATTR(0)

                c2 = self.colsep // 2
                if not c.last:
                    text += _spaces(c2) + self._vline() +  _spaces(c2)
                else:
                    text += _spaces(c2) + self._vline()
        else:
            # no border
            text = _spaces(self.offset)

            for c in self.columns:
                ansi = c._settyle(row is None)
                text += ansi
                if row is None:
                    # header
                    text += _aligntext(c.headalign, c.name, c.width)
                else:
                    # table row proper
                    text += _aligntext(c.colalign, c.formatted[row], c.width, 
                                (self.FG(c.fgcolor[row]), self.ATTR(0)))
                if len(ansi) > 0:
                    text += self.ATTR(0)
                text +=  _spaces(self.colsep)

        return text + "\n"

    def print(self, file=None):
        """
        Print the table

        :param file: Print the table to this file, defaults to stdout
        :type file: writeable object, optional

        Example::

            table = ANSITable("col1", "column 2 has a big header", "column 3")
            table.row("aaaaaaaaa", 2.2, 3)
            table.row("bbbbbbbbbbbbb", -5.5, 6)
            table.row("ccccccc", 8.8, -9)
            table.print()
            
            +--------------+---------------------------+----------+
            |         col1 | column 2 has a big header | column 3 |
            +--------------+---------------------------+----------+
            |    aaaaaaaaa |                       2.2 |        3 |
            |bbbbbbbbbbbbb |                      -5.5 |        6 |
            |      ccccccc |                       8.8 |       -9 |
            +--------------+---------------------------+----------+

        """

        try:
            print(str(self), file=file)
        except UnicodeEncodeError:
            self.border = 'ascii'
            print(str(self), file=file)

    def __str__(self):
        """
        Output the table as a string

        :return: ANSI string
        :rtype: str
        """

        if self.border is not None:
            # printing borders, adjust some other parameters
            if self.offset == 0:
                self.offset = 1
            self.colsep |= 1  # make it odd

            self.borderdict = borderdict[self.border]
        else:
            self.borderdict = None

        for i, c in enumerate(self.columns):
            c.width = c.width or c.maxwidth
            c.last = i == len(self.columns) - 1

        text = ""

        # heading
        text += self._topline()
        if self.header:
            text += self._row()
            text += self._midline()

        # rows
        for i in range(self.nrows):
            text += self._row(i)
        
        # footer
        text += self._bottomline()

        return text

    def markdown(self):
        """
        Output the table in MarkDown format

        :return: ASCII markdown text
        :rtype: str

        Example::

            table = ANSITable("col1", "column 2 has a big header", "column 3")
            table.row("aaaaaaaaa", 2.2, 3)
            table.row("bbbbbbbbbbbbb", -5.5, 6)
            table.row("ccccccc", 8.8, -9)
            table.markdown()
            
            |          col1 | column 2 has a big header | column 3 |
            | ------------: | ------------------------: | -------: |
            |     aaaaaaaaa |                       2.2 |        3 |
            | bbbbbbbbbbbbb |                      -5.5 |        6 |
            |       ccccccc |                       8.8 |       -9 |

        .. note::
            - supports column alignment
            - does not support header alignment, same as column
        """

        # markdown table setup
        s = ''

        # column headers
        for c in self.columns:
            s += '| ' + _aligntext(c.headalign, c.name, c.width) + ' '
        s += "|\n"

        for c in self.columns:
            if c.headalign == '<':
                bar = ':' + '-' * (c.width - 1)
            elif c.headalign == '^':
                bar = ':' + '-' * (c.width - 2) + ':'
            elif c.headalign == '>':
                bar = '-' * (c.width - 1) + ':'
            s += '| ' + bar + ' '
        s += "|\n"

        # rows
        for i in range(self.nrows):
            for c in self.columns:
                s += '| ' + _aligntext(c.colalign, c.formatted[i], c.width) + ' '
            s += "|\n"

        return s

    def latex(self):
        r"""
        Output the table in LaTeX format

        :return: ASCII markdown text
        :rtype: str

        Example::

            table = ANSITable("col1", "column 2 has a big header", "column 3")
            table.row("aaaaaaaaa", 2.2, 3)
            table.row("bbbbbbbbbbbbb", -5.5, 6)
            table.row("ccccccc", 8.8, -9)
            table.latex()

            \begin{tabular}{ |r|r|r| }\hline
            \multicolumn{1}{|r|}{col1} & \multicolumn{1}{|r|}{column 2 has a big header} & \multicolumn{1}{|r|}{column 3}\\\hline\hline
            aaaaaaaaa & 2.2 & 3 \\
            bbbbbbbbbbbbb & -5.5 & 6 \\
            ccccccc & 8.8 & -9 \\
            \hline
            \end{tabular}

        .. note::
            - supports column alignment
            - supports header alignment
        """

        # LaTeX tabular setup
        s = "\\begin{tabular}{ |"
        for c in self.columns:
            if c.colalign == '<':
                s += 'l|'
            elif c.colalign == '^':
                s += 'c|'
            elif c.colalign == '>':
                s += 'r|'
        s += " }\\hline\n"

        # column headers
        first = True
        for c in self.columns:
            if first:
                first = False
            else:
                s += ' & '

            s += '\\multicolumn{1}{'
            if c.headalign == '<':
                s += '|l|'
            elif c.headalign == '^':
                s += '|c|'
            elif c.headalign == '>':
                s += '|r|'
            s += "}{" + c.name + "}"

        s += "\\\\\\hline\\hline\n"
        # rows
        for i in range(self.nrows):
            first = True
            for c in self.columns:
                if first:
                    first = False
                else:
                    s += ' & '
                s += c.formatted[i]
            s += " \\\\\n"
        s += "\\hline\n"
        s += "\\end{tabular}\n"
        return s

    def FG(self, c):
        if self.color and c is not None:
            return fg(c)
        else:
            return ""

    def BG(self, c):
        if self.color and c is not None:
            return bg(c)
        else:
            return ""

    def ATTR(self, c):
        if self.color and c is not None:
            return attr(c)
        else:
            return "" 

if __name__ == "__main__":

    import numpy as np

    # -------------------------------- test ANSIMatrix
    m = np.arange(16).reshape((4,4)) /10 - 0.8
    m[0,0] = 1.23456e-14
    print(m)
    print(np.array2string(m))

    formatter = ANSIMatrix(style='thick', squish=True)

    formatter.print(m)

    formatter.print(m, suffix_super='T', suffix_sub='3')

    m = np.arange(4) / 4 - 0.5
    formatter.print(m, 'T')

    # -------------------------------- test ANSITable

    table = ANSITable("col1", "column 2 has a big header", "column 3", color=False)
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.row("ccccccc", 8.8, -9)
    table.print()

    table = ANSITable("col1", "column 2 has a big header", "column 3", color=False)
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("<<red>>bbbbbbbbbbbbb", 5.5, 6)
    table.row("<<blue>>ccccccc", 8.8, -9)
    table.print()

    table = ANSITable(
        Column("col1"),
        Column("column 2 has a big header"),
        Column("column 3")
    )
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.row("ccccccc", 8.8, -9)
    table.print()

    table = ANSITable(
        Column("col1"),
        Column("column 2 has a big header", "{:.3g}"),
        Column("column 3", "{:-10.4f}")
    )
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.row("ccccccc", 8.8, -9)
    table.print()

    table = ANSITable(
        Column("col1", width=10),
        Column("column 2 has a big header", "{:.3g}"),
        Column("column 3", "{:-10.4f}")
    )
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.row("ccccccc", 8.8, -9)
    table.print()

    table = ANSITable(
        Column("col1"),
        Column("column 2 has a big header"),
        Column("column 3"),
        border="ascii"
    )
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.row("ccccccc", 8.8, -9)
    table.print()

    table = ANSITable(
        Column("col1"),
        Column("column 2 has a big header"),
        Column("column 3"),
        border="thick"
    )
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.row("ccccccc", 8.8, -9)
    table.print()

    table = ANSITable(
        Column("col1"),
        Column("column 2 has a big header", colalign="^"),
        Column("column 3"),
        border="thick"
    )
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.row("ccccccc", 8.8, -9)
    table.print()

    table = ANSITable(
        Column("col1", headalign="<"),
        Column("column 2 has a big header", colalign="^"),
        Column("column 3", colalign="<"),
        border="thick"
    )
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.row("ccccccc", 8.8, -9)
    table.print()

    table = ANSITable(
        Column("col1", headalign="<"),
        Column("column 2 has a big header", colalign="^", colstyle="reverse"),
        Column("column 3", colalign="<"),
        border="thick"
    )
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.row("ccccccc", 8.8, -9)
    table.print()

    table = ANSITable(
        Column("col1", headalign="<", colcolor="red", headstyle="underlined"),
        Column("column 2 has a big header", colalign="^", colstyle="reverse"),
        Column("column 3", colalign="<", colbgcolor="green", fmt="{: d}"),
        border="thick", bordercolor="blue"
    )
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.rule()
    table.row("ccccccc", 8.8, -9)
    table.print()


    table = ANSITable("col1", "column 2 has a big header", "column 3")
    table.row("aaaaaaaaa", 2.2, 3)
    table.row("bbbbbbbbbbbbb", -5.5, 6)
    table.row("ccccccc", 8.8, -9)
    table.print()
    print(table.latex())
    print(table.markdown())