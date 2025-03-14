-- 1. Listar los usuarios que cumplan años el día de hoy cuya cantidad de ventas realizadas en enero 2020 sea superior a 1500.
SELECT 
    c.id -- Customer ID
    ,c.first_name -- Customer First Name
    ,c.last_name -- Customer Last Name
    ,COUNT(o.id) AS total_sales -- Total Sales
FROM 
    db_marketplace.Customer c
INNER JOIN -- Inner Join para obtener los datos de los clientes que cumplan años el día de hoy
    db_marketplace.Order o 
ON 
    c.id = o.customer_id
WHERE 
    MONTH(c.birth_date) = MONTH(CURDATE()) -- Mes de nacimiento igual al mes actual
    AND DAY(c.birth_date) = DAY(CURDATE()) -- Día de nacimiento igual al día actual
    AND MONTH(o.purchase_date) = 1 -- Mes de compra igual a enero
    AND YEAR(o.purchase_date) = 2020 -- Año de compra igual a 2020
GROUP BY c.id, c.first_name, c.last_name -- Agrupar por ID, Nombre y Apellido del cliente
HAVING COUNT(o.id) > 1500; -- Filtrar por clientes con más de 1500 ventas en enero 2020


-- 2. Por cada mes del 2020, se solicita el top 5 de usuarios que más vendieron($) en la categoría Celulares. Se requiere el mes y año de análisis, nombre y apellido del vendedor, cantidad de ventas realizadas, cantidad de productos vendidos y el monto total transaccionado. 
SELECT 
    month
    ,year
    ,first_name
    ,last_name
    ,total_sales
    ,total_products_sold
    ,total_revenue
FROM (
    SELECT 
        MONTH(o.purchase_date) AS month -- Mes de la compra
        ,YEAR(o.purchase_date) AS year -- Año de la compra
        ,c.first_name -- Nombre del cliente
        ,c.last_name -- Apellido del cliente
        ,COUNT(o.id) AS total_sales -- Total de ventas realizadas
        ,SUM(o.quantity) AS total_products_sold -- Total de productos vendidos
        ,SUM(o.total) AS total_revenue -- Monto total transaccionado
        ,ROW_NUMBER() OVER (PARTITION BY YEAR(o.purchase_date), MONTH(o.purchase_date) ORDER BY SUM(o.total) DESC) AS rn -- Ranking de ventas por mes y año
    -- Join de las tablas Order, Item, Category y Customer para obtener los datos requeridos
    FROM db_marketplace.Order o 
    JOIN db_marketplace.Item i ON o.item_id = i.id
    JOIN db_marketplace.Category cat ON i.category_id = cat.id
    JOIN db_marketplace.Customer c ON o.customer_id = c.id
    WHERE 
        YEAR(o.purchase_date) = 2020 -- Compras realizadas en el año 2020
        AND cat.name = 'Celulares' -- Categoría de los ítems es Celulares
    GROUP BY year, month, c.first_name, c.last_name -- Agrupar por año, mes, nombre y apellido del cliente
) ranked
WHERE rn <= 5 -- Filtrar los 5 primeros vendedores por mes y año
ORDER BY year, month, total_revenue DESC; -- Ordenar por año, mes y monto total transaccionado en orden descendente


-- 3. Se solicita poblar una nueva tabla con el precio y estado de los Ítems a fin del día. Tener en cuenta que debe ser reprocesable. Vale resaltar que en la tabla Item, vamos a tener únicamente el último estado informado por la PK definida. (Se puede resolver a través de StoredProcedure) 
CREATE TABLE IF NOT EXISTS db_marketplace.ItemStatus (
    execution_id BIGINT PRIMARY KEY, -- ID de ejecución
    item_id BIGINT, -- ID del ítem
    price FLOAT, -- Precio del ítem
    status INT, -- Estado del ítem
    execution_date TIMESTAMP, -- Fecha de ejecución
    FOREIGN KEY (item_id) REFERENCES db_marketplace.Item(id) -- Llave foránea a la tabla Item
);

CREATE PROCEDURE CaptureItemStatus() -- Procedimiento almacenado para capturar el estado de los ítems
BEGIN
    INSERT INTO db_marketplace.ItemStatus (item_id, price, status, execution_date) -- Insertar datos en la tabla ItemStatus
    SELECT id, price, status, CURRENT_TIMESTAMP -- Seleccionar ID, precio, estado y fecha actual
    FROM db_marketplace.Item; -- Tabla de ítems
END;

-- Llamada diaria para capturar el estado de los ítems
CALL CaptureItemStatus();