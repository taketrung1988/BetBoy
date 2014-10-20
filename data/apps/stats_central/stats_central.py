#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright 2013 Jacek Markowski, jacek87markowski@gmail.com

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import sys

from PySide import QtGui

from data.apps.stats_central.ui.stats_central import Ui_MainWindow
from data.apps.stats_central.services import (renders)


class StatisticsApp(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)
        self.vars = {
            'csv_file': '',
            'mode_standings': self.gui.combo_standings_mode.currentIndex,
            'mode_form': self.gui.combo_form_mode.currentIndex,
            'mode_date': self.gui.combo_scheudle_dates.currentText,
            'mode_home': self.gui.combo_home_mode.currentIndex,
            'mode_away': self.gui.combo_away_mode.currentIndex,
            'home_team': self.gui.main_combo_home.currentText,
            'away_team': self.gui.main_combo_away.currentText,
            'ann': self.gui.main_combo_nets.currentText,
            'ranges': self.gui.main_combo_ranges.currentText
        }
        self.gui.tree_picks.headerItem().setText(0, 'League')
        self.gui.tree_picks.setColumnWidth(0,110)
        self.gui.tree_picks.headerItem().setText(1, 'Home')
        self.gui.tree_picks.setColumnWidth(1,100)
        self.gui.tree_picks.headerItem().setText(2, 'Away')
        self.gui.tree_picks.setColumnWidth(2,100)
        self.gui.tree_picks.headerItem().setText(3, 'Bet')
        self.gui.tree_picks.setColumnWidth(3,15)
        self.gui.tree_picks.headerItem().setText(4, 'Net')
        self.gui.tree_picks.setColumnWidth(4,50)
        self.gui.tree_picks.headerItem().setText(5, 'Value')
        self.gui.tree_picks.setColumnWidth(5,50)
        self.gui.tree_picks.headerItem().setText(6, '1')
        self.gui.tree_picks.setColumnWidth(6,30)
        self.gui.tree_picks.headerItem().setText(7, 'x')
        self.gui.tree_picks.setColumnWidth(7,30)
        self.gui.tree_picks.headerItem().setText(8, '2')
        self.gui.tree_picks.setColumnWidth(8,30)
        self.gui.tree_picks.headerItem().setText(9, '1x')
        self.gui.tree_picks.setColumnWidth(9,30)
        self.gui.tree_picks.headerItem().setText(10, 'x2')
        self.gui.tree_picks.setColumnWidth(10,30)
        self.gui.tree_picks.headerItem().setText(11, 'Comments')


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
                           data, labels, self.gui.main_table_standings)
        else:
            labels = ['Team', 'Matches', 'Pts', 'GS', 'GL', 'Wins', 'Draws',
                      'Loses', 'BTS', 'over2.5', 'under2.5']






if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    my_app = StatisticsApp()
    my_app.show()
    sys.exit(app.exec_())
