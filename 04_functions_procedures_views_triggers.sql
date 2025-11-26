-- =====================================
-- Función: total_gastado_por_cliente
-- =====================================
CREATE OR REPLACE FUNCTION total_gastado_por_cliente(p_id_cliente INT)
RETURNS NUMERIC AS $$
DECLARE
    total NUMERIC;
BEGIN
    SELECT SUM(dp.cantidad * pr.precio)
    INTO total
    FROM pedidos pe
    JOIN detalle_pedido dp ON dp.id_pedido = pe.id_pedido
    JOIN productos pr ON pr.id_producto = dp.id_producto
    WHERE pe.id_cliente = p_id_cliente;

    RETURN COALESCE(total,0);
END;
$$ LANGUAGE plpgsql;

-- =====================================
-- Procedimiento: registrar_pedido
-- =====================================
CREATE OR REPLACE PROCEDURE registrar_pedido(
    p_id_cliente INT,
    p_fecha DATE,
    p_id_producto INT,
    p_cantidad INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    nuevo_id INT;
BEGIN
    INSERT INTO pedidos(id_cliente, fecha)
    VALUES (p_id_cliente, p_fecha)
    RETURNING id_pedido INTO nuevo_id;

    INSERT INTO detalle_pedido(id_pedido, id_producto, cantidad)
    VALUES (nuevo_id, p_id_producto, p_cantidad);
END;
$$;

-- =====================================
-- Vista: vista_detalle_pedidos
-- =====================================
CREATE OR REPLACE VIEW vista_detalle_pedidos AS
SELECT
    pe.id_pedido,
    cl.nombre AS cliente,
    pr.nombre AS producto,
    dp.cantidad,
    (dp.cantidad*pr.precio) AS total_linea
FROM pedidos pe
JOIN clientes cl ON cl.id_cliente = pe.id_cliente
JOIN detalle_pedido dp ON dp.id_pedido = pe.id_pedido
JOIN productos pr ON pr.id_producto = dp.id_producto;

-- =====================================
-- Tabla de auditoría y trigger
-- =====================================
CREATE TABLE IF NOT EXISTS auditoria_pedidos (
    id_auditoria SERIAL PRIMARY KEY,
    id_cliente INT,
    fecha_pedido DATE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION fn_auditoria_pedidos()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO auditoria_pedidos(id_cliente, fecha_pedido)
    VALUES (NEW.id_cliente, NEW.fecha);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_auditoria_pedidos
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION fn_auditoria_pedidos();

-- =====================================
-- Índice compuesto
-- =====================================
CREATE INDEX IF NOT EXISTS idx_cliente_producto
ON detalle_pedido(id_pedido, id_producto);
