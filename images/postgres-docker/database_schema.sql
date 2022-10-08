CREATE TABLE IF NOT EXISTS postgres_db (
    match_id INTEGER PRIMARY KEY,
    home_name VARCHAR,
    away_name VARCHAR,
    location VARCHAR,
    scheduled VARCHAR,
    status VARCHAR,
    home_top_goalscorer_name VARCHAR,
    home_top_goalscorer_goals VARCHAR,
    away_top_goalscorer_name VARCHAR,
    away_top_goalscorer_goals VARCHAR,
    home_yellow_cards VARCHAR,
    away_yellow_cards VARCHAR
);
