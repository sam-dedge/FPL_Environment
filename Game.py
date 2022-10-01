from re import L
import requests
import pandas as pd
#import numpy as np

def getALLPlayers():
    # Get page at endpoint bottstrap-static
        url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
        r = requests.get(url)
        json = r.json()
        elements_df = pd.DataFrame(json['elements'])
        element_types_df = pd.DataFrame(json['element_types'])
        return elements_df, element_types_df

class Matches:
    def __init__(self):
        # Get page at endpoint bottstrap-static
        url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
        r = requests.get(url)
        
        # Converting page request to json and forming data frame of teams
        json = r.json()
        teams_df = pd.DataFrame(json['teams'])
        self.teams_df = teams_df

        # Get page at endpoint fixtures with only future fixture list asked 
        url = 'https://fantasy.premierleague.com/api/fixtures?future=1'
        r = requests.get(url)

        #Converting page request to json and forming data frame of fixtures
        fixtures_json = r.json()
        fixtures_df = pd.DataFrame(fixtures_json)
        self.fixtures_df = fixtures_df
        
    def make_fixture_list(self, till_gw = 38):
        # Getting Team names and Ids to join with fixtures
        teams_df = self.teams_df.loc[:,['id', 'name']]
        
        # No. of columns in teams_df and fixtures_df
        #print(len(teams_df.columns.to_list()), len(fixtures_df.columns.to_list()))

        # Rearranging Home team to the left and Away team to the right
        fixtures_df = self.fixtures_df
        cols = fixtures_df.columns.tolist()
        cols = cols[:9] + cols[11:13] + cols[9:11] + cols[13:]
        fixtures_df = fixtures_df.reindex(columns=cols)

        # Left Join on Away ids in fixtures_df and ids in teams_df
        fix = pd.merge(fixtures_df, teams_df, left_on='team_a', right_on='id', how='left').drop('id_y', axis=1)
        fix.rename(columns={'name':'away_name', 'id_x':'id'}, inplace=True)
        
        # Left Join on Home ids in fixtures_df and ids in teams_df
        fix = pd.merge(fix, teams_df, left_on='team_h', right_on='id', how='left').drop('id_y', axis=1)
        fix.rename(columns={'name':'home_name', 'id_x':'id'}, inplace=True)
        
        # Rearranging team names along team ids and scores
        cols = fix.columns.tolist()
        cols = cols[:10] + cols[-1:] + cols[10:11] + cols[12:13] + cols[-2:-1] + cols[11:12] + cols[13:-2]
        fix = fix.reindex(columns=cols)

        # Print column and column length to ensure integrity
        #print(cols)
        #print(len(cols))

        # Return Fixtures untill a certain Gameweek
        # Default till_gw is 38 giving all remaining fixtures
        fix = fix.loc[fix['event'] <= till_gw]
        return fix


class Player():
    
    player_types = getALLPlayers()

    def __init__(self, identifier):
        self.identifier = identifier
        self.player = self.get_Player_by_identifier()

    def get_general_player_info(self):
        return Player.player_types

    def get_Player_by_identifier(self):
        elements, _ = self.get_general_player_info()
        #print('Here2', elements.columns)
        #print(elements.loc[elements['id']==self.identifier])
        #print(type(self.identifier))
        if type(self.identifier) == int:
            if len(elements.loc[elements['id']==self.identifier]) != 1:
                print('Player Not found. Check your identifier')
                return         
            else:
                return elements.loc[elements['id']==self.identifier]
        elif type(self.identifier) == str:
            #print('HERE', self.identifier)
            if len(elements.loc[elements['second_name']==self.identifier]) == 1:
                return elements.loc[elements['second_name']==self.identifier]
            elif len(elements.loc[elements['web_name']==self.identifier]) == 1:
                return elements.loc[elements['web_name']==self.identifier]
            elif len(elements.loc[elements['first_name']==self.identifier]) == 1:
                return elements.loc[elements['first_name']==self.identifier]
            else:
                print('Player Not found. Check your identifier')
                return

    def check_squad_position_rule(self, myTeamObj):
        plyr = self.player
        #print('Here', plyr)
        
        #############################
        #### Position Rules ####
        #############################
        if  plyr is not None:
            if plyr['element_type'].iloc[0] == 1:
                if len(myTeamObj.team_gk_by_id) < 2:
                    myTeamObj.team_gk_by_id.append(plyr['id'].iloc[0])
                else:
                    print(f'Cannot Add GK. You already have {len(myTeamObj.team_gk_by_id)} Gks.')
                    return False
            elif plyr['element_type'].iloc[0] == 2:
                if len(myTeamObj.team_def_by_id) < 5:
                    myTeamObj.team_def_by_id.append(plyr['id'].iloc[0])
                else:
                    print(f'Cannot Add Def. You already have {len(myTeamObj.team_def_by_id)} Defenders.')
                    return False
            elif plyr['element_type'].iloc[0] == 3:
                if len(myTeamObj.team_mid_by_id) < 5:
                    myTeamObj.team_mid_by_id.append(plyr['id'].iloc[0])
                else:
                    print(f'Cannot Add Mid. You already have {len(myTeamObj.team_mid_by_id)} Midfielders.')
                    return False
            elif plyr['element_type'].iloc[0] == 4:
                if len(myTeamObj.team_fwd_by_id) < 3:
                    myTeamObj.team_fwd_by_id.append(plyr['id'].iloc[0])
                else:
                    print(f'Cannot Add Fwd. You already have {len(myTeamObj.team_fwd_by_id)} Forwards.')
                    return False
            else:
                print('Player Element Type Not Found')
                return False
        else:
            print('Wrong Identifier')
            return False
        
        return True

    def check_team_rule(self, myTeamObj):
        plyr = self.player
        #############################
        #### Team Rules ####
        #############################
        if  plyr is not None:
            team = plyr['team'].iloc[0]
            count = myTeamObj.team_list_teams.count(team)
            if count >= 3:
                print('You cannot have more than 3 players of the same team')
                return False
            else:
                return True
        else:
            return False

    def check_not_selected_before(self, myTeamObj):
        plyr = self.player
        #################################
        #### Already Selected Rules ####
        #################################
        if plyr is not None:
            pl_id = plyr['id'].iloc[0]
            if pl_id not in myTeamObj.team_list_by_id:
                return True
            else:
                print('Player already Selected')
                return False
        else:
            print('Player was None')
            return False

    def check_balance_rule(self, myTeamObj):
        plyr = self.player
        #################################
        #### Check Sufficient Funds ####
        #################################
        if myTeamObj.balance < plyr['now_cost'].iloc[0]:
            print('You do not have Sufficient Funds')
            return False
        else:
            return True
