
import pytest

def test_jsonb_query(db_connection):
    """Verifica la consulta de JSONB para encontrar usuarios con una acción específica."""
    cursor = db_connection.cursor()

    cursor.execute("""
        SELECT nombre 
        FROM usuarios 
        WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';
    """)

    results = cursor.fetchall()
    nombres = sorted([r[0] for r in results])


    expected_names = ['Laura Gómez', 'Pedro Ruiz']

    assert nombres == expected_names, "La consulta JSONB no devolvió los usuarios correctos."

    cursor.close()
