# -*- coding: utf-8 -*-
"""
Copyright 2014 Jacek Markowski, jacek87markowski@gmail.com

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
from __future__ import print_function
import csv
from data.sql.services import (check_line, check_winner, clear_tables,
                               remove_duplicates_from_results,
                               table_creator, updater_team)
from data.sql.sql_queries import get_matches
from data.helpers import print_traceback
import data.sql.table_schemes as t
from data.sql.rating import new_rating
BASIC_H = ('team_basic', 'team_basic_home')
BASIC_A = ('team_basic', 'team_basic_away')
FORM_H = ('team_form', 'team_form_home')
FORM_A = ('team_form', 'team_form_away')
FORM_BB_H = ('team_form_bb', 'team_form_bb_home')
FORM_BB_A = ('team_form_bb', 'team_form_bb_away')
SERIES_H = ('team_series', 'team_series_home')
SERIES_A = ('team_series', 'team_series_away')
ADVANCED = ('team_advanced', 'team_advanced_home', 'team_advanced_away')
ADVANCED_H = ('team_advanced', 'team_advanced_home')
ADVANCED_A = ('team_advanced', 'team_advanced_away')


def initialize_tables(cursor):
    """Create tables

    :rtype : int
    :param cursor: sqlite cursor
    :return: 1-success, 0-fail
    """
    basic_names = 'team_basic'
    adv_names = 'team_advanced'
    series_names = 'team_series'
    form_names = 'team_form'
    form_bb_names = 'team_form_bb'

    try:
        cursor.execute('CREATE TABLE results' + t.RESULTS)
        cursor.execute('CREATE TABLE odds' + t.ODDS)
        cursor.execute('CREATE TABLE odds_scaled' + t.ODDS_SCALED)
        table_creator(cursor, basic_names, t.TEAM_BASIC)
        table_creator(cursor, adv_names, t.TEAM_ADVANCED)
        table_creator(cursor, series_names, t.TEAM_SERIES)
        table_creator(cursor, form_names, t.TEAM_FORM)
        table_creator(cursor, form_bb_names, t.TEAM_FORM)
        table_creator(cursor, basic_names, t.TEAM_BASIC, 1)
        table_creator(cursor, adv_names, t.TEAM_ADVANCED, 1)
        table_creator(cursor, series_names, t.TEAM_SERIES, 1)
        table_creator(cursor, form_names, t.TEAM_FORM, 1)
        table_creator(cursor, form_bb_names, t.TEAM_FORM, 1)
    except:
        print_traceback()
        return 0
    return 1


def load_csv(cursor, path):
    """
    :param cursor: sql cursor
    :param path: path to csv file
    :return: 1-success 0-fail
    """
    clear_tables(cursor)
    with open(path, 'r') as f:
        csv_list = list(csv.reader(f))
    csv_list.pop(0)
    for i in csv_list:
        new_line = check_line(i)
        if new_line:
            update_results(cursor, new_line)
        elif not isinstance(new_line, list):
            print('Invalid line in csv file\nfile: {0}\n'
                  'line number: {1}\n'
                  'line: {2}'.format(path, csv_list.index(i), i))
            return 0
    return 1


def update_results(cursor, line):
    """Insert match into the results table.

    :type line: []
    :param line: one match result(from check_line)
    :param cursor: sql cursor
    :return: 1-success 0-fail
    """
    try:
        (date, home, away, g_home, g_away, odds_1, odds_x, odds_2) = line[0:8]
        cursor.execute('''INSERT INTO results(
        date,
        team_home,
        team_away,
        g_home_end,
        g_away_end,
        odds_1,
        odds_x,
        odds_2)
        VALUES({0},"{1}","{2}",
               {3},{4},{5},
               {6},{7})'''.format(date, home, away, g_home, g_away,
                                  odds_1, odds_x, odds_2))
        remove_duplicates_from_results(cursor)
    except:
        print_traceback()
        return 0
    return 1

def update_tables(cursor, result):
        """Update team statistics in tables.
        :type result: []
        :param result: match result
        """
        # order matters
        update_tables.update_team_basic_all(cursor, result)
        update_tables.update_team_form_all(cursor, result)
        update_tables.update_team_series_all(cursor, result)
        update_tables.update_team_advanced_all(cursor, result)


def update_team_basic_all(cursor, result):
    """Update basic statistics(overall,home,away) for teams.

    :param cursor: sql cursor
    :type result:['home','away',int,int]
    :param result: match results
    """
    team_home, team_away, goals_home, goals_away = result
    winner = check_winner(goals_home, goals_away)

    # goals team_home
    fields = 'goals_scored=goals_scored +{0},' \
             'goals_lost=goals_lost+{0}'.format(goals_home, goals_away)
    updater_team(cursor, BASIC_H, fields, team_home)
    # goals team_away
    fields = 'goals_scored=goals_scored +{0},' \
             'goals_lost=goals_lost+{0}'.format(goals_away, goals_home)
    updater_team(cursor, BASIC_A, fields, team_away)

    fields_win = 'wins=wins+1,' \
                 'points=points+3' \
                 'matches=matches+1'
    fields_lose = 'loses=loses+1,' \
                  'matches=matches+1'
    fields_draw = 'draws=draws+1,' \
                  'points=points+1,' \
                  'matches=matches+1'
    if winner == 1:
        updater_team(cursor, BASIC_H, fields_win, team_home)
        updater_team(cursor, BASIC_A, fields_lose, team_away)
    elif winner == 0:
        updater_team(cursor, BASIC_H, fields_draw, team_home)
        updater_team(cursor, BASIC_A, fields_draw, team_away)
    elif winner == 2:
        updater_team(cursor, BASIC_H, fields_lose, team_home)
        updater_team(cursor, BASIC_A, fields_win, team_away)


def update_team_form_all(cursor, result):
    """

    :param cursor: sql cursor
    :type result:['home','away',int,int]
    :param result: match results
    """
    team_home, team_away, goals_home, goals_away = result
    winner = check_winner(goals_home, goals_away)
    fields = 'f4=f3,' \
             'f3=f2,' \
             'f2=f1,' \
             'f1={0}'

    if winner == 1:
        updater_team(cursor, FORM_H, fields.format(3), team_home)
        updater_team(cursor, FORM_A, fields.format(0), team_away)
    elif winner == 0:
        updater_team(cursor, FORM_H, fields.format(1), team_home)
        updater_team(cursor, FORM_A, fields.format(1), team_away)
    elif winner == 2:
        updater_team(cursor, FORM_H, fields.format(0), team_home)
        updater_team(cursor, FORM_A, fields.format(3), team_away)


def update_team_form_bb_all(cursor, team_home, team_away, p_home, p_away):
    """Update form_bb for given teams.

    :param cursor: sql cursor
    :param team_home: string
    :param team_away: string
    :param p_home: float - points earned by team_home in match
    :param p_away: float - points earned by team_away in match
    """
    fields = 'f4=f3,' \
             'f3=f2,' \
             'f2=f1,' \
             'f1={0}'
    updater_team(cursor, FORM_BB_H, fields.format(p_home), team_home)
    updater_team(cursor, FORM_BB_A, fields.format(p_away), team_away)


def update_team_series_all(cursor, result):
    """

    :param cursor: sql cursor
    :type result:['home','away',int,int]
    :param result: match results
    """
    team_home, team_away, goals_home, goals_away = result
    winner = check_winner(goals_home, goals_away)
    fields_win = 'wins = wins + 1, loses = 0, draws = 0' \
                 'no_wins = 0, no_draws = no_draws + 1' \
                 'no_loses = no_loses + 1'
    fields_lose = 'wins = 0, loses = loses + 1, draws = 0' \
                  'no_wins = no_wins + 1, no_draws = no_draws + 1' \
                  'no_loses = 0'
    fields_draw = 'wins = 0, loses = 0, draws = draws + 1' \
                  'no_wins = no_wins + 1, no_draws = 0' \
                  'no_loses = no_loses + 1'
    if winner == 1:
        updater_team(cursor, SERIES_H, fields_win, team_home)
        updater_team(cursor, SERIES_A, fields_lose, team_away)
    elif winner == 0:
        updater_team(cursor, SERIES_H, fields_draw, team_home)
        updater_team(cursor, SERIES_A, fields_draw, team_away)
    elif winner == 2:
        updater_team(cursor, SERIES_H, fields_lose, team_home)
        updater_team(cursor, SERIES_A, fields_win, team_away)
    # BTS
    bts = (goals_home > 0) and (goals_away > 0)
    bts_true = 'bts = bts + 1,' \
               'no_bts = 0'
    bts_false = 'bts = 0,' \
                'no_bts = no_bts + 1'
    if bts:
        updater_team(cursor, SERIES_H, bts_true, team_home)
        updater_team(cursor, SERIES_A, bts_true, team_away)
    else:
        updater_team(cursor, SERIES_H, bts_false, team_home)
        updater_team(cursor, SERIES_A, bts_false, team_away)
    # over/under
    over = (goals_away + goals_home) > 2.5
    over_true = 'over25 = over25 + 1,' \
                'no_over25 = 0,' \
                'under_25 = 0,' \
                'no_under25 = no_under25 + 1'
    over_false = 'over25 = 0,' \
                 'no_over25 = no_over25 + 1,' \
                 'under_25 = under25 + 1,' \
                 'no_under25 = 0'
    if over:
        updater_team(cursor, SERIES_H, over_true, team_home)
        updater_team(cursor, SERIES_A, over_true, team_away)
    else:
        updater_team(cursor, SERIES_H, over_false, team_home)
        updater_team(cursor, SERIES_A, over_false, team_away)


def update_team_advanced_all(cursor, result):
    """

    :param cursor: sql cursor1
    :type result:['home','away',int,int]
    :param result: match results
    """
    # points
    team_home, team_away, goals_home, goals_away = result
    outcome = check_winner(goals_home, goals_away)
    g_diff = abs(goals_home - goals_away)
    over = (goals_home + goals_away) > 2.5
    bts = goals_home > 0 and goals_away > 0
    matches_t1 = get_matches(cursor, team_home)
    matches_t2 = get_matches(cursor, team_away)
    (ph, pa) = new_rating(cursor, team_home, team_away, outcome)
    fields_points_h = 'points={0}'.format(ph)
    fields_points_a = 'points={0}'.format(pa)
    fields_diff_loss = \
        'goal_difference_wins=goal_difference_wins+{0}'.format(g_diff)
    fields_diff_win = \
        'goal_difference_loses=goal_difference_loses+{0}'.format(g_diff)
    mov_mol = 'SET margin_of_wins = goal_difference_wins/{0},' \
              'margin_of_loses = goal_difference_loses/{0}'
    fields_mov_mol_t1 = mov_mol.format(matches_t1)
    fields_mov_mol_t2 = mov_mol.format(matches_t2)
    fields_over = 'over25 = over25 + 1'
    fields_under = 'under25 = under25 + 1'
    fields_bts = 'bts = bts + 1'
    # Points
    updater_team(cursor, ADVANCED_H, fields_points_h, team_home)
    updater_team(cursor, ADVANCED_A, fields_points_a, team_away)
    # Mov, Mol
    if outcome == 1:
        updater_team(cursor, ADVANCED_H, fields_diff_win, team_home)
        updater_team(cursor, ADVANCED_H, fields_mov_mol_t1, team_home)
        updater_team(cursor, ADVANCED_A, fields_diff_loss, team_away)
        updater_team(cursor, ADVANCED_A, fields_mov_mol_t2, team_away)
    if outcome == 2:
        updater_team(cursor, ADVANCED_H, fields_diff_loss, team_home)
        updater_team(cursor, ADVANCED_H, fields_mov_mol_t1, team_home)
        updater_team(cursor, ADVANCED_A, fields_diff_win, team_away)
        updater_team(cursor, ADVANCED_A, fields_mov_mol_t2, team_away)
    # under/over 2.5
    if over:
        updater_team(cursor, ADVANCED_H, fields_over, team_home)
        updater_team(cursor, ADVANCED_A, fields_over, team_away)
    else:
        updater_team(cursor, ADVANCED_H, fields_under, team_home)
        updater_team(cursor, ADVANCED_A, fields_under, team_away)
    # bts
    if bts:
        updater_team(cursor, ADVANCED_H, fields_bts, team_home)
        updater_team(cursor, ADVANCED_A, fields_bts, team_away)
