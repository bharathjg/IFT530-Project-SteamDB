
SELECT Games.game_id, Games.game_name, Genres.indie, Genres.action_, Genres.adventure, Genres.casual, Genres.simulation, Genres.strategy, Genres.rpg, Genres.early_access, Genres.free_to_play, Genres.sports, Genres.racing, Genres.massively_multiplayer
FROM Games
INNER JOIN Genres ON Games.game_id=Genres.game_id