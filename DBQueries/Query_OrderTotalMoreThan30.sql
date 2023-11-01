USE Steam

SELECT game_id FROM Games AS counter_strike WHERE game_name='Counter_Strike'

DECLARE @gamevar int
SELECT @gamevar=0

SELECT @gamevar=[game_id]
FROM Games
WHERE game_name='Runes of Avalon - Path of Magic'

--SELECT @gamevar AS GV

SELECT OrderDetails.order_id, Orders.order_date
FROM OrderDetails
INNER JOIN Orders ON OrderDetails.order_id=Orders.order_id
WHERE OrderDetails.game_id=@gamevar AND Orders.order_date>'2022-06-30'

SELECT OrderDetails.game_id, Games.game_name
FROM OrderDetails
INNER JOIN Games ON OrderDetails.game_id=Games.game_id

SELECT OrderDetails.game_id, count(game_id) AS ct
FROM OrderDetails
GROUP BY game_id
ORDER BY ct DESC

SELECT game_name
FROM Games
WHERE game_id=858340

SELECT OrderDetails.game_id, OrderDetails.order_id, Orders.order_date
FROM OrderDetails
INNER JOIN Orders ON OrderDetails.order_id=Orders.order_id WHERE OrderDetails.game_id=637110

SELECT 