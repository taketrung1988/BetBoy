# -*- coding: utf-8 -*-
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
from data.third_party.peewee.peewee import (Model, SqliteDatabase, TextField,
                                            FloatField, IntegerField,
                                            ForeignKeyField)

db = SqliteDatabase(':memory:')


class BaseModel(Model):
    class Meta:
        database = db


class Team(BaseModel):
    name = TextField(unique=True)


class TeamStats(BaseModel):
    team = ForeignKeyField(Team)
    matches = IntegerField(default=0)
    wins = IntegerField(default=0)
    draws = IntegerField(default=0)
    loses = IntegerField(default=0)
    goals_scored = IntegerField(default=0)
    goals_lost = IntegerField(default=0)
    points = IntegerField(default=0)
    points_bb = FloatField(default=0)
    margin_of_wins = FloatField(default=0)
    margin_of_loses = FloatField(default=0)
    goal_diff_wins = IntegerField(default=0)
    goal_diff_loses = IntegerField(default=0)
    bts = IntegerField(default=0)
    over25 = IntegerField(default=0)
    under25 = IntegerField(default=0)


class TeamStatsHome(TeamStats):
    pass


class TeamStatsAway(TeamStats):
    pass


class LastMatches(BaseModel):
    team = ForeignKeyField(Team)
    opponent = ForeignKeyField(Team, related_name='opp')
    points = IntegerField(default=0)
    points_bb = FloatField(default=0)


class LastMatchesHome(LastMatches):
    opponent = ForeignKeyField(Team, related_name='oppH')


class LastMatchesAway(LastMatches):
    opponent = ForeignKeyField(Team, related_name='oppA')


class Series(BaseModel):
    team = ForeignKeyField(Team, related_name='series')
    wins = IntegerField(default=0)
    draws = IntegerField(default=0)
    loses = IntegerField(default=0)
    no_loses = IntegerField(default=0)
    no_wins = IntegerField(default=0)
    no_draws = IntegerField(default=0)
    bts = IntegerField(default=0)
    no_bts = IntegerField(default=0)
    over25 = IntegerField(default=0)
    no_over25 = IntegerField(default=0)
    under25 = IntegerField(default=0)
    no_under25 = IntegerField(default=0)


class SeriesHome(Series):
    team = ForeignKeyField(Team, related_name='seriesH')


class SeriesAway(Series):
    team = ForeignKeyField(Team, related_name='seriesA')





