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
from decimal import Decimal as D
from data.sql.services import selector_team


def new_rating(cursor, team_home, team_away, outcome):
    """

    :param cursor: sl cursor
    :param team_home: string
    :param team_away: string
    :param outcome: int 1-home 0-draw 2-away
    :return new_rating: (float, float)
    """
    p = 'points'
    p_max_min = 'MAX(points), MIN(points)'
    f = 'form'
    f_max_min = 'MAX(form), MIN(form)'
    table_p = 'team_advanced'
    table_p_h = 'team_advanced_home'
    table_p_a = 'team_advanced_away'
    table_f = 'team_form_bb'
    table_f_h = 'team_form_bb_home'
    table_f_a = 'team_form_bb_away'

    # team_home
    #p1 = selector_team(cursor, table_p, p, team_home)
    #(max_p1, min_p1) = selector_team(cursor, table_p, p_max_min, team_home)
    p1h = selector_team(cursor, table_p_h, p, team_home)
    (max_ph, min_ph) = selector_team(cursor, table_p_h, p_max_min, team_home)
    #f1 = selector_team(cursor, table_f, f, team_home)
    #(max_f, min_f) = selector_team(cursor, table_f, f_max_min, team_home)
    f1h = selector_team(cursor, table_f_h, f, team_home)
    (max_fh, min_ph) = selector_team(cursor, table_f_h, f_max_min, team_home)

    # team_away
    #p2 = selector_team(cursor, table_p, p, team_away)
    #(max_p, min_p) = selector_team(cursor, table_p, p_max_min, team_away)
    p2a = selector_team(cursor, table_p_a, p, team_away)
    (max_pa, min_pa) = selector_team(cursor, table_p_a, p_max_min, team_away)
    #f2 = selector_team(cursor, table_f, f, team_away)
    #(max_f , min_f ) = selector_team(cursor, table_f, f_max_min, team_away)
    f2a = selector_team(cursor, table_f_a, f, team_away)
    (max_fa, min_pa) = selector_team(cursor, table_f_a, f_max_min, team_away)


    if outcome == 1:
        new_home = 3 + D(p2a)/D(max_pa) + D(f2a)/D(max_fa)
        new_away = D(p1h)/D(max_ph) + D(f1h)/D(max_fh)
    elif outcome == 0:
        new_home = 1 + D(p2a)/D(max_pa) + D(f2a)/D(max_fa)
        new_away = 1 + D(p1h)/D(max_ph) + D(f1h)/D(max_fh)
    elif outcome == 2:
        new_home = D(p2a)/D(max_pa) + D(f2a)/D(max_fa)
        new_away = 3 + D(p1h)/D(max_ph) + D(f1h)/D(max_fh)
    check_limits = lambda x: float(x) if 0 <= x <= 100 else 0 if x < 0 else 100

    return map(check_limits, [new_home, new_away])

