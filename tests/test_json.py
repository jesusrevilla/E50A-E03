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


def test_json_tables_exist():
    # README: productos_json.usuarios con JSONB :contentReference[oaicite:11]{index=11}
    r1 = psql("""
      SELECT COUNT(*)
      FROM information_schema.columns
      WHERE table_schema='public' AND table_name='productos_json'
        AND column_name='atributos';
    """)
    assert int(r1[0]) == 1, "Falta productos_json.atributos"

    r2 = psql("""
      SELECT COUNT(*)
      FROM information_schema.columns
      WHERE table_schema='public' AND table_name='usuarios'
        AND column_name='historial_actividad';
    """)
    assert int(r2[0]) == 1, "Falta usuarios.historial_actividad"


def test_query_productos_json_marca_dell():
    # README: debe existir Laptop con marca Dell :contentReference[oaicite:12]{index=12}
    r = psql("""
      SELECT COUNT(*)
      FROM productos_json
      WHERE atributos ->> 'marca' = 'Dell';
    """)
    assert int(r[0]) >= 1, "No se encontró producto con marca Dell en productos_json"


def test_historial_actividad_contains_inicio_sesion():
    # README: consulta con @> '[{"accion":"inicio_sesion"}]' :contentReference[oaicite:13]{index=13}
    r = psql("""
      SELECT COUNT(*)
      FROM usuarios
      WHERE historial_actividad @> '[{"accion":"inicio_sesion"}]'::jsonb;
    """)
    assert int(r[0]) >= 1, "No se encontró usuario con accion inicio_sesion en historial_actividad"


def test_historial_is_array():
    r = psql("""
      SELECT COUNT(*)
      FROM usuarios
      WHERE jsonb_typeof(historial_actividad) = 'array';
    """)
    assert int(r[0]) >= 1, "historial_actividad no está guardado como arreglo JSONB"
