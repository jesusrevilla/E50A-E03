import pytest
# ... (incluir fixture db_connection) ...

def test_jsonb_query(db_connection):
    """Verifica la consulta de JSONB para encontrar usuarios con una acción específica."""
    cursor = db_connection.cursor()

    # Consulta del examen: Consultar usuarios que realizaron la acción 'inicio_sesion'
    cursor.execute("""
        SELECT nombre 
        FROM usuarios 
        WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';
    """)
    
    results = cursor.fetchall()
    nombres = sorted([r[0] for r in results])
    
    # En los datos de ejemplo, Laura Gómez y Pedro Ruiz tienen 'inicio_sesion'
    expected_names = ['Laura Gómez', 'Pedro Ruiz']
    
    assert nombres == expected_names, "La consulta JSONB no devolvió los usuarios correctos."

    cursor.close()
