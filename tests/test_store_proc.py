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


def test_procedure_exists():
    # Debe existir el procedimiento registrar_pedido (README). :contentReference[oaicite:3]{index=3}
    r = psql("""
      SELECT COUNT(*)
      FROM pg_proc
      WHERE proname='registrar_pedido'
        AND prokind='p';
    """)
    assert int(r[0]) >= 1, "No existe el PROCEDURE registrar_pedido(...)"


def test_call_registrar_pedido_inserts_rows():
    # Ejemplo del README: CALL registrar_pedido(1,'2025-05-20',2,3) :contentReference[oaicite:4]{index=4}
    # Lo hacemos en transacción y ROLLBACK para que no ensucie la BD.
    out = psql("""
      BEGIN;

      SELECT COUNT(*) FROM pedidos;
      SELECT COUNT(*) FROM detalle_pedido;

      CALL registrar_pedido(1, '2025-05-20', 2, 3);

      SELECT COUNT(*) FROM pedidos;
      SELECT COUNT(*) FROM detalle_pedido;

      ROLLBACK;
    """)
    # Esperamos 4 líneas: pedidos_before, detalle_before, pedidos_after, detalle_after
    assert len(out) >= 4, f"Salida inesperada: {out}"

    pedidos_before = int(out[0])
    detalle_before = int(out[1])
    pedidos_after  = int(out[2])
    detalle_after  = int(out[3])

    assert pedidos_after == pedidos_before + 1, "CALL registrar_pedido no insertó en pedidos"
    assert detalle_after == detalle_before + 1, "CALL registrar_pedido no insertó en detalle_pedido"
