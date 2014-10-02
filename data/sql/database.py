# -*- coding: utf-8 -*-

# Copyright 2014 Jacek Markowski, jacek87markowski@gmail.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sqlite3
import update_tables


class Database(object):

    def __init__(self, path):
        con = sqlite3.connect(':memory:')
        self.cursor = con.cursor()
        update_tables.initialize_tables(self.cursor)
        update_tables.load_csv(self.cursor, path)

    def normal(self):
        pass

    def simulation(self):
        pass

    def export(self):
        pass





