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

import unittest
from data.sql_core import (models as m,
                           csv_loader as csv)
from data.sql_core.queries import tables as s


class Testing(unittest.TestCase):
    def setUp(self):
        s.create_tables()
        self.csv_db = csv.load_csv('test.csv')
        s.fill_tables(self.csv_db)

    def assert_team_stats(self, team, wins, draws, loses, **kwargs):
        #  TODO TeamStatsHome, TeamStatsAway
        team = m.TeamStats.\
            get(m.TeamStats.team == m.Team.get(m.Team.name == team))

        self.assertEqual(team.win, wins)
        self.assertEqual(team.draw, draws)
        self.assertEqual(team.lose, loses)
        self.assertAlmostEqual(team.margin_of_win, kwargs['mov'], delta=0.01)
        self.assertAlmostEqual(team.margin_of_lose, kwargs['mol'], delta=0.01)
        self.assertAlmostEqual(team.point, kwargs['points'], delta=0.01)
        self.assertAlmostEqual(team.point_bb, kwargs['points_bb'], delta=0.01)

    def assert_team_series(self, team=None, **kw):
        #  TODO TeamSeriesHome, TeamSeriesAway
        team = m.Series.\
            get(m.Series.team == m.Team.get(m.Team.name == team))
        self.assertEqual(team.win, kw.get('win', 0))
        self.assertEqual(team.draw, kw.get('draw', 0))
        self.assertEqual(team.lose, kw.get('lose', 0))
        self.assertEqual(team.no_lose, kw.get('no_lose', 0))
        self.assertEqual(team.no_win, kw.get('no_win', 0))
        self.assertEqual(team.no_draw, kw.get('no_draw', 0))
        self.assertEqual(team.bts, kw.get('bts', 0))
        self.assertEqual(team.no_bts, kw.get('no_bts', 0))
        self.assertEqual(team.over25, kw.get('over25', 0))
        self.assertEqual(team.no_over25, kw.get('no_over25', 0))
        self.assertEqual(team.under25, kw.get('under25', 0))
        self.assertEqual(team.no_under25, kw.get('no_under25', 0))
        self.assertEqual(team.scored_goal, kw.get('scored_goal', 0))
        self.assertEqual(team.no_scored_goal, kw.get('no_scored_goal', 0))
        self.assertEqual(team.lost_goal, kw.get('lost_goal', 0))
        self.assertEqual(team.no_lost_goal, kw.get('no_lost_goal', 0))

    def test_stats(self):
        for t in STATS:
            self.assert_team_stats(**t)
        #for i in m.TeamStats.select().order_by(m.TeamStats.points.desc()):
        #    print(i.matches, i.team.name, i.points, i.points_bb)

    def test_series(self):
        for t in SERIES:
            self.assert_team_series(**t)

STATS = [
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
     'mov': 0, 'mol': 1, 'points': 1, 'points_bb': 1.2}
]

