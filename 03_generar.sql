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

-- Procedimiento almacenado
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
