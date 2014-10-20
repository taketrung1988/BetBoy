#!/usr/bin/env python
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

from __future__ import print_function
import unittest
from data.sql_core import (queries as s,
                           models as m,
                           csv_loader as csv)


class Testing(unittest.TestCase):
    def setUp(self):
        s.create_tables()
        self.csv_db = csv.load_csv('test.csv')

    def assert_team_basic(self, team_name, wins, draws, loses):
        team = m.TeamStats.\
            get(m.TeamStats.team == m.Team.get(m.Team.name == team_name))
        self.assertEqual(team.wins, wins)
        self.assertEqual(team.draws, draws)
        self.assertEqual(team.loses, loses)

    def test_stats(self):
        db = self.csv_db
        s.fill_tables(db)
        teams = [
            {'team': 'E.Frankfurt', 'wins': 3, 'draws': 0, 'loses': 0},
            {'team': 'B.Munich', 'wins': 3, 'draws': 0, 'loses': 0},
            {'team': 'Nuremberg', 'wins': 2, 'draws': 1, 'loses': 0},
            {'team': 'Hannover', 'wins': 2, 'draws': 1, 'loses': 0},
            {'team': 'Dortmund', 'wins': 2, 'draws': 1, 'loses': 0},
            {'team': 'Schalke04', 'wins': 2, 'draws': 1, 'loses': 0},
            {'team': 'Freiburg', 'wins': 1, 'draws': 1, 'loses': 1},
            {'team': 'Leverkusen', 'wins': 1, 'draws': 0, 'loses': 2},
            {'team': 'Furth', 'wins': 1, 'draws': 0, 'loses': 2},
            {'team': 'Wolfsburg', 'wins': 1, 'draws': 1, 'loses': 1},
            {'team': 'Mgladbach', 'wins': 1, 'draws': 1, 'loses': 1},
            {'team': 'Dusseldorf', 'wins': 1, 'draws': 2, 'loses': 0},
            {'team': 'Hoffenheim', 'wins': 0, 'draws': 0, 'loses': 3},
            {'team': 'Stuttgart', 'wins': 0, 'draws': 1, 'loses': 2},
            {'team': 'Augsburg', 'wins': 0, 'draws': 1, 'loses': 2},
            {'team': 'Hamburg', 'wins': 0, 'draws': 0, 'loses': 3},
            {'team': 'Mainz05', 'wins': 0, 'draws': 1, 'loses': 2}
        ]
        for t in teams:
            self.assert_team_basic(t['team'], t['wins'], t['draws'], t['loses'])

        #for i in m.TeamStats.select().order_by(m.TeamStats.wins.desc()):
        #    print(i.team.name, i.wins, i.draws, i.loses)





