CREATE TABLE IF NOT EXISTS daily_game_stats (
    date DATE PRIMARY KEY,
    dau INTEGER NOT NULL,
    successful_players INTEGER NOT NULL,
    failed_players INTEGER NOT NULL
);