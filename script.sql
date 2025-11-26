CREATE VIEW vista_detalle_pedidos AS
SELECT 
    c.nombre AS nombre_cliente,
    p.nombre AS nombre_producto,
    dp.cantidad,
    dp.cantidad * p.precio AS total_linea
FROM detalle_pedido dp
JOIN pedidos ped ON dp.id_pedido = ped.id_pedido
JOIN clientes c ON ped.id_cliente = c.id_cliente
JOIN productos p ON dp.id_producto = p.id_producto;

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
END;
$$;

CREATE OR REPLACE FUNCTION total_gastado_por_cliente(p_id_cliente INT) 
RETURNS DECIMAL(10,2)
LANGUAGE plpgsql
AS $$
DECLARE
    v_total DECIMAL(10,2);
BEGIN
    SELECT SUM(dp.cantidad * p.precio)
    INTO v_total
    FROM detalle_pedido dp
    JOIN productos p ON dp.id_producto = p.id_producto
    JOIN pedidos ped ON dp.id_pedido = ped.id_pedido
    WHERE ped.id_cliente = p_id_cliente;
    
    RETURN COALESCE(v_total, 0); 
END;
$$;

CREATE INDEX idx_cliente_producto ON detalle_pedido(id_pedido, id_producto);

CREATE OR REPLACE FUNCTION registrar_auditoria_pedido()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO auditoria_pedidos (id_cliente, fecha_pedido)
    VALUES (NEW.id_cliente, NEW.fecha);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_auditoria_pedido
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION registrar_auditoria_pedido();

SELECT * FROM productos_json
WHERE atributos ->> 'marca' = 'Dell';

SELECT nombre, correo
FROM usuarios
WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';

SELECT c1.nombre AS origen, c2.nombre AS destino, r.distancia_km
FROM rutas r
JOIN ciudades c1 ON r.id_origen = c1.id
JOIN ciudades c2 ON r.id_destino = c2.id
WHERE c1.nombre = 'San Luis Potosí';
