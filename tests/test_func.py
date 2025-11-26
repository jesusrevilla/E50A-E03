

import psycopg2
from decimal import Decimal
from .conftest import db_connection

def test_total_gastado_cliente_calculo_correcto():
    conn = db_connection()
    cur = conn.cursor()
    
    # C
    id_cliente_a_probar = 1
    total_esperado = Decimal('1251.00')

    cur.execute("SELECT total_gastado_por_cliente(%s);", (id_cliente_a_probar,))
    total_obtenido = cur.fetchone()[0]

    assert total_obtenido == total_esperado

    cur.close()
    conn.close()

def test_total_gastado_cliente_sin_pedidos():
    conn = db_connection()
    cur = conn.cursor()
    
   
    id_cliente_sin_pedidos = 999 
    total_esperado = Decimal('0.00')

    cur.execute("SELECT total_gastado_por_cliente(%s);", (id_cliente_sin_pedidos,))
    total_obtenido = cur.fetchone()[0]

    assert total_obtenido == total_esperado

    cur.close()
    conn.close()
