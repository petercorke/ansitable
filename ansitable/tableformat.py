#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 21:43:18 2020

@author: corkep
"""
import copy

class Column():
    def __init__(self, name, fmt, align="<", width=None, color=None, hcolor=None, formatter=None, colsep="", headsep=False, colgap=2):
        self.name = name
        self.fmt = fmt
        self.align = align
        self.width = width
        self.color = color
        self.hcolor = hcolor
        self.formatter = formatter
        self.colsep = colsep
        self.headsep = headsep
        self.colgap = colgap

class TableFormat:
    
    def __init__(self, *pos, colsep = 2):
        """
        Tabular printing
        
        :param table: format string
        :type table: str
        :param extrasep: extra separation between columns, default 2
        :type extrasep: int
        :return: a format string
        :rtype: str
        
        Given an input string like::
        
            "col1[s] col2[d] col3[10s] col4[3d]"
            
        where the square brackets denote type  (as per `format`) and the
        number if given is a minumum column width.  The actual column width
        is the maximum of the given value and the width of the heading text
        plus `extrasep`.
        
        Then print the header and a separator line::
        
        col1  col2  col3        col4
        ----  ----  ----------  ----

        and return a format string that can be used with `format` to format
        the arguments for subsequent data rows.
        """
        # parse the format line
        # re_fmt = re.compile(r"([a-zA-Z]+)\[(\-?[0-9]*|\*)([a-z])\]")
        
        # colheads = []
        # varwidth = {}
        # columns = []
        
        # for i, col in enumerate(table.split(' ')):
        #     m = re_fmt.search(col)
        #     colhead = m.group(1)
        #     colwidth = m.group(2)
        #     if colwidth == '':
        #         colwidth = len(colhead) + colsep
        #         coljust = '<'
        #     elif colwidth == '*':
        #         varwidth[i] = 0
        #         colwidth = None
        #         coljust = '<'
        #     else:
        #         w = int(colwidth)
        #         if w < 0:
        #             coljust = '>'
        #             w = -w
        #         else:
        #             coljust = '<'
        #         colwidth = max(w, len(colhead) + colsep)
        #     colfmt = m.group(3)
        #     columns.append( (colhead, colfmt, coljust, colwidth) )
        # else:
        #     self.ncols = i + 1
            
        # self.data = []
        # self.colsep = colsep
        # self.columns = columns
        # self.varwidth = varwidth

        for column in pos:
            if not isinstance(column, Column):
                raise TypeError('expecting a lists of Column objects')
        self.columns = pos

    
    def add(self, *data):
        assert len(data) == len(self.columns), 'wrong number of data items added'
        for d, c in zip(data, self.columns):
            c.data.append(copy.copy(d))
    
    def print(self):
        hfmt = ""
        cfmt = ""
        sep = ""
        
        colheads = []
        for i, col in enumerate(self.columns):
            colhead, colfmt, coljust, colwidth = col
            
            colheads.append(colhead)
            
            if colwidth is None:
                colwidth = self.varwidth[i]
                
            if colfmt == 'd':
                hfmt += "{:>%ds}" % (colwidth,)
            else:
                hfmt += "{:%ds}" % (colwidth,)
                
            cfmt += "{:%s%d%s}" % (coljust, colwidth, colfmt)
            hfmt += ' ' * self.colsep
            cfmt += ' ' * self.colsep
            sep += '-' * colwidth + '  '
            
        print(hfmt.format(*colheads))
        print(sep)
        
        for d in self.data:
            print( cfmt.format(*d))
            
    
            
if __name__ == "__main__":
    
    table = TableFormat(
        Column("Axis", ">%d", align="^"),
        Column("q", "<%s"),
        Column("d", "%.2f"),
        Column("a", "%.2f"),
        Column("⍺", "%.3f"))

    table.add("q1", 0, 0, 1)
    table.add("q2 + 90", 0, 0, 1)
    table.add("q3", 0, 0, 1)

    table.print()

