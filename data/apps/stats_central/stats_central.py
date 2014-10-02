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


class StatisticsApp(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)
        #main tab variables
        self.gui.tree_picks.headerItem().setText(0, ('League'))
        self.gui.tree_picks.setColumnWidth(0,110)
        self.gui.tree_picks.headerItem().setText(1, ('Home'))
        self.gui.tree_picks.setColumnWidth(1,100)
        self.gui.tree_picks.headerItem().setText(2, ('Away'))
        self.gui.tree_picks.setColumnWidth(2,100)
        self.gui.tree_picks.headerItem().setText(3, ('Bet'))
        self.gui.tree_picks.setColumnWidth(3,15)
        self.gui.tree_picks.headerItem().setText(4, ('Net'))
        self.gui.tree_picks.setColumnWidth(4,50)
        self.gui.tree_picks.headerItem().setText(5, ('Value'))
        self.gui.tree_picks.setColumnWidth(5,50)
        self.gui.tree_picks.headerItem().setText(6, ('1'))
        self.gui.tree_picks.setColumnWidth(6,30)
        self.gui.tree_picks.headerItem().setText(7, ('x'))
        self.gui.tree_picks.setColumnWidth(7,30)
        self.gui.tree_picks.headerItem().setText(8, ('2'))
        self.gui.tree_picks.setColumnWidth(8,30)
        self.gui.tree_picks.headerItem().setText(9, ('1x'))
        self.gui.tree_picks.setColumnWidth(9,30)
        self.gui.tree_picks.headerItem().setText(10, ('x2'))
        self.gui.tree_picks.setColumnWidth(10,30)
        self.gui.tree_picks.headerItem().setText(11, ('Comments'))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    my_app = StatisticsApp()
    my_app.show()
    sys.exit(app.exec_())
