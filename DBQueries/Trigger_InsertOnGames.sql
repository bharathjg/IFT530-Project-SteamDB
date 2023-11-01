CREATE TRIGGER InsertOnGames
ON Games
FOR INSERT
AS
BEGIN
	DECLARE @gameid int
	SELECT @gameid=game_id FROM inserted
	INSERT INTO InsertionRecordsForGames
	VALUES('New game with game_id='+CAST(@gameid AS VARCHAR(10))+' has been added to the Games table')
END

SELECT * FROM InsertionRecordsForGames
