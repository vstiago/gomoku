CREATE TABLE IF NOT EXISTS players (
	player_id INTEGER PRIMARY KEY,
   	email TEXT NOT NULL UNIQUE,
    code TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tournaments (
  tournament_id INTEGER PRIMARY KEY,
  board_size INTEGER,
  score_board TEXT NOT NULL,
  matches_board TEXT NOT NULL,
);

CREATE TABLE IF NOT EXISTS matches (
    id_player_one INTEGER,
    id_player_two INTEGER,
    tournament_id INTEGER,
    winner INTEGER,
    log TEXT,

    PRIMARY KEY (id_player_one, id_player_two, tournament_id),

    FOREIGN KEY (id_player_one)
      REFERENCES players (player_id)
         ON DELETE CASCADE
         ON UPDATE NO ACTION,

    FOREIGN KEY (id_player_two)
      REFERENCES players (player_id)
         ON DELETE CASCADE
         ON UPDATE NO ACTION
);

