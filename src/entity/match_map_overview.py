class MatchMapOverview:
    
    def __init__(self, _id, match_id, team1_id, team1_name, team1_score, team1_atk_won, team1_def_won, team2_id, team2_name, team2_score, team2_atk_won, team2_def_won, map_name):
        self._id = _id
        self.match_id = match_id
        
        # Team 1 details
        self.team1_id = team1_id
        self.team1_name = team1_name
        self.team1_score = team1_score
        self.team1_atk_won = team1_atk_won
        self.team1_def_won = team1_def_won

        # Team 2 details
        self.team2_id = team2_id
        self.team2_name = team2_name
        self.team2_score = team2_score
        self.team2_atk_won = team2_atk_won
        self.team2_def_won = team2_def_won
        
        # Map
        self.map_name = map_name
        
        
