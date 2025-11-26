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
    # intenta exercises y luego test_db (por workflow)
    preferred = os.environ.get("PGDATABASE") or "exercises"
    try:
        return _run_psql(sql, preferred)
    except subprocess.CalledProcessError:
        return _run_psql(sql, "test_db")


def test_view_exists_and_columns():
    # Debe existir la vista vista_detalle_pedidos (README). :contentReference[oaicite:1]{index=1}
    cols = psql("""
      SELECT column_name
      FROM information_schema.columns
      WHERE table_schema='public'
        AND table_name='vista_detalle_pedidos'
      ORDER BY ordinal_position;
    """)

    assert cols, "No existe la vista vista_detalle_pedidos"

    expected = ["id_pedido", "cliente", "producto", "cantidad", "total_linea", "fecha"]
    assert [c.strip() for c in cols] == expected, f"Columnas esperadas: {expected}, got: {cols}"


def test_view_returns_expected_rows():
    # Con los inserts del README: Ana compra Laptop y 2 Mouse; Luis compra 1 Teclado. :contentReference[oaicite:2]{index=2}
    rows = psql("""
      SELECT cliente, producto, cantidad, total_linea
      FROM vista_detalle_pedidos
      WHERE id_pedido = 1
      ORDER BY producto;
    """)
    assert len(rows) == 2, f"Se esperaban 2 renglones para id_pedido=1, got={len(rows)}"

    parsed = [r.split("\t") for r in rows]
    assert parsed[0][0] == "Ana Torres"
    assert parsed[0][1] == "Laptop"
    assert int(parsed[0][2]) == 1
    assert parsed[1][1] == "Mouse"
    assert int(parsed[1][2]) == 2

