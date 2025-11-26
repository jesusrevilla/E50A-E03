--------------- 




-------------------------------------------------------------------

SELECT * FROM vista_detalle_pedidos;

CALL registrar_pedido(1, '2025-05-20', 2, 3);

-- Verificar la auditoría
SELECT * FROM auditoria_pedidos;

SELECT total_gastado_por_cliente(1);

SELECT * FROM productos_json
WHERE atributos ->> 'marca' = 'Dell';

SELECT nombre, correo
FROM usuarios
WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';

