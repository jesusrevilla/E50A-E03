from db import run_query

def test_funciones_adicionales():
    result = run_query("SELECT total_gastado_por_cliente(1);")
    assert result[0][0] >= 0
