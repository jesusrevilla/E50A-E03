import psycopg2
import pytest

def test_total_gastado_por_cliente():
    # Conexión a la base de datos
    conn = psycopg2.connect("dbname=test user=postgres password=secret")
    cur = conn.cursor()
    
    # Ejecutar la función
    cur.execute("SELECT total_gastado_por_cliente(1);")
    result = cur.fetchone()[0]
    
    # Verificar el resultado (ajustar el valor esperado)
    assert result == 2371.00  # Cambia esto con el valor correcto de la suma
    
    cur.close()
    conn.close()
