USE Steam

SELECT Genres.game_id, Games.game_name
FROM Genres
INNER JOIN Games ON Games.game_id=Genres.game_id
WHERE action_=1 AND adventure=1

SELECT * FROM Genres