
import pandas as pd
from math import log, fsum

def WP(df_name, season, team_id):
    """ Calculates Winning Percentage
    """

    wintable1 = df_name.ix[[season]]
    wintable2 = wintable1[wintable1.wteam == team_id]
    away_wins = len(wintable2[wintable2.wloc == 'A'])
    neutral_wins = len(wintable2[wintable2.wloc == 'N'])
    home_wins = len(wintable2[wintable2.wloc == 'H'])
    effective_wins = (1.4*away_wins) + (1.0*neutral_wins) + (0.6*home_wins)

    losstable1 = df_name.ix[[season]]
    losstable2 = losstable1[losstable1.lteam == team_id]
    away_losses = len(losstable2[losstable2.wloc == 'H']) #'wloc' refers to location of WINNING team
    neutral_losses = len(losstable2[losstable2.wloc == 'N'])
    home_losses = len(losstable2[losstable2.wloc == 'A']) 
    effective_losses = (1.4*home_losses) + (1.0*neutral_losses) + (0.6*away_losses)
    
    WP = effective_wins/(effective_wins + effective_losses)
    return WP


def teams_played(season_tab, primary_id):
    """ Creates lists of opponent teams for primary team 
    """
    team_tab = season_tab[(season_tab.wteam == primary_id) | (season_tab.lteam == primary_id)]
    team_list1 = team_tab.wteam[team_tab.wteam != primary_id]
    team_list2 = team_tab.lteam[team_tab.lteam != primary_id]
    team_list = pd.concat([team_list1, team_list2], axis = 0)
    return team_list


def OWP(df_name, season, primary_id):
    """ Calculates average of the Opponent Winning Percentage for the primary team
    """
    season_tab = df_name.ix[[season]]
    OWP_list = []
    team_list = []

    # Find teams that played against primary team
    team_list = teams_played(season_tab, primary_id)

    for id in team_list:
        win_table = season_tab[(season_tab.wteam == int(id)) & (season_tab.lteam != primary_id)]
        wins = len(win_table.wteam)
        lose_table = season_tab[(season_tab.lteam == int(id)) & (season_tab.wteam != primary_id)]
        losses = len(lose_table.lteam)
        if (wins != 0) & (losses != 0):
            OWP_list.append((float(wins))/(float(wins)+float(losses)))

    OWP = sum(OWP_list)/len(OWP_list)

    return OWP


def OOWP(df_name, season, primary_id):
    """ Calculates opponents OWP for primary team
    """
    
    opponents_list = teams_played(df_name.ix[[season]], primary_id)
    opponents_OWP = {}

    for team in opponents_list:
        if team in opponents_OWP:
            opponents_OWP[team].append(OWP(df_name, season, team))
        else:
            opponents_OWP[team] = [OWP(df_name, season, team)]
 
        
    OOWP = sum(sum(v) for v in opponents_OWP.values()) / (sum(len(v) for v in opponents_OWP.itervalues()))
    return OOWP


def RPI(df_name, season, primary_id):
    """ Calculates the RPI for the primary team for a given season. 
    """
  
    RPI = (0.25*WP(df_name, season, primary_id)) + \
          (0.50 * OWP(df_name, season, primary_id)) + \
          (0.25 * OOWP(df_name, season, primary_id))

    return RPI

def winning_per(team1_rating, team2_rating):
    """ Calculates the winning percentage for match between team1 and team2.
        Ratings are based on 'power ratings' 
    """
    
    rating_diff = team1_rating - team2_rating
    wp = 1.0/(1+pow(10,(-rating_diff/15.0)))
    return wp

def logloss(y, yhat):
     score = -fsum(map(lambda y, yhat: y*log(yhat) + (1-y)*log(1-yhat), y, yhat))/len(y)     

     Return score

