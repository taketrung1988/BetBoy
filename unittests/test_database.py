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
from data.sql_core import (models as m,
                           csv_loader as csv)
from data.sql_core.queries import tables as s

TABLE = [
    {'team': 'E.Frankfurt', 'wins': 3, 'draws': 0, 'loses': 0,
     'mov': 2.0, 'mol': 0, 'points': 9, 'points_bb': 8.3},
    {'team': 'B.Munich', 'wins': 3, 'draws': 0, 'loses': 0,
     'mov': 3.33, 'mol': 0, 'points': 9, 'points_bb': 8.7},
    {'team': 'Nuremberg', 'wins': 2, 'draws': 1, 'loses': 0,
     'mov': 0.66, 'mol': 0, 'points': 7, 'points_bb': 6.4},
    {'team': 'Hannover', 'wins': 2, 'draws': 1, 'loses': 0,
     'mov': 1.66, 'mol': 0, 'points': 7, 'points_bb': 6.6},
    {'team': 'Dortmund', 'wins': 2, 'draws': 1, 'loses': 0,
     'mov': 1.33, 'mol': 0, 'points': 7, 'points_bb': 6.6},
    {'team': 'Schalke04', 'wins': 2, 'draws': 1, 'loses': 0,
     'mov': 1.33, 'mol': 0, 'points': 7, 'points_bb': 6.8},
    {'team': 'Freiburg', 'wins': 1, 'draws': 1, 'loses': 1,
     'mov': 0.66, 'mol': 0.66, 'points': 4, 'points_bb': 3.9},
    {'team': 'Leverkusen', 'wins': 1, 'draws': 0, 'loses': 2,
     'mov': 0.66, 'mol': 1.33, 'points': 3, 'points_bb': 3.1},
    {'team': 'Furth', 'wins': 1, 'draws': 0, 'loses': 2,
     'mov': 0.33, 'mol': 1.66, 'points': 3, 'points_bb': 2.7},
    {'team': 'Wolfsburg', 'wins': 1, 'draws': 1, 'loses': 1,
     'mov': 0.33, 'mol': 1.33, 'points': 4, 'points_bb': 3.9},
    {'team': 'Mgladbach', 'wins': 1, 'draws': 1, 'loses': 1,
     'mov': 0.33, 'mol': 0.33, 'points': 4, 'points_bb': 4.1},
    {'team': 'Dusseldorf', 'wins': 1, 'draws': 2, 'loses': 0,
     'mov': 0.66, 'mol': 0, 'points': 5, 'points_bb': 5.3},
    {'team': 'Hoffenheim', 'wins': 0, 'draws': 0, 'loses': 3,
     'mov': 0, 'mol': 2.33, 'points': 0, 'points_bb': 0.2},
    {'team': 'Stuttgart', 'wins': 0, 'draws': 1, 'loses': 2,
     'mov': 0, 'mol': 2, 'points': 1, 'points_bb': 1.4},
    {'team': 'Augsburg', 'wins': 0, 'draws': 1, 'loses': 2,
     'mov': 0, 'mol': 1.33, 'points': 1, 'points_bb': 1.2},
    {'team': 'Hamburg', 'wins': 0, 'draws': 0, 'loses': 3,
     'mov': 0, 'mol': 1.33, 'points': 0, 'points_bb': 0.4},
    {'team': 'Mainz05', 'wins': 0, 'draws': 1, 'loses': 2,
     'mov': 0, 'mol': 1, 'points': 1, 'points_bb': 1.2}]


class Testing(unittest.TestCase):
    def setUp(self):
        s.create_tables()
        self.csv_db = csv.load_csv('test.csv')

    def assert_team_basic(self, team, wins, draws, loses, **kwargs):
        team = m.TeamStats.\
            get(m.TeamStats.team == m.Team.get(m.Team.name == team))
        self.assertEqual(team.wins, wins)
        self.assertEqual(team.draws, draws)
        self.assertEqual(team.loses, loses)
        self.assertAlmostEqual(team.margin_of_wins, kwargs['mov'], delta=0.01)
        self.assertAlmostEqual(team.margin_of_loses, kwargs['mol'], delta=0.01)
        self.assertAlmostEqual(team.points, kwargs['points'], 2)
        self.assertAlmostEqual(team.points_bb, kwargs['points_bb'], 2)

    def test_stats(self):
        db = self.csv_db
        s.fill_tables(db)
        for t in TABLE:
            self.assert_team_basic(**t)
        #for i in m.TeamStats.select().order_by(m.TeamStats.points.desc()):
        #    print(i.matches, i.team.name, i.points, i.points_bb)





