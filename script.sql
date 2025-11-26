
CREATE VIEW vista_detalle_pedidos as
SELECT 
p.id_pedido as pedido,
dp.id_detalle as detalle,
c.nombre as cliente,
ps.nombre as producto,
dp.cantidad,
(dp.cantidad*ps.precio) as total
FROM detalle_pedido dp
JOIN pedidos p on p.id_pedido=dp.id_pedido
JOIN productos ps on ps.id_producto=dp.id_producto
JOIN clientes c on c.id_cliente=p.id_cliente;

CREATE OR REPLACE PROCEDURE registrar_pedido(
  IN id_cliente INT,
  IN fecha DATE,
  IN id_producto INT,
  IN cantidad INT
)
LANGUAGE plpgsql
as $$
DECLARE
   pedido INT;
BEGIN
  INSERT INTO pedidos(id_cliente,fecha)
  VALUES (id_cliente,fecha)
  RETURNING id_pedido INTO pedido;
  INSERT INTO detalle_pedido(id_pedido,id_producto,cantidad)
  VALUES (pedido,id_producto,cantidad);
END;
$$;

CALL registrar_pedido(1, '2025-05-20', 2, 3);
SELECT * FROM pedidos;
SELECT * FROM detalle_pedido;

CREATE OR REPLACE FUNCTION total_gastado_por_cliente(
  cliente INT
)
RETURNS NUMERIC
AS $$
BEGIN
  return(SELECT 
  sum((dp.cantidad*ps.precio)) as total
  FROM detalle_pedido dp
  JOIN productos ps on ps.id_producto=dp.id_producto
  JOIN pedidos p on p.id_pedido=dp.id_pedido
  WHERE p.id_cliente=cliente);
END;
$$ LANGUAGE plpgsql;

SELECT total_gastado_por_cliente(1);

--CREATE INDEX idx_cliente_producto ON detalle_pedido(id_cliente,id_producto);

CREATE OR REPLACE FUNCTION insertar_auditoria()
RETURNS TRIGGER
AS $$
BEGIN
  INSERT INTO auditoria_pedidos(id_cliente,fecha_pedido)
  VALUES (NEW.id_cliente,NEW.fecha);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_auditoria
AFTER INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION insertar_auditoria();

-- Insertar un nuevo pedido
INSERT INTO pedidos (id_cliente, fecha) VALUES (1, '2025-05-20');

-- Verificar la auditoría
SELECT * FROM auditoria_pedidos;

SELECT * FROM productos_json
WHERE atributos ->> 'marca' = 'Dell';

SELECT nombre, correo
FROM usuarios
WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';

SELECT historial_actividad
FROM usuarios 
WHERE id=1
