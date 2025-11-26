import pytest
import psycopg2
import json

DB_CONFIG = {
    'host': 'localhost',
    'database': 'test_db',
    'user': 'postgres',
    'password': 'postgres',
    'port': 5432
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def test_consulta_json_atributos():
    conn = get_connection()
    try:
        cur = conn.cursor()
        
        datos_json = json.dumps({"marca": "TestBrand", "color": "RojoFuego"})
        cur.execute("INSERT INTO productos_json (nombre, atributos) VALUES (%s, %s)", ('ProductoTest', datos_json))
        conn.commit()
        
        cur.execute("SELECT nombre FROM productos_json WHERE atributos ->> 'color' = 'RojoFuego';")
        resultado = cur.fetchone()
        
        assert resultado is not None
        assert resultado[0] == 'ProductoTest'
        
    finally:
        cur.close()
        conn.close()

def test_usuario_historial_containment():
    conn = get_connection()
    try:
        cur = conn.cursor()
        
        cur.execute("SELECT nombre FROM usuarios WHERE historial_actividad @> '[{\"accion\": \"inicio_sesion\"}]';")
        usuarios_encontrados = cur.fetchall()
        
        nombres = [u[0] for u in usuarios_encontrados]
        assert 'Laura Gómez' in nombres
        
    finally:
        cur.close()
        conn.close()
