# -*- coding: utf-8 -*-
import os
import subprocess

import pytest


# Tokens típicos que psql imprime como "command status" y estorban a los asserts
_PSQL_STATUS_TOKENS = {
    "BEGIN", "COMMIT", "ROLLBACK",
    "INSERT", "UPDATE", "DELETE",
    "CALL", "DO",
    "CREATE", "DROP", "ALTER", "TRUNCATE",
    "GRANT", "REVOKE", "SET",
}


def _clean_psql_lines(stdout: str) -> list[str]:
    """
    psql (incluso con -At) puede imprimir:
      - BEGIN / ROLLBACK
      - CALL
      - INSERT 0 1
      - NOTICE/WARNING
    Esta función deja SOLO líneas útiles (resultados de SELECT).
    """
    lines: list[str] = []
    for raw in stdout.splitlines():
        s = raw.strip()
        if not s:
            continue

        # Mensajes
        if s.startswith(("NOTICE:", "WARNING:")):
            continue

        # Status lines (BEGIN, INSERT 0 1, CALL, etc.)
        first = s.split()[0]
        if first in _PSQL_STATUS_TOKENS:
            continue

        lines.append(s)
    return lines


def _run_psql(sql: str, db: str) -> list[str]:
    env = os.environ.copy()
    env.setdefault("PGHOST", "localhost")
    env.setdefault("PGUSER", "postgres")
    env.setdefault("PGPASSWORD", "postgres")

    cmd = [
        "psql",
        "-h", env["PGHOST"],
        "-U", env["PGUSER"],
        "-d", db,
        "-q",          # quiet (reduce banners / extra output)
        "-At",         # unaligned + tuples only (pero aun así salen status lines)
        "-F", "\t",
        "-c", sql,
    ]
    out = subprocess.check_output(cmd, env=env, stderr=subprocess.STDOUT, text=True)
    return _clean_psql_lines(out)


def psql(sql: str) -> list[str]:
    preferred = os.environ.get("PGDATABASE") or "exercises"
    try:
        return _run_psql(sql, preferred)
    except subprocess.CalledProcessError:
        return _run_psql(sql, "test_db")


def test_auditoria_table_exists():
    r = psql("""
      SELECT COUNT(*)
      FROM information_schema.tables
      WHERE table_schema='public' AND table_name='auditoria_pedidos';
    """)
    assert int(r[0]) == 1, "No existe la tabla auditoria_pedidos"


def test_trigger_exists_on_pedidos():
    r = psql("""
      SELECT COUNT(*)
      FROM pg_trigger
      WHERE tgname='trg_auditar_pedido'
        AND NOT tgisinternal;
    """)
    assert int(r[0]) >= 1, "No existe el trigger trg_auditar_pedido"


def test_trigger_inserts_audit_row():
    out = psql("""
      BEGIN;

      SELECT COUNT(*) FROM auditoria_pedidos;

      INSERT INTO pedidos (id_cliente, fecha) VALUES (1, '2025-05-20');

      SELECT COUNT(*) FROM auditoria_pedidos;

      SELECT id_cliente, fecha_pedido
      FROM auditoria_pedidos
      ORDER BY id_auditoria DESC
      LIMIT 1;

      ROLLBACK;
    """)

    assert len(out) >= 3, f"Salida inesperada: {out}"

    before = int(out[0])
    after  = int(out[1])
    assert after == before + 1, "El trigger no insertó registro en auditoria_pedidos"

    last = out[2].split("\t")
    assert int(last[0]) == 1
    assert last[1] == "2025-05-20"
