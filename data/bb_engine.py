#!/usr/bin/env python -u

"""
Copyright 2013 Jacek Markowski, jacek87markowski@gmail.com

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

import sqlite3
import codecs
import unicodedata
from csv import reader
import os
import locale
locale.setlocale(locale.LC_ALL, "C")
import platform
system = platform.system()
if system == 'Windows':
    from pyfann_win import libfann
elif system == 'Linux':
    from pyfann import libfann
else:
    from pyfann import libfann
from bb_shared import Shared
from PySide import QtGui



class Database(Shared):
    ''' SQL base'''
    def __init__(self, parent=None):
       pass # przerobione
    def load_csv(self, folder, name, expt_name = None, r_min = 5,
                 r_max = 50, mode=0,net = None):
        '''mode:
        0-normal
        1-export
        2-simulation'''
        print net
        with open(os.path.join('tmp','comm'),'w') as comm:
            # communicates with export manager
            comm.write('')
        self.clear_tables()
        ##
        ##return_teams insert fil to sql table + return list of teams
        ##
        teams = self.return_teams(folder, name)
        for team in teams:
            item = team[0]
            self.relations_base.execute('''INSERT INTO league(team)
                                    VALUES(?)''', [(item)])
            self.relations_base.execute('''INSERT INTO series(team)
                                    VALUES(?)''', [(item)])
            self.relations_base.execute('''INSERT INTO scaled(team)
                                    VALUES(?)''', [(item)])
        self.relations_base.execute('''INSERT INTO odds(name,odd_home,odd_draw,odd_away)
                                    VALUES("odds",0.0,0.0,0.0)''')
        # Selecting all matches from database to process
        results = self.relations_base.execute('''SELECT
                                date_txt,
                                home,
                                away,
                                gHomeEnd,
                                gAwayEnd,
                                odd_1,
                                odd_x,
                                odd_2
                                FROM results WHERE NOT gHomeEnd='NULL'
                                ORDER BY date_num ASC
                                ''')
        results = results.fetchall()
        # Processing selected matches
        teams_num = len(teams)
        self.match_group = 0
        self.match_group_date = 0
        index = 0
        for i in results:
            day, home, away, fth, fta, odd_1, odd_x, odd_2  = i[:]
            rounds_m = self.relations_base.execute('''SELECT
            max(matches) FROM league''')
            rounds = rounds_m.fetchone()
            rounds = rounds[0]
            if mode == 1: #export
                with open(os.path.join('tmp','comm'),'r') as comm:
                # communicates with export manager
                    comm_var = comm.readline()
                if comm_var != '':
                    break
                ####################################
                if r_min <= rounds <= r_max:
                    index += 1
                    self.scale_group_check(day)
                    if self.match_group == 1:
                        self.scale_group(teams_num)
                        self.scale_odds(home,away,day)
                        #with open(os.path.join('tmp','print'),'w') as export_print_file:
                        line =  '==== Scaling====' + day + ' Round:' + str(rounds)
                        QtGui.QApplication.processEvents()
                        self.gui.text_export.append(line)
                        #    export_print_file.write('Process data :'+day+' Round %d'%rounds)
                    if odd_1 > 0 and odd_x > 0 and odd_2 > 0:
                        self.export('tmp', home, away, rounds, fth, fta, mode=1)
                    else:
                        self.export('tmp', home, away, rounds, fth, fta, mode=0)
                if rounds <= r_max:
                    self.process_csv(i)
            if self.stop_action == 1:
                break
            if mode == 2: # simulation
                if r_min <= rounds <= r_max:
                    self.scale_group_check(day)
                    if self.match_group == 1:
                        self.scale_group(teams_num)
                    ### used in simulation module
                    self.date = day
                    self.home = home
                    self.away = away
                    self.fth = fth
                    self.fta = fta
                    if odd_1>0 and odd_x > 0 and odd_2 > 0: # odds in file
                        x=2
                    else:
                        x=0 # predict odds
                    self.simulation_prediction(home, away, net, date=day, mode=x)
                    self.simulation_filters(home, away)
                    
                    self.batch_print() # simulation module
                if rounds <= r_max:
                    self.process_csv(i)
            if mode == 0:
                self.process_csv(i)
                # final scale for predicting in stats window
        if mode==0:
            self.scale_group(teams_num)

    def batch_print(self):
        ''' Used in simulator app'''
        pass
    def export(self, expt_name, home, away, rounds, fth, fta, mode=0):
        """
        Exports data for learning
        mode = 0 predict odds
        mode = 1 take odds from database
        """
        with open(os.path.join('tmp', 'export'), 'a') as save:
            scaled_h = self.relations_base.execute('''SELECT
            matches,
            points,
            pointsHome,
            pointsBB,
            pointsBBHome,
            form,
            formHome,
            formBB,
            formBBHome,
            points_b,
            pointsHome_b,
            pointsBB_b,
            pointsBBHome_b,
            form_b,
            formHome_b,
            formBB_b,
            formBBHome_b,
            winhome,
            drawhome,
            losehome,
            winhome_b,
            drawhome_b,
            losehome_b,
            goalsscored,
            goalslost,
            goalsscoredhome,
            goalslosthome,
            goalsscored_b,
            goalslost_b,
            goalsscoredhome_b,
            goalslosthome_b,
            mowins,
            moloses,
            mowinsHome,
            molosesHome,
            f1,
            f2,
            f3,
            f4,
            f1Home,
            f2Home,
            f1BB,
            f2BB,
            f3BB,
            f4BB,
            f1BBHome,
            f2BBHome,
            bts,
            btsHome,
            over25,
            over25Home,
            under25,
            under25Home,
            series_wins,
            series_draws,
            series_loses,
            series_winshome,
            series_drawshome,
            series_loseshome,
            series_noloses,
            series_noloseshome,
            series_nowins,
            series_nowinshome,
            series_nodraws,
            series_nodrawshome,
            series_bts,
            series_btsHome,
            series_over25,
            series_over25Home,
            series_under25,
            series_under25Home
            FROM scaled
            WHERE team="%s"'''%home)
            scaled_h = scaled_h.fetchone()
            scaled_h = str(scaled_h[:])
            scaled_a = self.relations_base.execute('''SELECT
            matches,
            points,
            pointsAway,
            pointsBB,
            pointsBBAway,
            form,
            formAway,
            formBB,
            formBBAway,
            points_b,
            pointsAway_b,
            pointsBB_b,
            pointsBBAway_b,
            form_b,
            formAway_b,
            formBB_b,
            formBBAway_b,
            winaway,
            drawaway,
            loseaway,
            winaway_b,
            drawaway_b,
            loseaway_b,
            goalsscored,
            goalslost,
            goalsscoredaway,
            goalslostaway,
            goalsscored_b,
            goalslost_b,
            goalsscoredaway_b,
            goalslostaway_b,
            mowins,
            moloses,
            mowinsAway,
            molosesAway,
            f1,
            f2,
            f3,
            f4,
            f1Away,
            f2Away,
            f1BB,
            f2BB,
            f3BB,
            f4BB,
            f1BBAway,
            f2BBAway,
            bts,
            btsAway,
            over25,
            over25Away,
            under25,
            under25Away,
            series_wins,
            series_draws,
            series_loses,
            series_winsaway,
            series_drawsaway,
            series_losesaway,
            series_noloses,
            series_nolosesaway,
            series_nowins,
            series_nowinsaway,
            series_nodraws,
            series_nodrawsaway,
            series_bts,
            series_btsAway,
            series_over25,
            series_over25Away,
            series_under25,
            series_under25
            FROM scaled
            WHERE team="%s"'''%away)
            scaled_a = scaled_a.fetchone()
            scaled_a = str(scaled_a[:])
            # prediction mode=1 return predicted oddse
            if mode == 0: # predict odds
                prediction = self.simulation_prediction(home,away,'default',mode=1)
                ## odds
                prd_line = ','+str(prediction[0])+','+str(prediction[1])+','+str(prediction[2])
                # line to write
                line = scaled_h[1:-1]+','+scaled_a[1:-1]+prd_line+self.nl
            if mode == 1: # take odds from database
                odds = self.relations_base.execute('''SELECT odd_home, odd_draw, odd_away FROM odds''')
                odds = odds.fetchone()
                odd_1 = odds[0]
                odd_x = odds[1]
                odd_2 = odds[2]
                odds_line =','+str(odd_1)+','+str(odd_x)+','+str(odd_2)
                line = scaled_h[1:-1]+','+scaled_a[1:-1]+odds_line+self.nl
            if fth > fta:  #win home
                #save.write(home+'-'+away+self.nl)
                save.write(line)
                save.write('-1'+self.nl)
            if fth == fta:  #draw
                #save.write(home+'-'+away+self.nl)
                save.write(line)
                save.write('0'+self.nl)
            if fth < fta:  #win away
                #save.write(home+'-'+away+self.nl)
                save.write(line)
                save.write('1'+self.nl)
    def export_fix(self, expt_name):
        ''' Count lines,inputs and outputs and write in title'''
        print '=============fix'
        path = os.path.join('export','')
        with open(os.path.join('tmp','export'),'r') as f:
            tmp = reader(f)
            tmp = list(tmp)
        with open(path+expt_name,'w') as fix_file:
            inputs = str(len(tmp[0]))
            outputs = str(len(tmp[1]))
            sets = str(len(tmp)/2)
            title = sets+' ' +inputs+' '+outputs+self.nl
            fix_file.write(title)
            for i in tmp:
                line = str(i)
                line = line.replace('[','')
                line = line.replace(']','')
                line = line.replace(' ','')
                line = line.replace(',',' ')
                line = line.replace("'",'')
                fix_file.write(line+self.nl)
            with open(path+expt_name,'r') as f:
                fix_file = f.readline()
            print fix_file

    def scale_group_check(self, day):
        ''' Checks is scaling has been done for current round'''
        if day != self.match_group_date:
            self.match_group_date = day
            self.match_group = 1

    def scale_group(self, teams):
        '''Scales data only once a day before first match'''
        self.match_group = 0
        ############## scale variables
        max_matches = (teams-1)*2.0 # when each team plays 2 matches
                                  #(at home,at away)
        max_points = max_matches*3
        max_points_h = max_matches*1.5
        max_points_a = max_matches*1.5
        max_form = 12
        max_form_h = 6
        max_form_a = 6
        max_points_bb = max_matches*4
        max_points_bb_h = max_matches*2
        max_points_bb_a = max_matches*2
        max_form_bb = 16
        max_form_bb_h = 8
        max_form_bb_a = 8
        max_goals = max_matches * 3
        max_goals_ha = max_goals/2
        ############## in comparision to max to achieve in season
        self.scale('matches', 'matches', 0, max_matches)
        self.scale('points', 'points', 0, max_points)
        self.scale('pointsHome', 'pointsHome', 0, max_points_h)
        self.scale('pointsAway', 'pointsAway', 0, max_points_a)
        self.scale('pointsBB', 'pointsBB', 0, max_points_bb)
        self.scale('pointsBBHome', 'pointsBBHome', 0, max_points_bb_h)
        self.scale('pointsBBAway', 'pointsBBAway', 0, max_points_bb_a)
        self.scale('form', 'form', 0, max_form)
        self.scale('f1', 'f1', 0, 3)
        self.scale('f2', 'f2', 0, 3)
        self.scale('f3', 'f3', 0, 3)
        self.scale('f4', 'f4', 0, 3)
        self.scale('formHome', 'formHome', 0, max_form_h)
        self.scale('f1Home', 'f1Home', 0, 3)
        self.scale('f2Home', 'f2Home', 0, 3)
        self.scale('formAway', 'formAway', 0, max_form_a)
        self.scale('f1Away', 'f1Away', 0, 3)
        self.scale('f2Away', 'f2Away', 0, 3)
        self.scale('formBB', 'formBB', 0, max_form_bb)
        self.scale('f1BB', 'f1BB', 0, 4)
        self.scale('f2BB', 'f2BB', 0, 4)
        self.scale('f3BB', 'f3BB', 0, 4)
        self.scale('f4BB', 'f4BB', 0, 4)
        self.scale('formBBHome', 'formBBHome', 0, max_form_bb_h)
        self.scale('f1BBHome', 'f1BBHome', 0, 4)
        self.scale('f2BBHome', 'f2BBHome', 0, 4)
        self.scale('formBBAway', 'formBBAway', 0, max_form_bb_a)
        self.scale('f1BBAway', 'f1BBAway', 0, 4)
        self.scale('f2BBAway', 'f2BBAway', 0, 4)
        self.scale('goalsscored', 'goalsscored', 0, max_goals)
        self.scale('goalsscoredhome', 'goalsscoredhome', 0, max_goals_ha)
        self.scale('goalsscoredaway', 'goalsscoredaway', 0, max_goals_ha)
        self.scale('goalslost', 'goalslost', 0, max_goals)
        self.scale('goalslosthome', 'goalslosthome', 0, max_goals_ha)
        self.scale('goalslostaway', 'goalslostaway', 0, max_goals_ha)
        self.scale('bts', 'bts', 0, max_matches)
        self.scale('btsHome','btsHome', 0, max_matches/2)
        self.scale('btsAway','btsAway', 0, max_matches/2)
        self.scale('over25', 'over25', 0, max_matches)
        self.scale('over25Home','over25Home', 0, max_matches/2)
        self.scale('over25Away','over25Away', 0, max_matches/2)
        self.scale('under25', 'under25', 0, max_matches)
        self.scale('under25Home','under25Home', 0, max_matches/2)
        self.scale('under25Away','under25Away', 0, max_matches/2)
        ############## in comparision to others
        self.scale('winhome', 'winhome_b')
        self.scale('drawhome', 'drawhome_b')
        self.scale('losehome', 'losehome_b')
        self.scale('winaway', 'winaway_b')
        self.scale('drawaway', 'drawaway_b')
        self.scale('loseaway', 'loseaway_b')
        self.scale('points', 'points_b')
        self.scale('pointsHome', 'pointsHome_b')
        self.scale('pointsAway', 'pointsAway_b')
        self.scale('pointsBB', 'pointsBB_b')
        self.scale('pointsBBHome', 'pointsBBHome_b')
        self.scale('pointsBBAway', 'pointsBBAway_b')
        self.scale('form', 'form_b')
        self.scale('formHome', 'formHome_b')
        self.scale('formAway', 'formAway_b')
        self.scale('formBB', 'formBB_b')
        self.scale('formBBHome', 'formBBHome_b')
        self.scale('formBBAway', 'formBBAway_b')
        self.scale('goalsscored', 'goalsscored_b')
        self.scale('goalsscoredhome', 'goalsscoredhome_b')
        self.scale('goalsscoredaway', 'goalsscoredaway_b')
        self.scale('goalslost', 'goalslost_b')
        self.scale('goalslosthome', 'goalslosthome_b')
        self.scale('goalslostaway', 'goalslostaway_b')
        ############## mov,mol
        self.scale('mowins', 'mowins', 0, 3)
        self.scale('mowinsHome', 'mowinsHome', 0, 3)
        self.scale('mowinsAway', 'mowinsAway', 0, 3)
        self.scale('moloses', 'moloses', 0, 3)
        self.scale('molosesHome', 'molosesHome', 0, 3)
        self.scale('molosesAway', 'molosesAway', 0, 3)
        ################ series
        self.scale('series_wins', 'series_wins',
                   min_value=0, max_value=10, series=1)
        self.scale('series_draws', 'series_draws',
                   min_value=0, max_value=10, series=1)
        self.scale('series_loses', 'series_loses',
                   min_value=0, max_value=10, series=1)
        self.scale('series_winshome', 'series_winshome',
                   min_value=0, max_value=10, series=1)
        self.scale('series_drawshome', 'series_drawshome',
                   min_value=0, max_value=10, series=1)
        self.scale('series_loseshome', 'series_loseshome',
                   min_value=0, max_value=10, series=1)
        self.scale('series_winsaway', 'series_winsaway',
                   min_value=0, max_value=10, series=1)
        self.scale('series_drawsaway', 'series_drawsaway',
                   min_value=0, max_value=10, series=1)
        self.scale('series_losesaway', 'series_losesaway'
        , min_value=0, max_value=10, series=1)
        self.scale('series_noloses', 'series_noloses',
                   min_value=0, max_value=10, series=1)
        self.scale('series_noloseshome', 'series_noloseshome',
                   min_value=0, max_value=10, series=1)
        self.scale('series_nolosesaway', 'series_nolosesaway',
                   min_value=0, max_value=10, series=1)
        self.scale('series_nowins', 'series_nowins',
                   min_value=0, max_value=10, series=1)
        self.scale('series_nowinshome', 'series_nowinshome',
                   min_value=0, max_value=10, series=1)
        self.scale('series_nowinsaway', 'series_nowinsaway',
                   min_value=0, max_value=10, series=1)
        self.scale('series_nodraws', 'series_nodraws',
                   min_value=0, max_value=10, series=1)
        self.scale('series_nodrawshome', 'series_nodrawshome',
                   min_value=0, max_value=10, series=1)
        self.scale('series_nodrawsaway', 'series_nodrawsaway',
                   min_value=0, max_value=10, series=1)
        self.scale('series_bts', 'series_bts',
                   min_value=0, max_value=10, series=1)
        self.scale('series_btsHome', 'series_btsHome',
                   min_value=0, max_value=10, series=1)
        self.scale('series_btsAway', 'series_btsAway',
                   min_value=0, max_value=10, series=1)
        self.scale('series_over25', 'series_over25',
                   min_value=0, max_value=10, series=1)
        self.scale('series_over25Home', 'series_over25Home',
                   min_value=0, max_value=10, series=1)
        self.scale('series_over25Away', 'series_over25Away',
                   min_value=0, max_value=10, series=1)
        self.scale('series_under25', 'series_under25',
                   min_value=0, max_value=10, series=1)
        self.scale('series_under25Home', 'series_under25Home',
                   min_value=0, max_value=10, series=1)
        self.scale('series_under25Away', 'series_under25Away',
                   min_value=0, max_value=10, series=1)


    def scale_odds(self, home,away,date,min_value=1,max_value=20):
        """
        scales odds to range(-1,1)
        """
        odds = self.relations_base.execute('''SELECT odd_1,odd_x,odd_2
        FROM results WHERE home="%s" AND away="%s" AND date_txt="%s"'''%(home,away,date))
        odd_home,odd_draw,odd_away = odds.fetchone()
        scaled_1 = 2.0*(float(odd_home)-min_value)/(max_value-min_value)-1
        scaled_x = 2.0*(float(odd_draw)-min_value)/(max_value-min_value)-1
        scaled_2 = 2.0*(float(odd_away)-min_value)/(max_value-min_value)-1
        val = [scaled_1,scaled_x,scaled_2]
        for i in range(0,len(val)):
            if val[i] > 1:
                val[i]=1
            elif val[i] < 1:
                val[i]=-1
        self.relations_base.execute('''UPDATE odds SET odd_home=?,odd_draw=?,odd_away=?''',(scaled_1,scaled_x,scaled_2))
        return (scaled_1,scaled_x,scaled_2)
    def scale(self, record_in, record_out, min_value=None, max_value=None,
              series=0):
        ''' Scales data to range(-1,1), Need some tweaks to speed up'''
        if max_value == None:
            if series == 0:
                max_value = self.relations_base.execute('''SELECT max(%s)
                                               FROM league''' %record_in)
            else:
                max_value = self.relations_base.execute('''SELECT max(%s)
                                               FROM series''' %record_in)
            max_value, = max_value.fetchone()
        if min_value == None:
            if series == 0:
                min_value = self.relations_base.execute('''SELECT min(%s)
                                               FROM league''' %record_in)
            else:
                min_value = self.relations_base.execute('''SELECT min(%s)
                                               FROM series''' %record_in)
            min_value, = min_value.fetchone()

        if series == 0:
            teams = self.relations_base.execute('''SELECT %s,team
                                                FROM league''' %record_in)
        else:
            teams = self.relations_base.execute('''SELECT %s,team
                                                FROM series''' %record_in)
        teams = tuple(teams)
        try:
            for i in teams:
                scaled = 2.0*(i[0]-min_value)/(max_value-min_value)-1
                if scaled < -1:
                    scaled = -1
                elif scaled > 1:
                    scaled = 1
                self.relations_base.execute('''UPDATE scaled
                    SET %s=? WHERE team=? ''' %record_out, (scaled, i[1]))
        except:
            print 'Scale: error'

    def simulation_filters(self, home, away):
        ''' Loads into variables actual team stats to compare with filters'''
        # filters variables
        t1_stats = self.relations_base.execute('''SELECT points,pointsHome,
                form,formHome FROM league
                WHERE team="%s"'''%home)
        t1 = tuple(t1_stats)
        for i in t1:
            self.t1_points = i[0]
            self.t1_points_h = i[1]
            self.t1_form = i[2]
            self.t1_form_h = i[3]
        t1_series = self.relations_base.execute('''SELECT series_wins,
                series_winshome,series_draws,series_drawshome,series_loses,
                series_loseshome,series_nowins,series_nowinshome,
                series_nodraws,series_nodrawshome,series_noloses,
                series_noloseshome,series_bts,series_btsHome,series_over25,
                series_over25Home,series_under25,series_under25Home
                FROM series
                WHERE team="%s"'''%home)
        t1 = tuple(t1_series)
        for i in t1:
            self.t1_wins = i[0]
            self.t1_winshome = i[1]
            self.t1_draws = i[2]
            self.t1_drawshome = i[3]
            self.t1_loses = i[4]
            self.t1_loseshome = i[5]
            self.t1_nowins = i[6]
            self.t1_nowinshome = i[7]
            self.t1_nodraws = i[8]
            self.t1_nodrawshome = i[9]
            self.t1_noloses = i[10]
            self.t1_noloseshome = i[11]
            self.t1_bts = i[12]
            self.t1_btshome = i[13]
            self.t1_over = i[14]
            self.t1_overhome = i[15]
            self.t1_under = i[16]
            self.t1_underhome = i[17]

        t2_stats = self.relations_base.execute('''SELECT points,pointsHome,
                form,formHome FROM league
                WHERE team="%s"'''%away)
        t2 = tuple(t2_stats)
        for i in t2:
            self.t2_points = i[0]
            self.t2_points_a = i[1]
            self.t2_form = i[2]
            self.t2_form_a = i[3]
        t2_series = self.relations_base.execute('''SELECT series_wins,
                series_winsaway,series_draws,series_drawsaway,
                series_loses,series_losesaway,series_nowins,
                series_nowinsaway,series_nodraws,series_nodrawsaway,
                series_noloses,series_nolosesaway,series_bts,
                series_btsAway,series_over25,series_over25Away,
                series_under25,series_under25Away
                FROM series
                WHERE team="%s"'''%away)
        t2 = tuple(t2_series)
        for i in t2:
            self.t2_wins = i[0]
            self.t2_winsaway = i[1]
            self.t2_draws = i[2]
            self.t2_drawsaway = i[3]
            self.t2_loses = i[4]
            self.t2_losesaway = i[5]
            self.t2_nowins = i[6]
            self.t2_nowinsaway = i[7]
            self.t2_nodraws = i[8]
            self.t2_nodrawsaway = i[9]
            self.t2_noloses = i[10]
            self.t2_nolosesaway = i[11]
            self.t2_bts = i[12]
            self.t2_btsaway = i[13]
            self.t2_over = i[14]
            self.t2_overaway = i[15]
            self.t2_under = i[16]
            self.t2_underaway = i[17]

        ####
        # Odds
        ####
        odds = self.relations_base.execute('''SELECT odd_1,odd_x,odd_2
        FROM results WHERE (home="%s" AND away="%s" AND date_txt = "%s")'''%(home,away,self.date))
        odds = odds.fetchone()
        if odds[0]>0 and odds[1]>0 and odds[2]>0: # odds in file
            self.odds = odds
            self.odd_1,self.odd_x,self.odd_2 = odds
            self.odd_1 = self.odd_1*self.odds_level/100
            self.odd_x = self.odd_x*self.odds_level/100
            self.odd_2 = self.odd_2*self.odds_level/100
            self.odd_1x = round(1/((1/self.odd_1) + (1/self.odd_x)),3)
            self.odd_x2 = round(1/((1/self.odd_x) + (1/self.odd_2)),3)
        else: # no odds, predict odds
            self.odds = self.simulation_prediction(home,away,'default',mode=1)
            self.odd_1 = round(self.odds_rescale(self.odds[0],self.odds_level),3)
            self.odd_x = round(self.odds_rescale(self.odds[1],self.odds_level),3)
            self.odd_2 = round(self.odds_rescale(self.odds[2],self.odds_level),3)
            self.odd_1x = round(1/((1/self.odd_1) + (1/self.odd_x)),3)
            self.odd_x2 = round(1/((1/self.odd_x) + (1/self.odd_2)),3)
        if self.odd_1 < 1:
            self.odd_1 = 1.0
        if self.odd_2 < 1:
            self.odd_2 = 1.0
        if self.odd_x < 1:
            self.odd_x = 1.0
        if self.odd_x2 < 1:
            self.odd_x2 = 1.0
        if self.odd_1x < 1:
            self.odd_1x = 1.0
    def process_csv(self, results):
        pass # przerobione
    def clear_tables(self):
        '''Reamoves all data form tables for new file process '''

        try:
            self.relations_base.execute('''DELETE FROM league
                                            WHERE id''')
        except:
            print 'League table deletion error'

        try:
            self.relations_base.execute('''DELETE FROM results WHERE id''')
        except:
            print 'League results deletion error'

        try:
            self.relations_base.execute('''DELETE FROM series WHERE id''')
        except:
            print 'Series table deletion error'
        try:
            self.relations_base.execute('''DELETE FROM scaled WHERE id''')
        except:
            print 'Scaled table deletion error'
        try:
            self.relations_base.execute('''DELETE FROM odds WHERE id''')
        except:
            print 'Odds table deletion error'
    def simulation_prediction(self, home, away, net, date=0, mode=0):
        ''' Predict outcome form match using given net
        mode 0 predicting outcomes (1,x,2) using predicted odds
        mode 1 predictiong odds
        mode 2 predict outcomes (1,x,2) using odds from file
        '''
        path_net = os.path.join('net','')
        path_odds = os.path.join('odds','')
        input_list = []
        t1 = self.relations_base.execute('''SELECT
            matches,
            points,
            pointsHome,
            pointsBB,
            pointsBBHome,
            form,
            formHome,
            formBB,
            formBBHome,
            points_b,
            pointsHome_b,
            pointsBB_b,
            pointsBBHome_b,
            form_b,
            formHome_b,
            formBB_b,
            formBBHome_b,
            winhome,
            drawhome,
            losehome,
            winhome_b,
            drawhome_b,
            losehome_b,
            goalsscored,
            goalslost,
            goalsscoredhome,
            goalslosthome,
            goalsscored_b,
            goalslost_b,
            goalsscoredhome_b,
            goalslosthome_b,
            mowins,
            moloses,
            mowinsHome,
            molosesHome,
            f1,
            f2,
            f3,
            f4,
            f1Home,
            f2Home,
            f1BB,
            f2BB,
            f3BB,
            f4BB,
            f1BBHome,
            f2BBHome,
            bts,
            btsHome,
            over25,
            over25Home,
            under25,
            under25Home,
            series_wins,
            series_draws,
            series_loses,
            series_winshome,
            series_drawshome,
            series_loseshome,
            series_noloses,
            series_noloseshome,
            series_nowins,
            series_nowinshome,
            series_nodraws,
            series_nodrawshome,
            series_bts,
            series_btsHome,
            series_over25,
            series_over25Home,
            series_under25,
            series_under25Home
            FROM scaled
            WHERE team="%s"'''%home)
        t1 = tuple(t1)
        for i in t1[0]:
            input_list.append(i)
        t2 = self.relations_base.execute('''SELECT
            matches,
            points,
            pointsAway,
            pointsBB,
            pointsBBAway,
            form,
            formAway,
            formBB,
            formBBAway,
            points_b,
            pointsAway_b,
            pointsBB_b,
            pointsBBAway_b,
            form_b,
            formAway_b,
            formBB_b,
            formBBAway_b,
            winaway,
            drawaway,
            loseaway,
            winaway_b,
            drawaway_b,
            loseaway_b,
            goalsscored,
            goalslost,
            goalsscoredaway,
            goalslostaway,
            goalsscored_b,
            goalslost_b,
            goalsscoredaway_b,
            goalslostaway_b,
            mowins,
            moloses,
            mowinsAway,
            molosesAway,
            f1,
            f2,
            f3,
            f4,
            f1Away,
            f2Away,
            f1BB,
            f2BB,
            f3BB,
            f4BB,
            f1BBAway,
            f2BBAway,
            bts,
            btsAway,
            over25,
            over25Away,
            under25,
            under25Away,
            series_wins,
            series_draws,
            series_loses,
            series_winsaway,
            series_drawsaway,
            series_losesaway,
            series_noloses,
            series_nolosesaway,
            series_nowins,
            series_nowinsaway,
            series_nodraws,
            series_nodrawsaway,
            series_bts,
            series_btsAway,
            series_over25,
            series_over25Away,
            series_under25,
            series_under25Away
            FROM scaled
            WHERE team="%s"'''%away)
        t2 = tuple(t2)
        for i in t2[0]:
            input_list.append(i)
        locale.setlocale(locale.LC_ALL, "C")
        if mode == 0: # prediction using predicted odds
            ann = libfann.neural_net()
            ann.create_from_file(path_odds+'odds.net')
            odds = ann.run(input_list[:])
            for i in odds:
                input_list.append(i)
            ann = libfann.neural_net()
            ann.create_from_file(path_net+str(net))
            prediction = ann.run(input_list[:])
            self.prediction = prediction[0]
            return self.prediction
        elif mode == 1: # predict odds
            ann = libfann.neural_net()
            ann.create_from_file(path_odds+'odds.net')
            odds = ann.run(input_list[:])
            return odds
        elif mode == 2: #prediction using odds from file
            print 'simulation using odds'
            odds = self.scale_odds(home,away,date)
            print odds
            for i in odds:
                input_list.append(i)
            ann = libfann.neural_net()
            ann.create_from_file(path_net+str(net))
            prediction = ann.run(input_list[:])
            self.prediction = prediction[0]
            return self.prediction
    def return_teams(self, folder, name):
        ''' Adds all matches to sql and return list of teams'''
        self.clear_tables()
        file_open = reader(open(folder+name))
        for line in file_open:
            date = line[0]
            date = date[0:7]+date[8:]
            date_num = float(date)
            fth = line[3]
            fta = line[4]
            
            if len(line)>5: # files with odds included
                if line[5] == "NULL":
                    odd_1 = 0
                else:
                    odd_1 = line[5]
            else:
                odd_1 = 0
            if len(line)>5:
                if line[6] == "NULL":
                    odd_x = 0
                else:
                    odd_x = line[6]
            else:
                odd_x = 0
            if len(line)>5:
                if line[7] == "NULL":
                    odd_2 = 0
                else:
                    odd_2 = line[7]
            else:
                odd_2 = 0
            home_txt = line[1].decode('utf8', 'replace')
            away_txt = line[2].decode('utf8', 'replace')
            home = unicodedata.normalize('NFD', home_txt).encode('ascii', 'ignore')
            away = unicodedata.normalize('NFD', away_txt).encode('ascii', 'ignore')
            if fth == '' or fta =='':
                fth = 'NULL'
                fta = 'NULL'
            self.relations_base.execute('''INSERT INTO results(
            date_txt,
            date_num,
            home,
            away,
            gHomeEnd,
            gAwayEnd,
            odd_1,
            odd_x,
            odd_2) VALUES(?,?,?,?,?,?,?,?,?)''',
            (
            line[0],
            date_num,
            home,
            away,
            fth,
            fta,
            odd_1,
            odd_x,
            odd_2))
        #always sort results according to date
        self.relations_base.execute('''CREATE TEMPORARY TABLE results_copy
        AS SELECT * FROM results ORDER BY date_num ASC''')
        self.relations_base.execute('''DELETE FROM results''')
        self.relations_base.execute('''INSERT INTO results(
                                    date_txt,
                                    date_num,
                                    home,
                                    away,
                                    gHomeEnd,
                                    gAwayEnd,
                                    odd_1,
                                    odd_x,
                                    odd_2)
                                    SELECT
                                    date_txt,
                                    date_num,
                                    home,
                                    away,
                                    gHomeEnd,
                                    gAwayEnd,
                                    odd_1,
                                    odd_x,
                                    odd_2
                                    FROM results_copy''')
        self.relations_base.execute('''DROP TABLE results_copy''')
        # remove duplicates:
        self.relations_base.execute('''delete from results
            where exists (select * from results t2
            where results.date_num = t2.date_num
            and results.home = t2.home
            and results.away = t2.away
            and results.id > t2.id);''')


        teams = self.relations_base.execute('''SELECT DISTINCT home
                                             FROM results''')
        teams = teams.fetchall()
        self.relations_base.execute('''SELECT DISTINCT away FROM results''')
        for i in self.relations_base:
            if i not in teams:
                teams.append(i)
        teams.sort()
        return teams

def main():
    ''' Main function'''
    print 'print a'
    x = Database()
    #x.load_csv(os.path.join('leagues', 'current', ''), 'default', expt_name='jhjh',mode = 1)

if __name__ == '__main__':
    main()

