CREATE VIEW vista_detalle_pedidos AS
SELECT p.id_pedido,c.nombre AS cliente,pr.nombre AS producto,d.cantidad,pr.precio,(d.cantidad * pr.precio) AS total_linea
FROM detalle_pedido d JOIN pedidos p ON d.id_pedido = p.id_pedido JOIN clientes c ON p.id_cliente = c.id_cliente
JOIN productos pr ON d.id_producto = pr.id_producto;

CREATE OR REPLACE PROCEDURE registrar_pedido(id_cliente INTEGER,fecha DATE,id_producto INTEGER,cantidad INTEGER)
LANGUAGE plpgsql AS $$
DECLARE
    pedido INTEGER;
BEGIN
    INSERT INTO pedidos (id_cliente, fecha) VALUES (id_cliente, fecha)
    RETURNING id_pedido INTO pedido;

    INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad) VALUES (pedido, id_producto, cantidad);
END;
$$;

CALL registrar_pedido(1, '2025-05-20', 2, 3);

CREATE OR REPLACE FUNCTION total_gastado_por_cliente(ped_id_cliente INTEGER)
RETURNS NUMERIC(10,2) AS $$
DECLARE
    total INTEGER;
BEGIN
    SELECT COALESCE(SUM(pr.precio * d.cantidad), 0)
    INTO total FROM pedidos p
    JOIN detalle_pedido d ON p.id_pedido = d.id_pedido JOIN productos pr ON d.id_producto = pr.id_producto
    WHERE p.id_cliente = ped_id_cliente;

    RETURN total;
END;
$$ LANGUAGE plpgsql;
CREATE INDEX idx_cliente_producto ON detalle_pedido(id_producto,id_pedido);

CREATE OR REPLACE FUNCTION registrar_auditoria()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO auditoria_pedidos (id_cliente, fecha_pedido)
    VALUES (NEW.id_cliente, NEW.fecha);
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_auditoria_pedido AFTER INSERT ON pedidos
FOR EACH ROW EXECUTE FUNCTION registrar_auditoria();

-- Insertar un nuevo pedido
INSERT INTO pedidos (id_cliente, fecha) VALUES (1, '2025-05-20');

-- Verificar la auditoría
SELECT * FROM auditoria_pedidos;

SELECT nombre,correo,actividad->>'fecha' AS fecha,actividad->>'accion' AS accion
FROM usuarios,jsonb_array_elements(historial_actividad) AS actividad WHERE id = 1;  


SELECT 
    o.nombre AS ORIGEN,d.nombre AS DESTINO,r.distancia_km
FROM rutas r
JOIN ciudades o ON r.id_origen = o.id
JOIN ciudades d ON r.id_destino = d.id
WHERE o.nombre = 'San Luis Potosí';
