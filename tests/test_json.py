import psycopg2
import pytest
import os

def test_producto_json():
    # Conexión a la base de datos usando las variables de entorno
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "test_db"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )
    cur = conn.cursor()

    # Ejecutar consulta de producto con marca 'Dell'
    cur.execute("""
        SELECT * FROM productos_json
        WHERE atributos ->> 'marca' = 'Dell';
    """)
    result = cur.fetchall()

    # Verificar que se haya encontrado el producto correcto
    assert result == [('Laptop', '{"marca": "Dell", "ram": "16GB", "procesador": "Intel i7"}')]

    cur.close()
    conn.close()
