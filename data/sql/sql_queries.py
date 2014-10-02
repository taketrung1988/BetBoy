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


def get_matches(cursor, team):
    """
    Get matches of a given  team.

    :param cursor: sql cursor
    :param team: team name
    :return:
    """
    return cursor.execute(
        'SELECT matches FROM '
        'team_basic WHERE team={0}'.format(team)).fetch_one()[0]


def get_teams(self):
    """
    :rtype: [String]
    :return results: list of teams
    """
    home = self.cur.execute('''SELECT DISTINCT team_home
    FROM results''').fetchall()
    away = self.cur.execute('''SELECT DISTINCT team_away
    FROM results''').fetchall()
    teams = filter(
        (lambda x: True if x not in home else False), away) + home
    return map(lambda x: x[0], teams)


def get_results(self):
    """
    :rtype: [()]
    :return results: all results
    """
    results = self.cur.execute('''SELECT * FROM results''').fetchall()
    return results


def get_results_home(self, team):
    """
    :type team: String
    :param team: name of a team
    :rtype results: [()]
    :return: home results of a team
    """
    results = self.cur.execute('''SELECT * FROM results
    WHERE team_home={0}'''.format(team)).fetchall()
    return results


def get_results_away(self, team):
    """
    :type team: String
    :param team: name of a team
    :rtype results: [()]
    :return: away results of a team
    """
    results = self.cur.execute('''SELECT * FROM results
    WHERE team_away={0}'''.format(team)).fetchall()
    return results