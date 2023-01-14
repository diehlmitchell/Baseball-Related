#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 17:19:46 2021
@author: EmilioMartinez
"""

# NEEDS A REQUIREMENTS.txt 
import pybaseball as pyb
from pybaseball import statcast, statcast_batter, statcast_pitcher, spraychart, team_pitching, team_pitching_bref, pitching_stats, batting_stats, playerid_lookup
from pybaseball.plotting import plot_bb_profile, plot_stadium

import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
 
#get playeerid for archie from pybaseball 
# (NOTE: WHAT IS PLAYER? (Whats in it for example) TO FIND OUT LATER)
archies_playerid = playerid_lookup('Bradley', 'Archie')

#get his career stats up till 2021 (INCLUDES 2020)
before_archies_mlb_debut = '2018-01-01'
pitch_sample_stop_date = '2020-12-31'

# get archies data from statcast  --- https://github.com/jldbc/pybaseball/blob/master/docs/statcast_pitcher.md
data_archie = statcast_pitcher(before_archies_mlb_debut, pitch_sample_stop_date, 605151) #before I replaced it this number was 605151

# get and display headers for data_archie_header
# iterating the columns
# for col in data_archie.columns:
#     print(col)

# label events with the 4 hit types as hits
data_archie.loc[
      (data_archie['events'] == 'single')  
    | (data_archie['events'] == 'double') 
    | (data_archie['events'] == 'triple') 
    | (data_archie['events'] == 'home_run'),
'hit_out'] = 'hit'  

# label remaing events as outs
data_archie.loc[
      (data_archie['events'] != 'single') 
    & (data_archie['events'] != 'double') 
    & (data_archie['events'] != 'triple') 
    & (data_archie['events'] != 'home_run'),
'hit_out'] = 'out' 

#Hexbin using BBE coordinates, change color basedo n what metric wants to be shown --- https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.hexbin.html
plt.hexbin(data_archie['hc_x'], data_archie['hc_y']*-1, C=data_archie['launch_speed']>50 ,cmap=plt.cm.YlOrRd, gridsize = 20)
cb = plt.colorbar()
cb.set_label('Exit Velo')
#plt.xlabel('Exit Velocity')
#plt.ylabel('Launch Angle') 
plt.title('Archie Bradley Career Hits Allowed Density')
plt.show() 

#Create a function using the stadium csv ile from pybaseball. This will plot outlines of all stadiums
stadium = pd.read_csv('https://raw.githubusercontent.com/jldbc/pybaseball/master/pybaseball/data/mlbstadiums.csv')
stadium['y'] = stadium['y'] * -1
stadium = stadium.loc[:,'team':]

def plot_stadium(team, color):
    team_df = stadium[stadium['team'] == team.lower()]
    for i in stadium['segment'].unique():
        data = team_df[team_df['segment'] == i]
        plt.plot(data['x'],data['y'], linestyle = '-', color = color) 
    #plt.suptitle(team.capitalize(), y=.975, fontsize=15)
    plt.title(team_df['location'].any(), fontsize=8)
    plt.axis('off')

#Overlay archie hexbin of hits with Citizens bank park
plt.hexbin(data_archie['hc_x'], data_archie['hc_y']*-1, C=data_archie['hit_out']=='hit',cmap=plt.cm.YlOrRd, gridsize = 25)
plot_stadium('phillies','black') 
cb = plt.colorbar()
cb.set_label('Hit Probablity') 
plt.suptitle('Archie Bradley Career Hit Allowance', y=.975, fontsize=15)
plt.title('Overlaid at Citizens Bank Park')
plt.show()

#Overlay archie hexbin of EV with Citizens bank park
plot_stadium('phillies','black')
plt.hexbin(data_archie['hc_x'], data_archie['hc_y']*-1, C=data_archie['launch_speed'],cmap=plt.cm.Spectral_r, gridsize = 25)
cb = plt.colorbar()
cb.set_label('Exit Velocity') 
plt.suptitle('Archie Bradley Career BBE by Exit Velocity', y=.975, fontsize=15)
plt.title('Overlaid at Citizens Bank Park')
plt.show()
