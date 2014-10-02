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

RESULTS = '''
    (id INTEGER PRIMARY KEY,
    date INTEGER,
    team_home TEXT,
    team_away TEXT,
    g_home_end INTEGER,
    g_away_end INTEGER,
    odds_1 FLOAT DEFAULT 0,
    odds_x FLOAT DEFAULT 0,
    odds_2 FLOAT DEFAULT 0)'''

TEAM_BASIC = \
    ''' (id INTEGER PRIMARY KEY,
    team TEXT,
    matches INTEGER DEFAULT 0,
    points INTEGER DEFAULT 0,
    wins INTEGER DEFAULT 0,
    draws INTEGER DEFAULT 0,
    loses INTEGER DEFAULT 0,
    goals_scored INTEGER DEFAULT 0,
    goals_lost INTEGER DEFAULT 0)'''

TEAM_BASIC_SCALED = TEAM_BASIC.replace('INTEGER', 'FLOAT')

TEAM_FORM = \
    ''' (id INTEGER PRIMARY KEY,
    team TEXT,
    f1 INTEGER DEFAULT 0,
    f2 INTEGER DEFAULT 0,
    f3 INTEGER DEFAULT 0,
    f4 INTEGER DEFAULT 0,
    f1_opponent TEXT,
    f2_opponent TEXT,
    f3_opponent TEXT,
    f4_opponent TEXT)'''

TEAM_FORM_SCALED = TEAM_FORM.replace('INTEGER', 'FLOAT')
TEAM_FORM_BB = TEAM_FORM_SCALED

TEAM_ADVANCED = \
    ''' (id INTEGER PRIMARY KEY,
    team TEXT,
    points FLOAT DEFAULT 50,
    margin_of_wins FLOAT DEFAULT 0,
    margin_of_loses FLOAT DEFAULT 0,
    goal_difference_wins FLOAT DEFAULT 0,
    goal_difference_loses FLOAT DEFAULT 0,
    bts INTEGER DEFAULT 0,
    over25 INTEGER DEFAULT 0,
    under25 INTEGER DEFAULT 0)'''

TEAM_ADVANCED_SCALED = TEAM_ADVANCED.replace('INTEGER', 'FLOAT')

TEAM_SERIES = '''
    (id INTEGER PRIMARY KEY,
    team TEXT,
    wins INTEGER NOT NULL DEFAULT 0,
    draws INTEGER NOT NULL DEFAULT 0,
    loses INTEGER NOT NULL DEFAULT 0,
    noloses INTEGER NOT NULL DEFAULT 0,
    nowins INTEGER NOT NULL DEFAULT 0,
    nodraws INTEGER NOT NULL DEFAULT 0,
    bts INTEGER DEFAULT 0,
    no_bts INTEGER DEFAULT 0,
    over25 INTEGER DEFAULT 0,
    no_over25 INTEGER DEFAULT 0,
    under25 INTEGER DEFAULT 0,
    no_under25 INTEGER DEFAULT 0)'''

SERIES_SCALED = TEAM_SERIES.replace('INTEGER', 'FLOAT')

ODDS = '''
    (id INTEGER PRIMARY KEY,
    name TEXT,
    odd_home FLOAT DEFAULT 0,
    odd_draw FLOAT DEFAULT 0,
    odd_away FLOAT DEFAULT 0)'''

ODDS_SCALED = ODDS

