import pytest
from conftest import db_cursor, db_connection

class TestTrigger:
    def test_auditoria_on_new_pedido_insert(self, db_cursor, db_connection):
        """Prueba que el trigger registre un nuevo pedido en 'auditoria_pedidos'."""
        
        # 1. Conteo inicial de auditoría
        db_cursor.execute("SELECT COUNT(*) FROM auditoria_pedidos;")
        initial_audit_count = db_cursor.fetchone()[0]
        
        new_client_id = 2 # Luis Pérez
        new_date = '2025-11-20'

        # 2. Insertar un nuevo pedido (esto dispara el trigger)
        db_cursor.execute(f"INSERT INTO pedidos (id_cliente, fecha) VALUES ({new_client_id}, '{new_date}');")
        db_connection.commit()

        # 3. Conteo final de auditoría
        db_cursor.execute("SELECT COUNT(*) FROM auditoria_pedidos;")
        final_audit_count = db_cursor.fetchone()[0]
        
        assert final_audit_count == initial_audit_count + 1, "El trigger no insertó el registro de auditoría."
        
        # 4. Verificar el contenido del registro de auditoría
        db_cursor.execute(
            "SELECT id_cliente, fecha_pedido FROM auditoria_pedidos ORDER BY id_auditoria DESC LIMIT 1;"
        )
        auditoria_registro = db_cursor.fetchone()
        
        assert auditoria_registro[0] == new_client_id, "El id_cliente en auditoría es incorrecto."
        # psycopg2 devuelve objetos date, por eso lo convertimos a string para comparar
        assert str(auditoria_registro[1]) == new_date, "La fecha_pedido en auditoría es incorrecta."
