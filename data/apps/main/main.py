#!/usr/bin/env python
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

from data.apps.main.ui.main import Ui_BetTools
from data.apps.about.about import AboutApp
from data.apps.stats_central.stats_central import StatisticsApp


class BBApp(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_BetTools()
        self.ui.setupUi(self)
        ### Set style
        with open(os.path.join('data', 'static', 'styles', 'dark.css'), 'r') \
            as style:
            self.setStyleSheet(style.read())
        self.win_about()
        self.bindings()

    def bindings(self):
        self.ui.actionStats_central.triggered.connect(self.win_stats_central)
        self.ui.actionAbout.triggered.connect(self.win_about)

    def win_about(self):
        about_app = AboutApp()
        about = self.ui.mdiArea.addSubWindow(about_app)
        about.showMaximized()

    def win_stats_central(self):
        stats_app = StatisticsApp()
        stats = self.ui.mdiArea.addSubWindow(stats_app)
        stats.showMaximized()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    my_app = BBApp()
    my_app.showMaximized()
    sys.exit(app.exec_())


