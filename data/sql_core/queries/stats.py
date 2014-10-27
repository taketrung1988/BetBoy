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
from data.sql_core.models import (TeamStats, TeamStatsHome, TeamStatsAway)


def update_team_stats_draw(home_dict, away_dict):
    home_dict.update(draw=1,
                     point=1,
                     point_bb=1)
    away_dict.update(draw=1,
                     point=1,
                     point_bb=1)
    up_team_stats_all(home_dict, away_dict)


def update_team_stats_win_home(home_dict, away_dict):
    home_dict.update(win=1,
                     point=3,
                     point_bb=3)
    away_dict.update(lose=1)
    up_team_stats_all(home_dict, away_dict)


def update_team_stats_win_away(home_dict, away_dict):
    home_dict.update(lose=1)
    away_dict.update(win=1,
                     point=3,
                     point_bb=3)
    up_team_stats_all(home_dict, away_dict)


def up_team_stats_all(home_dict, away_dict):
    update_stats(table=TeamStats, **away_dict)
    update_stats(table=TeamStatsAway, **away_dict)
    update_stats(table=TeamStats, **home_dict)
    update_stats(table=TeamStatsHome, **home_dict)


def update_stats(table=None, **kw):
    table.\
        update(match=table.match + 1,
               win=table.win + kw.get('win', 0),
               draw=table.draw + kw.get('draw', 0),
               lose=table.lose + kw.get('lose', 0),
               goal_scored=table.goal_scored + kw.get('g_scored', 0),
               goal_lost=table.goal_lost + kw.get('g_lost', 0),
               point=table.point + kw.get('point', 0),
               point_bb=table.point_bb + points_bb(kw),
               goal_diff_win=g_diff_wins(kw['team'], table, kw),
               goal_diff_lose=g_diff_loses(kw['team'], table, kw),
               bts=table.bts + kw.get('bts', 0),
               over25=table.over25 + kw.get('over25', 0),
               under25=table.over25 + kw.get('under25', 0),
               ).\
        where(table.team == kw['team']).execute()

    table.\
        update(margin_of_win=mow(kw['team'], table),
               margin_of_lose=mol(kw['team'], table),
               ).\
        where(table.team == kw['team']).execute()


def mow(team_obj=None, table=None):
    query = table.get(table.team == team_obj)
    try:
        new_mow = query.goal_diff_win / float(query.match)
    except ZeroDivisionError:
        new_mow = 0
    return new_mow


def mol(team_obj=None, table=None):
    query = table.get(table.team == team_obj)
    try:
        new_mol = query.goal_diff_lose / float(query.match)
    except ZeroDivisionError:
        new_mol = 0
    return new_mol


def g_diff_wins(team_obj, table, stats_dict):
    g_scored = stats_dict['g_scored']
    g_lost = stats_dict['g_lost']
    query = table.get(table.team == team_obj)
    try:
        if g_scored > g_lost:
            new_mow = query.goal_diff_win + abs(g_scored - g_lost)
        else:
            new_mow = query.goal_diff_win
    except ZeroDivisionError:
        new_mow = query.goal_diff_wins
    return new_mow


def g_diff_loses(team_obj, table, stats_dict):
    g_scored = stats_dict['g_scored']
    g_lost = stats_dict['g_lost']
    query = table.get(table.team == team_obj)
    try:
        if g_scored < g_lost:
            new_mol = query.goal_diff_lose + abs(g_scored - g_lost)
        else:
            new_mol = query.goal_diff_lose
    except ZeroDivisionError:
        new_mol = query.goal_diff_loses
    return new_mol


def points_bb(stats_dict):
    bonus = 0
    bonus_draw = stats_dict['g_lost'] == 0
    bonus_win = abs(stats_dict['g_scored'] - stats_dict['g_lost']) >= 2
    bonus_loss = abs(stats_dict['g_scored'] - stats_dict['g_lost']) == 1
    draw = stats_dict['g_scored'] == stats_dict['g_lost']
    win = stats_dict['g_scored'] > stats_dict['g_lost']

    if draw:
        if bonus_draw:
            bonus = 0.2
        points = 1 + bonus
    elif win:
        if bonus_win:
            bonus = 0.2
        points = 2.7 + bonus
    elif not win:
        if bonus_loss:
            bonus = 0.2
        points = 0 + bonus
    return points


def check_result(g_home, g_away):
    if g_home == -1 or g_away == -1:
        result = -1
    elif g_home == g_away:
        result = 0
    elif g_home > g_away:
        result = 1
    elif g_home < g_away:
        result = 2
    else:
        result = -1
    return result