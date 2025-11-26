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


def test_graph_tables_exist():
    # README: ciudades (nodos) y rutas (aristas) :contentReference[oaicite:14]{index=14}
    r1 = psql("""
      SELECT COUNT(*)
      FROM information_schema.tables
      WHERE table_schema='public' AND table_name='ciudades';
    """)
    r2 = psql("""
      SELECT COUNT(*)
      FROM information_schema.tables
      WHERE table_schema='public' AND table_name='rutas';
    """)
    assert int(r1[0]) == 1, "No existe la tabla ciudades"
    assert int(r2[0]) == 1, "No existe la tabla rutas"


def test_graph_seed_counts():
    # README inserta 5 ciudades y 5 rutas :contentReference[oaicite:15]{index=15}
    c = int(psql("SELECT COUNT(*) FROM ciudades;")[0])
    r = int(psql("SELECT COUNT(*) FROM rutas;")[0])
    assert c == 5, f"Se esperaban 5 ciudades, got {c}"
    assert r == 5, f"Se esperaban 5 rutas, got {r}"


def test_routes_from_slp():
    # README: desde San Luis Potosí (id=1) salen 2 rutas: a 2 y a 5 :contentReference[oaicite:16]{index=16}
    out = psql("""
      SELECT id_destino, distancia_km
      FROM rutas
      WHERE id_origen = 1
      ORDER BY id_destino;
    """)
    assert len(out) == 2, f"Se esperaban 2 rutas desde SLP (id=1), got {len(out)}"
    d1 = out[0].split("\t")
    d2 = out[1].split("\t")
    assert int(d1[0]) == 2 and int(d1[1]) == 180
    assert int(d2[0]) == 5 and int(d2[1]) == 410
