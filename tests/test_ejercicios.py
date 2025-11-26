import psycopg2
import pytest
import os

DB_CONFIG = {
    "dbname": "test_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

def run_query(query):
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

def run_sql_file(filepath):
    test_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(test_dir)
    full_path = os.path.join(root_dir, filepath)

    try:
        conn_ext = psycopg2.connect(**DB_CONFIG)
        conn_ext.autocommit = True
        with conn_ext.cursor() as cur_ext:
            cur_ext.execute("CREATE EXTENSION IF NOT EXISTS hstore;")
        conn_ext.close()

        with open(full_path, 'r') as f:
            sql_content = f.read()

        with psycopg2.connect(**DB_CONFIG) as conn_run:
            with conn_run.cursor() as cur_run:
                cur_run.execute(sql_content)

        return True, ""

    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def test_total_gastado_por_cliente_ana():
    result = run_query("SELECT total_gastado_por_cliente(1);")
    assert result[0][0] == 1251.00

def test_vista_detalle_pedidos():
    result = run_query("SELECT cliente, producto, cantidad, total_linea FROM vista_detalle_pedidos WHERE id_pedido = 1;")
    productos = {row[1]: (row[2], float(row[3])) for row in result}
    assert productos["Laptop"] == (1, 1200.00)
    assert productos["Mouse"] == (2, 51.00)

def test_trigger_auditoria():
    run_query("INSERT INTO pedidos (id_cliente, fecha) VALUES (2, '2025-05-25');")
    result = run_query("SELECT id_cliente, fecha_pedido FROM auditoria_pedidos WHERE fecha_pedido = '2025-05-25';")
    assert result[0][0] == 2

sql_exercise_files = [
    "01_create_tables",
    "02_insert_data.sql",
    "03_ejercicios.sql"
]

@pytest.mark.parametrize("filename", sql_exercise_files)
def test_sql_exercise_file_execution(filename):
    success, error_message = run_sql_file(filename)
    assert success, f"El script {filename} falló al ejecutarse:\n{error_message}"
