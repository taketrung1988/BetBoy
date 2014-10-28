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
import sys
import os

from PySide import QtGui

from data.apps.stats_central.ui.stats_central import Ui_MainWindow
from data.apps.stats_central.services import (renders)


class StatisticsApp(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.vars = {
            'csv_file': '',
            'mode_standings': self.ui.combo_standings_mode.currentIndex,
            'mode_form': self.ui.combo_form_mode.currentIndex,
            'mode_date': self.ui.combo_scheudle_dates.currentText,
            'mode_home': self.ui.combo_home_mode.currentIndex,
            'mode_away': self.ui.combo_away_mode.currentIndex,
            'home_team': self.ui.main_combo_home.currentText,
            'away_team': self.ui.main_combo_away.currentText,
            'ann': self.ui.main_combo_nets.currentText,
            'ranges': self.ui.main_combo_ranges.currentText
        }
        self.render_csv_list('.')
        self.fill_combo_csv_paths()

    def render_standings(self,mode=0):
        """

        :param mode:
        :return:
        """
        mode = self.vars['mode_standings']()
        if mode in (0, 1, 2):
            labels = ['Team', 'Matches', 'Pts', 'GS', 'GL', 'Wins', 'Draws',
                      'Loses', 'BTS', 'over2.5', 'under2.5']
            renders.render(self.vars['home_team'](), self.vars['away_team'](),
                           data, labels, self.ui.main_table_standings)
        else:
            labels = ['Team', 'Matches', 'Pts', 'GS', 'GL', 'Wins', 'Draws',
                      'Loses', 'BTS', 'over2.5', 'under2.5']

    def render_csv_list(self, path):
        full_path = os.path.join('..', '..', 'csv', path)
        f = os.listdir(full_path)
        for i in f:
            if os.path.isfile(os.path.join(full_path, i)):
                item = QtGui.QTreeWidgetItem(self.ui.tree_csv_files)
                item.setText(0, i)

    def fill_combo_csv_paths(self):
        full_path = os.path.join('..', '..', 'csv')
        f = os.listdir(full_path)
        for i in f:
            if os.path.isdir(os.path.join(full_path, i)):
                self.ui.combo_csv_paths.addItem(i)




if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    my_app = StatisticsApp()
    my_app.show()
    sys.exit(app.exec_())
