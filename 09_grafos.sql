-- Ver rutas desde San Luis Potosí (id = 1)
SELECT 
    c1.nombre AS origen,
    c2.nombre AS destino,
    r.distancia_km
FROM rutas r
JOIN ciudades c1 ON r.id_origen = c1.id
JOIN ciudades c2 ON r.id_destino = c2.id
WHERE r.id_origen = 1;
