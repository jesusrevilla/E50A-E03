import pytest
import psycopg2
import os
import json

# Configuración de conexión
DB_CONFIG = {
    'host': 'localhost',
    'database': 'test_db',
    'user': 'postgres',
    'password': 'postgres',
    'port': 5432
}

def get_connection():
    """Obtener conexión a la base de datos"""
    return psycopg2.connect(**DB_CONFIG)

def test_fn_total_gastado_cliente():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT total_gastado_por_cliente(1);")
    total_gastado = cur.fetchone()[0]
    
    assert float(total_gastado) == 1327.50, f"El total esperado era 1327.50, pero se obtuvo {total_gastado}"

    cur.close()
    conn.close()

