
import psycopg2
import pytest

def test_producto_json():
    # Conexión a la base de datos
    conn = psycopg2.connect("dbname=test user=postgres password=secret")
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
