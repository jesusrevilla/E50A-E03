import psycopg2
import pytest
import os

def test_total_gastado_por_cliente():
    # Conexión a la base de datos usando las variables de entorno
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "test_db"),  # Nombre de la base de datos
        user=os.getenv("POSTGRES_USER", "postgres"),  # Usuario de PostgreSQL
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),  # Contraseña de PostgreSQL
        host=os.getenv("POSTGRES_HOST", "localhost"),  # Dirección del host
        port=os.getenv("POSTGRES_PORT", "5432")  # Puerto de PostgreSQL
    )
    cur = conn.cursor()

    # Ejecutar la función
    cur.execute("SELECT total_gastado_por_cliente(1);")
    result = cur.fetchone()[0]

    # Verificar el resultado (ajustar el valor esperado)
    assert result == 2371.00  # Cambia esto con el valor correcto de la suma

    cur.close()
    conn.close()
