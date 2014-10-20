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

from data.third_party.peewee.playhouse import csv_loader
from data.third_party.peewee.peewee import (SqliteDatabase, TextField,
                                            FloatField, IntegerField,
                                            DateField)

db = SqliteDatabase(':memory:')


def load_csv(path):
    fields = [DateField(), TextField(), TextField(), IntegerField(),
              IntegerField(), FloatField(), FloatField(), FloatField()]
    field_names = ['date', 'team_home', 'team_away', 'g_home', 'g_away',
                   'odds_home', 'odds_draw', 'odds_away']
    csv_db = csv_loader.load_csv(db, path, db_table='CSV', fields=fields,
                                 field_names=field_names)
    return csv_db






