class Match:
    
    def __init__(self, _id, team1_id, team1_name, team1_score, team2_id, team2_name, team2_score, date, patch, note, event_name, event_series, event_id=None):
        self._id = _id

        # Team 1 details
        self.team1_id = team1_id
        self.team1_name = team1_name
        self.team1_score = team1_score

        # Team 2 details
        self.team2_id = team2_id
        self.team2_name = team2_name
        self.team2_score = team2_score
        
        # Event details
        self.date = date
        self.patch = patch
        self.note = note

        # Event meta details
        self.event_name = event_name
        self.event_series = event_series
        self.event_id = event_id