from Game import Player
import pandas as pd

class MyTeam:
    def __init__(self):
        self.my_team_id = 102341
        self.team_list_by_id = []
        self.team_list_by_name = []
        self.team_list_types = []
        self.team_list_teams = []
        self.team_gk_by_id = []
        self.team_def_by_id = []
        self.team_mid_by_id = []
        self.team_fwd_by_id = []
        self.balance = 1000
        self.team_value = 0

    def print_team(self):
        squad_dict = {'name': self.team_list_by_name, 'id':self.team_list_by_id, 'pos':self.team_list_types}
        squad = pd.DataFrame(squad_dict)
        print(squad)

    def select_Player(self, identifier):
        player = Player(identifier)
        plyr = player.player
        
        if (plyr is not None) and (player.check_squad_position_rule(self)) and (player.check_team_rule(self)) and (player.check_not_selected_before(self)) and (player.check_balance_rule(self)):
            self.team_list_by_name.append(plyr['web_name'].iloc[0])
            self.team_list_by_id.append(plyr['id'].iloc[0])
            self.team_list_types.append(plyr['element_type'].iloc[0])
            self.team_list_teams.append(plyr['team'].iloc[0])
            self.balance = self.balance - plyr['now_cost'].iloc[0]

        
        #print('Function ENd', self.team_list_by_name)
