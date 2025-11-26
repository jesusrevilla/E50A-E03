import psycopg2
import pytest

def test_grafo_rutas_ciudades():
    conn = None
    try:
        conn = psycopg2.connect(
            dbname='test_db',
            user='postgres',
            password='postgres',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS rutas, ciudades CASCADE;")
        
        cur.execute("""
            CREATE TABLE ciudades (
                id SERIAL PRIMARY KEY,
                nombre TEXT NOT NULL
            );
        """)
        
        cur.execute("""
            CREATE TABLE rutas (
                id_origen INT REFERENCES ciudades(id),
                id_destino INT REFERENCES ciudades(id),
                distancia_km INT,
                PRIMARY KEY (id_origen, id_destino)
            );
        """)

        cur.execute("""
            INSERT INTO ciudades (nombre) VALUES
            ('San Luis Potosí'), 
            ('Querétaro'), 
            ('Guadalajara'), 
            ('Monterrey'), 
            ('CDMX');
        """)

        cur.execute("""
            INSERT INTO rutas (id_origen, id_destino, distancia_km) VALUES
            (1, 2, 180),  -- SLP -> Querétaro
            (2, 3, 350),  -- Querétaro -> GDL
            (1, 5, 410),  -- SLP -> CDMX
            (5, 4, 900),  -- CDMX -> Monterrey
            (3, 4, 700);  -- GDL -> Monterrey
        """)

        cur.execute("""
            SELECT 
                c1.nombre AS origen,
                c2.nombre AS destino,
                r.distancia_km
            FROM 
                rutas r
                JOIN ciudades c1 ON r.id_origen = c1.id
                JOIN ciudades c2 ON r.id_destino = c2.id
            WHERE 
                c1.nombre = 'San Luis Potosí'
            ORDER BY 
                c2.nombre; -- Ordenamos para facilitar la validación
        """)
        
        resultados = cur.fetchall()

        assert len(resultados) == 2, f"Se esperaban 2 rutas desde SLP, se encontraron {len(resultados)}."

        
        ruta_1 = resultados[0] 
        ruta_2 = resultados[1] 
        
        assert ruta_1[0] == 'San Luis Potosí'
        assert ruta_1[1] == 'CDMX'
        assert ruta_1[2] == 410

        assert ruta_2[0] == 'San Luis Potosí'
        assert ruta_2[1] == 'Querétaro'
        assert ruta_2[2] == 180

    finally:
        if conn:
            cur.close()
            conn.close()
