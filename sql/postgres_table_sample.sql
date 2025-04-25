DROP TABLE IF EXISTS match_map_player_stats;
DROP TABLE IF EXISTS match_map_overviews;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS players;

CREATE TABLE players (
    id int PRIMARY KEY,
    name VARCHAR(50)
);
CREATE TABLE teams (
    id int PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE events (
    id int PRIMARY KEY,
    title VARCHAR(255) DEFAULT 'No event name',
    description TEXT,
    starting_date DATE NOT NULL,
    ending_date DATE NOT NULL,
    prize_pool NUMERIC(15,2),
    location VARCHAR(255)
);

CREATE TABLE matches (
    id int PRIMARY KEY,
    
    -- Team 1 details
    team1_id INT NOT NULL,
    team1_name VARCHAR(255) DEFAULT 'TEAM 01',
    team1_score NUMERIC(5,2) DEFAULT '0',
    
    -- Team 2 details
    team2_id INT NOT NULL,
    team2_name VARCHAR(255) DEFAULT 'TEAM 02',
    team2_score NUMERIC(5,2) DEFAULT '0',
    
    -- Event details
    match_date text DEFAULT '',
    patch VARCHAR(100),
    note TEXT,
    
    -- Event meta details
    event_name VARCHAR(255) DEFAULT '',
    event_series VARCHAR(255),
    event_id INT
);

CREATE TABLE match_map_overviews (
    id int PRIMARY KEY,
    match_id INT NOT NULL,
    
    -- Team 1 details
    team1_id INT NOT NULL,
    team1_name VARCHAR(255) DEFAULT 'TEAM 01',
    team1_score NUMERIC(5,2) NOT NULL,
    team1_atk_won NUMERIC(5,2) NOT NULL,
    team1_def_won NUMERIC(5,2) NOT NULL,

    -- Team 2 details
    team2_id INT NOT NULL,
    team2_name VARCHAR(255) DEFAULT 'TEAM 02',
    team2_score NUMERIC(5,2) NOT NULL,
    team2_atk_won NUMERIC(5,2) NOT NULL,
    team2_def_won NUMERIC(5,2) NOT NULL,

    -- Map details
    map_name VARCHAR(100) DEFAULT 'MAP',
    team_id_map_pick INT NOT NULL
);

CREATE TABLE match_map_player_stats (
    id SERIAL PRIMARY KEY,
    match_id INT NOT NULL,
    match_map_id INT NOT NULL,
    player_id INT NOT NULL,
    player_name VARCHAR(255) DEFAULT '',
    team_name VARCHAR(255) DEFAULT '',
    agent VARCHAR(100) DEFAULT '',
    
    rating_20 NUMERIC(6,2),
    average_combat_score NUMERIC(6,2),
    kills NUMERIC(6,2) NOT NULL,
    deaths NUMERIC(6,2) NOT NULL,
    assists NUMERIC(6,2) NOT NULL,
    kd_ratio NUMERIC(6,2),
    kill_assists_trade_survival_perc NUMERIC(6,2),
    average_dmg_per_round NUMERIC(10,2),
    headshot_percentages NUMERIC(6,2),
    first_kills NUMERIC(6,2),
    first_deaths NUMERIC(6,2),
    first_kill_deaths_ratio NUMERIC(6,2),
    side VARCHAR(50)

);

ALTER TABLE matches ADD CONSTRAINT fk_event FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE SET NULL;

ALTER TABLE match_map_overviews ADD CONSTRAINT fk_match FOREIGN KEY (match_id) REFERENCES matches(id) ON DELETE CASCADE;

ALTER TABLE match_map_player_stats ADD CONSTRAINT fk_match FOREIGN KEY (match_id) REFERENCES matches(id) ON DELETE CASCADE;

ALTER TABLE matches ADD CONSTRAINT fk_team1 FOREIGN KEY (team1_id) REFERENCES teams(id) ON DELETE SET NULL;
ALTER TABLE matches ADD CONSTRAINT fk_team2 FOREIGN KEY (team2_id) REFERENCES teams(id) ON DELETE SET NULL;

ALTER TABLE match_map_overviews ADD CONSTRAINT fk_team1 FOREIGN KEY (team1_id) REFERENCES teams(id) ON DELETE SET NULL;
ALTER TABLE match_map_overviews ADD CONSTRAINT fk_team2 FOREIGN KEY (team2_id) REFERENCES teams(id) ON DELETE SET NULL;
ALTER TABLE match_map_overviews ADD CONSTRAINT fk_team_map_pick FOREIGN KEY (team_id_map_pick) REFERENCES teams(id) ON DELETE SET NULL;

ALTER TABLE match_map_player_stats ADD CONSTRAINT fk_match_map FOREIGN KEY (match_map_id) REFERENCES match_map_overviews(id) ON DELETE CASCADE;
ALTER TABLE match_map_player_stats ADD CONSTRAINT fk_player_id FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE SET NULL;


-- to disable foreign key constraint if necessary
ALTER TABLE events DISABLE TRIGGER ALL;
ALTER TABLE matches DISABLE TRIGGER ALL;
ALTER TABLE match_map_overviews DISABLE TRIGGER ALL;
ALTER TABLE match_map_player_stats DISABLE TRIGGER ALL;

-- Extract team and players data from map data
INSERT INTO players
SELECT player_id, player_name FROM match_map_player_stats
ON CONFLICT (id) DO NOTHING;

INSERT INTO teams(
    SELECT team1_id, team1_name FROM match_map_overviews
    UNION
    SELECT team2_id, team2_name FROM match_map_overviews
)
ON CONFLICT (id) DO NOTHING;

-- Enable foreign key constraint back
ALTER TABLE events ENABLE TRIGGER ALL;
ALTER TABLE matches ENABLE TRIGGER ALL;
ALTER TABLE match_map_overviews ENABLE TRIGGER ALL;
ALTER TABLE match_map_player_stats ENABLE TRIGGER ALL;

create or replace view major_events as
select * from events where starting_date >= '2021-05-24' and (title like 'Valorant Champions%' or title like '%Masters%' or title like '%LOCK%') order by starting_date desc;

create or replace view major_event_matches as
select m.* from matches m join major_events mjv on m.event_id = mjv.	id;

select player_name, mjr_m.match_id, sum(kills) kills from major_event_matches mjr_m 
	join match_map_overviews ovs on mjr_m.id = ovs.match_id 
	join match_map_player_stats ps on mjr_m.id = ps.match_id 
where player_name != 'Guest' and kills > -1
group by player_name, match_id
order by kills desc;
