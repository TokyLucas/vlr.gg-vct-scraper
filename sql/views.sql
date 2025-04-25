-- Stats per agent per map
select mm_pl.player_name, map_name, agent,
avg(average_combat_score) acs, sum(kills) kills, sum(deaths) deaths, sum(assists) assists
from major_event_matches mm
	join major_events me on mm.event_id = me.id
	join match_map_overviews mm_ov on mm.id = mm_ov.match_id
	join match_map_player_stats mm_pl on mm_ov.id = mm_pl.match_map_id
where mm_pl.kills > -1
group by player_name, map_name, agent
order by kills desc;

-- Agent pick per map
select map_name, agent, count(mm_pl.agent) c_agent, sum(team1_atk_won + team2_atk_won) atk_won, sum((12 - team1_atk_won) + (12 - team2_atk_won)) atk_lost, sum(team1_def_won + team2_def_won) def_won 
from major_event_matches mm
	join major_events me on mm.event_id = me.id
	join match_map_overviews mm_ov on mm.id = mm_ov.match_id
	join match_map_player_stats mm_pl on mm_ov.id = mm_pl.match_map_id
where mm_pl.kills > -1
group by map_name, agent
order by map_name asc, c_agent desc;

-- 