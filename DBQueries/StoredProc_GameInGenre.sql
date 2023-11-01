CREATE PROCEDURE GameInGenre @Genre NVARCHAR(20)
AS
BEGIN
	DECLARE @statement NVARCHAR(max)
	SET @statement='SELECT Genres.game_id, Games.game_name FROM Genres INNER JOIN Games ON Games.game_id=Genres.game_id WHERE '+@Genre+'=1'
	EXEC (@statement)
END;

EXEC GameInGenre 'adventure'