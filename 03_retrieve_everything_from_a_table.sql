-- Crear una vista con JOINs (vista_detalle_pedidos) Esta vista muestra el detalle de cada pedido, incluyendo el nombre del cliente, producto, cantidad y el total por línea.
CREATE VIEW vista_detalle_pedidos AS
SELECT 
    p.id_pedido,
    c.nombre AS cliente,
    pr.nombre AS producto,
    dp.cantidad,
    pr.precio,
    (dp.cantidad * pr.precio) AS total_linea,
    p.fecha
FROM detalle_pedido dp
JOIN pedidos p ON dp.id_pedido = p.id_pedido
JOIN clientes c ON p.id_cliente = c.id_cliente
JOIN productos pr ON dp.id_producto = pr.id_producto;

--🔍 Consultar la vista
SELECT * FROM vista_detalle_pedidos;

--Procedimiento almacenado
--🛠️ Registrar un nuevo pedido Este procedimiento llamado registrar_pedido inserta un nuevo pedido y sus detalles en varias tablas.
CREATE OR REPLACE PROCEDURE registrar_pedido(
    p_id_cliente INT,
    p_fecha DATE,
    p_id_producto INT,
    p_cantidad INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    nuevo_pedido_id INT;
BEGIN
    -- 1. Insertar el pedido y obtener su ID
    INSERT INTO pedidos (id_cliente, fecha)
    VALUES (p_id_cliente, p_fecha)
    RETURNING id_pedido INTO nuevo_pedido_id;

    -- 2. Insertar el detalle del pedido
    INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad)
    VALUES (nuevo_pedido_id, p_id_producto, p_cantidad);

    RAISE NOTICE 'Pedido % registrado correctamente.', nuevo_pedido_id;
END $$;

--Ejemplo de uso 
CALL registrar_pedido(1, '2025-05-20', 2, 3);
--Funcion
--Calcular el total gastado por un cliente, esta funcion devuelve el total gastado por un cliente sumando todos sus pedidos 
CREATE OR REPLACE FUNCTION total_gastado_por_cliente(p_id_cliente INT)
RETURNS DECIMAL(10,2)
LANGUAGE plpgsql
AS $$
DECLARE
    total DECIMAL(10,2);
BEGIN
    SELECT 
        COALESCE(SUM(dp.cantidad * pr.precio), 0)
    INTO total
    FROM pedidos p
    JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
    JOIN productos pr ON dp.id_producto = pr.id_producto
    WHERE p.id_cliente = p_id_cliente;

    RETURN total;
END $$;

--Ejemplo de uso 
SELECT total_gastado_por_cliente(1);

--Crear un trigger que registre en una tabla de auditoría cada vez
--que se inserte un nuevo pedido, incluyendo el ID del cliente,
--la fecha del pedido y la fecha y hora del registro.
--fUNCION
CREATE OR REPLACE FUNCTION fn_registrar_auditoria_pedido()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO auditoria_pedidos (id_cliente, fecha_pedido)
    VALUES (NEW.id_cliente, NEW.fecha);

    RETURN NEW;
END $$;

--Trigger
CREATE TRIGGER trg_auditar_pedido
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION fn_registrar_auditoria_pedido();
--Probar el TRIGGER
-- Insertar un nuevo pedido
INSERT INTO pedidos (id_cliente, fecha) VALUES (1, '2025-05-20');

-- Verificar la auditoría
SELECT * FROM auditoria_pedidos;

--NOSQL
--Consultar datos con atributo especifico
SELECT * FROM productos_json
WHERE atributos ->> 'marca' = 'Dell';

--🔍 Consultar usuarios que realizaron una acción específica

SELECT nombre, correo
FROM usuarios
WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';

--🔍 Extraer todas las acciones de un usuario

SELECT 
    (json_element->>'fecha') AS fecha,
    (json_element->>'accion') AS accion
FROM usuarios,
     jsonb_array_elements(historial_actividad) AS json_element
WHERE id = 1;

--6 Grafos 
SELECT 
    c1.nombre AS origen,
    c2.nombre AS destino,
    r.distancia_km
FROM rutas r
JOIN ciudades c1 ON r.id_origen = c1.id
JOIN ciudades c2 ON r.id_destino = c2.id
WHERE c1.nombre = 'San Luis Potosí';


