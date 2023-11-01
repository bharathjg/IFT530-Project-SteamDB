CREATE TRIGGER InsertOnUsers
ON Users
FOR INSERT
AS
BEGIN
	DECLARE @userid int
	DECLARE @username nvarchar(20)
	SELECT @userid=ID, @username=FirstName FROM inserted
	INSERT INTO InsertionRecordsForUsers
	VALUES('New user with ID='+CAST(@userid AS VARCHAR(10))+' and first name '+@username+' has been added to the Users table')
END

SELECT * FROM InsertionRecordsForUsers