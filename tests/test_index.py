# -*- coding: utf-8 -*-
import os
import subprocess

import pytest


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
        "-At",
        "-F", "\t",
        "-c", sql,
    ]
    out = subprocess.check_output(cmd, env=env, stderr=subprocess.STDOUT, text=True)
    return [line for line in out.splitlines() if line.strip() != ""]


def psql(sql: str) -> list[str]:
    preferred = os.environ.get("PGDATABASE") or "exercises"
    try:
        return _run_psql(sql, preferred)
    except subprocess.CalledProcessError:
        return _run_psql(sql, "test_db")


def test_index_exists_and_is_composite():
    # “Crea un índice compuesto llamado idx_cliente_producto” (README). :contentReference[oaicite:7]{index=7}
    rows = psql("""
      SELECT tablename, indexname, indexdef
      FROM pg_indexes
      WHERE schemaname='public'
        AND indexname='idx_cliente_producto';
    """)
    assert rows, "No existe el índice idx_cliente_producto"

    # Validar que sea compuesto (que tenga coma dentro de paréntesis)
    _, _, indexdef = rows[0].split("\t", 2)
    inside = indexdef[indexdef.find("(")+1:indexdef.rfind(")")]
    assert "," in inside, f"El índice no parece compuesto: {indexdef}"
