class MatchMapPlayerStats:
    
    def __init__(self, match_id, match_map_id, player_id, player_name, team_name, agent, rating_20, average_combat_score, kills, deaths, assists, kd_ratio, kill_assits_trade_surival_perc, average_dmg_perround, headshot_percentages, first_kills, first_deaths, first_kill_deaths_ratio, side):
        self.match_id = match_id
        self.match_map_id = match_map_id
        self.player_id = player_id
        self.player_name = player_name
        self.team_name = team_name
        self.agent = agent
        self.rating_20 = rating_20
        self.average_combat_score = average_combat_score
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.kd_ratio = kd_ratio
        self.kill_assists_trade_survival_perc = kill_assits_trade_surival_perc
        self.average_dmg_per_round = average_dmg_perround
        self.headshot_percentages = headshot_percentages
        self.first_kills = first_kills
        self.first_deaths = first_deaths
        self.first_kill_deaths_ratio = first_kill_deaths_ratio
        self.side = side
        
        
        
