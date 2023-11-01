DECLARE @gamevar int
SELECT @gamevar=0

SELECT @gamevar=[game_id]
FROM Games
WHERE game_name='Runes of Avalon - Path of Magic'

--Selecting all orders of the particular game
SELECT OrderDetails.order_id, Orders.order_date
FROM OrderDetails
INNER JOIN Orders ON OrderDetails.order_id=Orders.order_id
WHERE OrderDetails.game_id=@gamevar

--Selecting all orders of the particular game after June 2022
SELECT OrderDetails.order_id, Orders.order_date
FROM OrderDetails
INNER JOIN Orders ON OrderDetails.order_id=Orders.order_id
WHERE OrderDetails.game_id=@gamevar AND Orders.order_date>'2022-06-30'