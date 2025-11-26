-- Vista
CREATE OR REPLACE VIEW vista_detalle_pedidos AS
SELECT 
    c.nombre AS nombre_cliente,
    p.nombre AS nombre_producto,
    dp.cantidad,
    p.precio AS precio_unitario,
    (dp.cantidad * p.precio) AS total_linea,
    pe.fecha AS fecha_compra
FROM 
    detalle_pedido dp
    JOIN pedidos pe ON dp.id_pedido = pe.id_pedido
    JOIN clientes c ON pe.id_cliente = c.id_cliente
    JOIN productos p ON dp.id_producto = p.id_producto;
    
SELECT * FROM vista_detalle_pedidos;

CREATE OR REPLACE PROCEDURE registrar_pedido(
    p_id_cliente INT,
    p_fecha DATE,
    p_id_producto INT,
    p_cantidad INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id_pedido INT;
BEGIN
    INSERT INTO pedidos (id_cliente, fecha)
    VALUES (p_id_cliente, p_fecha)
    RETURNING id_pedido INTO v_id_pedido;

    INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad)
    VALUES (v_id_pedido, p_id_producto, p_cantidad);
    
    RAISE NOTICE 'Pedido registrado correctamente';
END;
$$;

CALL registrar_pedido(1, '2025-05-20', 2, 3);

CREATE OR REPLACE FUNCTION total_gastado_por_cliente(p_id_cliente INT)
RETURNS DECIMAL(10, 2)
LANGUAGE plpgsql
AS $$
DECLARE
    v_total DECIMAL(10, 2);
BEGIN
    SELECT COALESCE(SUM(dp.cantidad * pr.precio), 0)
    INTO v_total
    FROM pedidos pe
    JOIN detalle_pedido dp ON pe.id_pedido = dp.id_pedido
    JOIN productos pr ON dp.id_producto = pr.id_producto
    WHERE pe.id_cliente = p_id_cliente;

    RETURN v_total;
END;
$$;

SELECT total_gastado_por_cliente(1);

-- Indice
CREATE INDEX idx_cliente_producto ON detalle_pedido (id_pedido, id_producto);

-- Funcion Trigger
CREATE OR REPLACE FUNCTION fn_auditoria_pedido()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO auditoria_pedidos (id_cliente, fecha_pedido, fecha_registro)
    VALUES (NEW.id_cliente, NEW.fecha, NOW());

    RETURN NEW;
END;
$$;

-- trigger
CREATE TRIGGER trg_registrar_auditoria
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION fn_auditoria_pedido();

-- Insertar un nuevo pedido
INSERT INTO pedidos (id_cliente, fecha) VALUES (1, '2025-05-20');

-- Verificar la auditoría
SELECT * FROM auditoria_pedidos;

SELECT * FROM productos_json
WHERE atributos ->> 'marca' = 'Dell';

SELECT nombre, correo
FROM usuarios
WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';

-- Extraer todas las acciones de un usuario
SELECT 
    nombre, 
    elemento_historial ->> 'fecha' AS fecha,
    elemento_historial ->> 'accion' AS accion
FROM 
    usuarios,
    jsonb_array_elements(historial_actividad) AS elemento_historial
WHERE 
    nombre = 'Laura Gómez';

-- Ver todas las rutas desde San Luis Potosí
SELECT 
    c_origen.nombre AS origen,
    c_destino.nombre AS destino,
    r.distancia_km
FROM 
    rutas r
JOIN 
    ciudades c_origen ON r.id_origen = c_origen.id
JOIN 
    ciudades c_destino ON r.id_destino = c_destino.id
WHERE 
    c_origen.nombre = 'San Luis Potosí';
