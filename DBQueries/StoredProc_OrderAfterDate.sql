CREATE PROCEDURE OrderAfterDate @OrderDate DATE
AS
BEGIN
	SELECT *
	FROM Orders
	WHERE order_date>@OrderDate
	ORDER BY order_date
END;

EXEC OrderAfterDate '2022-04-30'