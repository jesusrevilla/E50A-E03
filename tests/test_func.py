from app.db import run_query


def test_funciones_adicionales():
    # Puedes poner aquí pruebas de otras funciones si existieran
    result = run_query("SELECT total_gastado_por_cliente(1);")
    assert result[0][0] >= 0

