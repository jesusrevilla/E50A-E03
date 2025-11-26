-- Ejercicio 1
CREATE OR REPLACE VIEW vista_detalle_pedidos AS
SELECT 
    c.nombre AS nombre_cliente,
    p.nombre AS nombre_producto,
    d.cantidad,
    (d.cantidad * p.precio) AS total_por_linea
FROM 
    detalle_pedido d
JOIN 
    pedidos pe ON d.id_pedido = pe.id_pedido
JOIN 
    clientes c ON pe.id_cliente = c.id_cliente
JOIN 
    productos p ON d.id_producto = p.id_producto;

-- Ejercicio 2
CREATE OR REPLACE PROCEDURE registrar_pedido(
    p_id_cliente INT,
    p_fecha DATE,
    p_id_producto INT,
    p_cantidad INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_new_id_pedido INT; 
BEGIN
    
    INSERT INTO pedidos (id_cliente, fecha)
    VALUES (p_id_cliente, p_fecha)
    RETURNING id_pedido INTO v_new_id_pedido;

    INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad)
    VALUES (v_new_id_pedido, p_id_producto, p_cantidad);
    
    RAISE NOTICE 'Pedido registrado con éxito. ID Pedido: %', v_new_id_pedido;
END;
$$;
-- Ejercicio 3
CREATE OR REPLACE FUNCTION total_gastado_por_cliente(p_id_cliente INT)
RETURNS DECIMAL(10, 2)
LANGUAGE plpgsql
AS $$
DECLARE
    v_total DECIMAL(10, 2);
BEGIN
    SELECT COALESCE(SUM(dp.cantidad * prod.precio), 0)
    INTO v_total
    FROM pedidos pe
    JOIN detalle_pedido dp ON pe.id_pedido = dp.id_pedido
    JOIN productos prod ON dp.id_producto = prod.id_producto
    WHERE pe.id_cliente = p_id_cliente;

    RETURN v_total;
END;
$$;

-- Ejercicio 4
CREATE OR REPLACE FUNCTION funcion_auditoria_pedido()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
   
    INSERT INTO auditoria_pedidos (id_cliente, fecha_pedido)
    VALUES (NEW.id_cliente, NEW.fecha);
    
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_registrar_auditoria
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION funcion_auditoria_pedido();

-- Ejercicio 5
SELECT 
    u.nombre, 
    actividad ->> 'fecha' AS fecha, 
    actividad ->> 'accion' AS accion
FROM 
    usuarios u,
    jsonb_array_elements(u.historial_actividad) AS actividad
WHERE 
    u.nombre = 'Laura Gómez';

-- Ejercicio 6
SELECT 
    c1.nombre AS origen,
    c2.nombre AS destino,
    r.distancia_km
FROM 
    rutas r
JOIN 
    ciudades c1 ON r.id_origen = c1.id
JOIN 
    ciudades c2 ON r.id_destino = c2.id
WHERE 
    c1.nombre = 'San Luis Potosí';
