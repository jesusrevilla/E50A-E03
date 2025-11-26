
# -*- coding: utf-8 -*-
import os
import subprocess
from decimal import Decimal

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


def test_function_exists():
    # Debe existir la función total_gastado_por_cliente (README). :contentReference[oaicite:5]{index=5}
    r = psql("""
      SELECT COUNT(*)
      FROM pg_proc
      WHERE proname='total_gastado_por_cliente'
        AND prokind='f';
    """)
    assert int(r[0]) >= 1, "No existe la FUNCIÓN total_gastado_por_cliente(id_cliente)"


def test_total_gastado_for_cliente_1():
    # Con los inserts del README:
    # Ana (id=1) compra 1 Laptop (1200.00) y 2 Mouse (25.50) => 1200 + 51 = 1251.00 :contentReference[oaicite:6]{index=6}
    r = psql("SELECT total_gastado_por_cliente(1);")
    got = Decimal(r[0]).quantize(Decimal("0.01"))
    assert got == Decimal("1251.00"), f"Esperado 1251.00, got {got}"
