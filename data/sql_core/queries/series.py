# -*- coding: utf-8 -*-
"""
 The MIT License (MIT)

Copyright (c) 2014, Jacek Markowski

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
from data.sql_core.models import (Series, SeriesHome, SeriesAway)


def update_team_series_draw(home_dict, away_dict):
    home_dict.update(draw=1, no_lose=1, no_win=1)
    away_dict.update(draw=1, no_lose=1, no_win=1)
    up_team_series_all(home_dict, away_dict)


def update_team_series_win_home(home_dict, away_dict):
    home_dict.update(win=1, no_lose=1, no_draw=1,)
    away_dict.update(lose=1, no_win=1, no_draw=1)
    up_team_series_all(home_dict, away_dict)


def update_team_series_win_away(home_dict, away_dict):
    home_dict.update(lose=1, no_win=1, no_draw=1)
    away_dict.update(win=1, no_lose=1, no_draw=1)
    up_team_series_all(home_dict, away_dict)


def up_team_series_all(home_dict, away_dict):
    update_series(table=Series, **away_dict)
    update_series(table=SeriesAway, **away_dict)
    update_series(table=Series, **home_dict)
    update_series(table=SeriesHome, **home_dict)


def update_series(table=None, **kw):
    table.\
        update(win=new_value(table.win, kw.get('win', 0)),
               draw=new_value(table.draw, kw.get('draw', 0)),
               lose=new_value(table.lose, kw.get('lose', 0)),
               no_lose=new_value(table.no_lose, kw.get('no_lose', 0)),
               no_win=new_value(table.no_win, kw.get('no_win', 0)),
               no_draw=new_value(table.no_draw, kw.get('no_draw', 0)),
               bts=new_value(table.bts, kw.get('bts', 0)),
               no_bts=new_value(table.no_bts, kw.get('no_bts', 0)),
               over25=new_value(table.over25, kw.get('over25', 0)),
               no_over25=new_value(table.no_over25, kw.get('no_over25', 0)),
               under25=new_value(table.under25, kw.get('under25', 0)),
               no_under25=new_value(table.no_under25, kw.get('no_under25', 0)),
               ).\
        where(table.team == kw['team']).execute()


def new_value(current, new):
    return (current+new) if new else 0
