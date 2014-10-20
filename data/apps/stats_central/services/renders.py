# -*- coding: utf-8 -*-
"""
 The MIT License (MIT)

Copyright (c) 2014 Jacek Markowski

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
from PySide import QtGui

COLORS = {
    'color_1': QtGui.QColor('#E6E6FA'),
    'color_2': QtGui.QColor('#BFBFBF'),
    'color_home': QtGui.QColor('#71CA80'),
    'color_away': QtGui.QColor('#E1571F'),
    'color_win': QtGui.QColor('#90D889'),
    'color_draw': QtGui.QColor('#9894EB'),
    'color_lose': QtGui.QColor('#DE7C7C'),
    'color_few_matches': QtGui.QColor('#9894EB'),
    'palette': '#39A1B2'
}


def render(home_team, away_team, data, labels, ui_table):
    ui_table.clear()
    ui_table.setColumnCount(len(labels))
    ui_table.setHorizontalHeaderLabels(labels)
    ui_table.setRowCount(len(data))
    row = -1
    col = -1
    for i in data:
        row += 1
        if i[0] == home_team:
            color = COLORS['color_home']
        elif i[0] == away_team:
            color = COLORS['color_away']
        elif row % 2:
            color = COLORS['color_1']
        else:
            color = COLORS['color_2']
        for j in i:
            col += 1
            line = QtGui.QTableWidgetItem(str(j))
            ui_table.setItem(row, col, line)
            ui_table.item(row, col).setBackground(color)
            ui_table.item(row, col).setTextAlignment(QtCore.Qt.AlignHCenter)
        col = -1
    ui_table.resizeRowsToContents()
    ui_table.resizeColumnsToContents()
    ui_table.verticalHeader().setDefaultSectionSize(20)

