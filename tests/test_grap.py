import pytest
from conftest import db_cursor

class TestGrafo:
    def test_ciudades_inserted(self, db_cursor):
        """Prueba que los nodos (ciudades) se hayan insertado."""
        db_cursor.execute("SELECT COUNT(*) FROM ciudades;")
        count = db_cursor.fetchone()[0]
        assert count == 5, "Faltan ciudades insertadas."

    def test_rutas_inserted(self, db_cursor):
        """Prueba que las aristas (rutas) se hayan insertado."""
        db_cursor.execute("SELECT COUNT(*) FROM rutas;")
        count = db_cursor.fetchone()[0]
        assert count == 5, "Faltan rutas insertadas."

    def test_get_rutas_desde_ciudad(self, db_cursor):
        """Prueba la consulta para ver todas las rutas desde San Luis Potosí."""
        db_cursor.execute("SELECT destino, distancia_km FROM get_rutas_desde_ciudad('San Luis Potosí');")
        rutas = db_cursor.fetchall()
        
        expected_rutas = [
            ('Querétaro', 180),
            ('CDMX', 410)
        ]
        
        assert len(rutas) == 2, "Debe haber 2 rutas desde San Luis Potosí."
        # Convertir a set para ignorar el orden
        assert set(rutas) == set(expected_rutas), "Las rutas o distancias desde SLP son incorrectas."
