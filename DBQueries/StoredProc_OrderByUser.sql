CREATE PROCEDURE OrderByUser @UserID int
AS
BEGIN
	DECLARE @ordernum int
	SELECT @ordernum = order_id
	FROM Orders
	WHERE customer_id=@UserID

	SELECT OrderDetails.*, Orders.customer_id,Orders.order_id, Orders.order_date
	FROM Orders
	INNER JOIN OrderDetails ON Orders.order_id=OrderDetails.order_id
	WHERE OrderDetails.order_id=@ordernum
END;

EXEC OrderByUser @UserID=213
