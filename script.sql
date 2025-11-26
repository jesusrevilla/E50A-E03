-- Consultar el total gastado por cada cliente usando la función
SELECT id_cliente, total_gastado_por_cliente(id_cliente) AS total_gastado
FROM clientes;

-- Verificar las rutas entre ciudades
SELECT id_origen, id_destino, distancia_km
FROM rutas
WHERE id_origen = 1;  -- Ver rutas desde San Luis Potosí


