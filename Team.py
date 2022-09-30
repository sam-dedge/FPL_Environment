class Team:

    def __init__(self):
        self.my_team_id = 102341
        self.team_by_id = []
        self.team_by_name = []
        self.balance = 100
        self.team_value = 0

    def print_team(self):
        print(self.team_by_name)
        print(f'Squad: [{self.team_by_name}]')
