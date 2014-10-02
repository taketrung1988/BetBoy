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

from __future__ import print_function
import calendar
import datetime
from data.helpers import print_traceback


def selector_team(cursor, table, fields, team):
    """

    :param cursor: sql cursor
    :param table: string - one table
    :param fields: string
    :param team: string team name
    :return selected: string || value
    """
    selected = cursor.execute(
        '''SELECT {0}
        FROM {1}
        WHERE team={2}'''.format(fields, table, team)
    ).fetchone()[0][0]
    return selected

def table_creator(cursor, name, template, scale=0):
    """
    :param scale: 0-normal , 1-add 'scaled' to table name
    :param cursor: sql cursor
    :param name: String
    :param template: String
    """
    table_names = [name, name + '_home', name + '_away']
    if scale:
        table_names = map(lambda x: x + '_scaled', table_names)
    for name in table_names:
        cursor.execute('CREATE TABLE {0} '.format(name) + template)

def sort_results(cursor):
    """Sort the results table by date. Create new ids.

    :param cursor: sql cursor
    """
    cursor.execute('''CREATE TEMPORARY TABLE results_copy
    AS SELECT * FROM results ORDER BY date ASC''')
    cursor.execute('''DELETE FROM results''')
    cursor.execute('''INSERT INTO results(
    date,
    team_home,
    team_away,
    g_home_end,
    g_away_end,
    odds_1,
    odds_x,
    odds_2)
    SELECT
    date,
    team_home,
    team_away,
    g_home_end,
    g_away_end,
    odds_1,
    odds_x,
    odds_2
    FROM results_copy''')
    cursor.execute('''DROP TABLE results_copy''')

def remove_duplicates_from_results(cursor):
    """Remove duplicated matches from the table results.

    :param cursor: sql cursor
    """
    sort_results(cursor)
    cursor.execute('''delete from results
            where exists (select * from results t2
            where results.date = t2.date
            and results.team_home = t2.team_home
            and results.team_away = t2.team_away
            and results.id > t2.id);''')

def check_line(line):
    """Check line and prepare for inserting to database.

    :type line: []
    :param line: line from csv file
    :rtype: [] or 0-fail
    :return: new_line ready to put into a table
    """
    len_ln = len(line)
    if len_ln < 5 and len(''.join(line).strip()) > 0:
        return 0
    elif len_ln == 5:
        (date, home, away, g_home, g_away) = line[0:5]
        odds_1 = 'null'
        odds_x = 'null'
        odds_2 = 'null'
    elif len_ln > 5:
        (date, home, away, g_home, g_away, odds_1, odds_x, odds_2) = line[0:8]
    else:
        return []
    try:
        goals = map((lambda x: int(x) if x != 'null' and x != '' else 'null'),
                    [g_home, g_away])
    except:
        print_traceback()
        return 0
    try:
        odds = map((lambda x: float(x) if x != 'null' and x != '' else 0),
                   [odds_1, odds_x, odds_2])
    except:
        print_traceback()
        return 0
    try:
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        date = calendar.timegm(date.timetuple())
    except:
        print_traceback()
        return 0
    if len(home.strip()) == 0 or len(away.strip()) == 0:
        return 0
    if g_home == 'null' or g_away == 'null':
        goals = ['null', 'null']
    if not all(odds):
        odds = [0, 0, 0]
    return [date, home, away] + goals + odds

def check_winner(goals_home, goals_away):
    """
    :param goals_home: int
    :param goals_away: int
    :return winner: 1-home 0-draw 2-away
    """
    if goals_home > goals_away:
        winner = 1
    if goals_home < goals_away:
        winner = 2
    if goals_home == goals_away:
        winner = 0

    return winner

def updater_team(cursor, tables, fields, team):
    """Update a table in sql.

    :param cursor: sql cursor
    :param tables:(String) ex. ('table1','table2')
    :param fields: String ex 'wins=wins+1,points=points+3'
    :param where: String ex 'Real'
    :return:
    """
    for table in tables:
        cursor.execute('''
           UPDATE {0}
           SET {1}
           WHERE team={2}'''.format(table, fields, team))

def clear_tables(cursor):
    pass
