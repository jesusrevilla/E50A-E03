import psycopg2
import pytest

def test_jsonb_arrays_scenarios():
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

        cur.execute("DROP TABLE IF EXISTS usuarios_log CASCADE;")
        cur.execute("""
            CREATE TABLE usuarios_log (
                id_usuario SERIAL PRIMARY KEY,
                nombre TEXT,
                historial_actividad JSONB
            );
        """)
        cur.execute("""
            INSERT INTO usuarios_log (nombre, historial_actividad) VALUES
            ('Carlos Ruiz', '[
                {"accion": "login", "fecha": "2025-05-20 09:00:00"},
                {"accion": "ver_producto", "producto_id": 105, "fecha": "2025-05-20 09:05:00"}
            ]'),
            ('Sofia Lopez', '[
                {"accion": "login", "fecha": "2025-05-21 10:00:00"},
                {"accion": "compra", "monto": 150.00, "fecha": "2025-05-21 10:30:00"},
                {"accion": "logout", "fecha": "2025-05-21 10:35:00"}
            ]');
        """)

        cur.execute("""
            SELECT nombre 
            FROM usuarios_log 
            WHERE historial_actividad @> '[{"accion": "compra"}]';
        """)
        resultado_log = cur.fetchall()
        nombres_compradores = [fila[0] for fila in resultado_log]

        assert 'Sofia Lopez' in nombres_compradores
        assert 'Carlos Ruiz' not in nombres_compradores
        assert len(nombres_compradores) == 1


        cur.execute("DROP TABLE IF EXISTS usuarios CASCADE;")
        cur.execute("""
            CREATE TABLE usuarios (
                id SERIAL PRIMARY KEY,
                nombre TEXT,
                correo TEXT,
                historial_actividad JSONB
            );
        """)

        cur.execute("""
            INSERT INTO usuarios (nombre, correo, historial_actividad) VALUES
            ('Laura Gómez', 'laura@example.com', '[
                {"fecha": "2025-05-01", "accion": "inicio_sesion"},
                {"fecha": "2025-05-02", "accion": "subio_archivo"},
                {"fecha": "2025-05-03", "accion": "cerró_sesion"}
            ]'),
            ('Pedro Ruiz', 'pedro@example.com', '[
                {"fecha": "2025-05-01", "accion": "inicio_sesion"},
                {"fecha": "2025-05-04", "accion": "comentó_publicación"}
            ]');
        """)

        cur.execute("""
            SELECT nombre, correo
            FROM usuarios
            WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';
        """)
        resultados_sesion = cur.fetchall()
        nombres_sesion = [fila[0] for fila in resultados_sesion]

        assert 'Laura Gómez' in nombres_sesion
        assert 'Pedro Ruiz' in nombres_sesion
        assert len(nombres_sesion) == 2

        cur.execute("""
            SELECT 
                nombre,
                elemento->>'fecha' AS fecha,
                elemento->>'accion' AS actividad
            FROM 
                usuarios,
                jsonb_array_elements(historial_actividad) AS elemento
            WHERE 
                nombre = 'Laura Gómez';
        """)
        desglose_laura = cur.fetchall()

        assert len(desglose_laura) == 3
        
        acciones_encontradas = [fila[2] for fila in desglose_laura] 
        assert 'inicio_sesion' in acciones_encontradas
        assert 'subio_archivo' in acciones_encontradas
        assert 'cerró_sesion' in acciones_encontradas

    finally:
        if conn:
            cur.close()
            conn.close()