SERIES = [
    {'team': 'E.Frankfurt', 'win': 3, 'draw': 0, 'lose': 0,
     'no_lose': 3, 'no_win': 0, 'no_draw': 3, 'bts': 1,
     'no_bts': 0, 'over25': 3, 'no_over25': 0, 'under25': 0, 'no_under25': 3,
     'scored_goal': 0, 'no_scored_goal':0, 'lost_goal': 0, 'no_lost_goal': 0},
    {'team': 'B.Munich', 'win': 3, 'draw': 0, 'lose': 0,
     'no_lose': 3, 'no_win': 0, 'no_draw': 3, 'bts': 2,
     'no_bts': 0, 'over25': 3, 'no_over25': 0, 'under25': 0, 'no_under25': 3,
     'scored_goal': 0, 'no_scored_goal':0, 'lost_goal': 0, 'no_lost_goal': 0},
    {'team': 'Nuremberg', 'win': 1, 'draw': 0, 'lose': 0,
     'no_lose': 3, 'no_win': 0, 'no_draw': 1, 'bts': 2,
     'no_bts': 0, 'over25': 1, 'no_over25': 0, 'under25': 0, 'no_under25': 1,
     'scored_goal': 0, 'no_scored_goal':0, 'lost_goal': 0, 'no_lost_goal': 0},
    {'team': 'Hannover', 'win': 2, 'draw': 0, 'lose': 0,
     'no_lose': 3, 'no_win': 0, 'no_draw': 2, 'bts': 1,
     'no_bts': 0, 'over25': 3, 'no_over25': 0, 'under25': 0, 'no_under25': 3,
     'scored_goal': 0, 'no_scored_goal':0, 'lost_goal': 0, 'no_lost_goal': 0},
    {'team': 'Dortmund', 'win': 1, 'draw': 0, 'lose': 0,
     'no_lose': 3, 'no_win': 0, 'no_draw': 1, 'bts': 0,
     'no_bts': 1, 'over25': 1, 'no_over25': 0, 'under25': 0, 'no_under25': 1,
     'scored_goal': 0, 'no_scored_goal': 0, 'lost_goal': 0, 'no_lost_goal': 0},
    {'team': 'Schalke04', 'win': 2, 'draw': 0, 'lose': 0,
     'no_lose': 3, 'no_win': 0, 'no_draw': 2, 'bts': 0,
     'no_bts': 1, 'over25': 0, 'no_over25': 1, 'under25': 1, 'no_under25': 0,
     'scored_goal': 0, 'no_scored_goal': 0, 'lost_goal': 0, 'no_lost_goal': 0},
    {'team': 'Freiburg', 'win': 1, 'draw': 0, 'lose': 0,
     'no_lose': 1, 'no_win': 0, 'no_draw': 2, 'bts': 1,
     'no_bts': 0, 'over25': 1, 'no_over25': 0, 'under25': 0, 'no_under25': 1,
     'scored_goal': 0, 'no_scored_goal': 0, 'lost_goal': 0, 'no_lost_goal': 0},
    {'team': 'Furth', 'win': 0, 'draw': 0, 'lose': 1,
     'no_lose': 0, 'no_win': 1, 'no_draw': 3, 'bts': 0,
     'no_bts': 3, 'over25': 0, 'no_over25': 2, 'under25': 2, 'no_under25': 0,
     'scored_goal': 0, 'no_scored_goal': 0, 'lost_goal': 0, 'no_lost_goal': 0},
    {'team': 'Wolfsburg', 'win': 0, 'draw': 1, 'lose': 0,
     'no_lose': 1, 'no_win': 2, 'no_draw': 0, 'bts': 0,
     'no_bts': 3, 'over25': 0, 'no_over25': 1, 'under25': 1, 'no_under25': 0,
     'scored_goal': 0, 'no_scored_goal': 0, 'lost_goal': 0, 'no_lost_goal': 0},
    {'team': 'Mgladbach', 'win': 0, 'draw': 0, 'lose': 1,
     'no_lose': 0, 'no_win': 2, 'no_draw': 1, 'bts': 1,
     'no_bts': 0, 'over25': 1, 'no_over25': 0, 'under25': 0, 'no_under25': 1,
     'scored_goal': 0, 'no_scored_goal': 0, 'lost_goal': 0, 'no_lost_goal': 0},
    {'team': 'Dusseldorf', 'win': 0, 'draw': 2, 'lose': 0,
     'no_lose': 3, 'no_win': 2, 'no_draw': 0, 'bts': 0,
     'no_bts': 3, 'over25': 0, 'no_over25': 3, 'under25': 3, 'no_under25': 0,
     'scored_goal': 0, 'no_scored_goal': 0, 'lost_goal': 0, 'no_lost_goal': 0},
    {'team': 'Hoffenheim', 'win': 0, 'draw': 0, 'lose': 3,
     'no_lose': 0, 'no_win': 3, 'no_draw': 3, 'bts': 1,
     'no_bts': 0, 'over25': 3, 'no_over25': 0, 'under25': 0, 'no_under25': 3,
     'scored_goal': 0, 'no_scored_goal': 0, 'lost_goal': 0, 'no_lost_goal': 0},
    {'team': 'Stuttgart', 'win': 0, 'draw': 1, 'lose': 0,
     'no_lose': 1, 'no_win': 3, 'no_draw': 0, 'bts': 0,
     'no_bts': 1, 'over25': 0, 'no_over25': 1, 'under25': 1, 'no_under25': 0,
     'scored_goal': 0, 'no_scored_goal': 0, 'lost_goal': 0, 'no_lost_goal': 0},
    {'team': 'Augsburg', 'win': 0, 'draw': 1, 'lose': 0,
     'no_lose': 1, 'no_win': 3, 'no_draw': 0, 'bts': 0,
     'no_bts': 1, 'over25': 0, 'no_over25': 1, 'under25': 1, 'no_under25': 0,
     'scored_goal': 0, 'no_scored_goal': 0, 'lost_goal': 0, 'no_lost_goal': 0},
    {'team': 'Hamburg', 'win': 0, 'draw': 0, 'lose': 3,
     'no_lose': 0, 'no_win': 3, 'no_draw': 3, 'bts': 1,
     'no_bts': 0, 'over25': 1, 'no_over25': 0, 'under25': 0, 'no_under25': 1,
     'scored_goal': 0, 'no_scored_goal': 0, 'lost_goal': 0, 'no_lost_goal': 0},
    {'team': 'Mainz05', 'win': 0, 'draw': 0, 'lose': 2,
     'no_lose': 0, 'no_win': 3, 'no_draw': 2, 'bts': 1,
     'no_bts': 0, 'over25': 1, 'no_over25': 0, 'under25': 0, 'no_under25': 1,
     'scored_goal': 0, 'no_scored_goal': 0, 'lost_goal': 0, 'no_lost_goal': 0},

]






