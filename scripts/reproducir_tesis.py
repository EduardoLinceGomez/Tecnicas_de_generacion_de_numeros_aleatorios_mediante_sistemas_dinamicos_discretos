#!/usr/bin/env python3
"""Orquesta la reproducción sin modificar las figuras canónicas."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Tarea:
    nombre: str
    argumentos: tuple[str, ...]
    herramientas: tuple[str, ...] = ()


def _script(nombre: str, salida: str) -> tuple[str, ...]:
    return (
        sys.executable,
        str(Path("scripts") / nombre),
        "--output-dir",
        str(Path("outputs") / salida),
    )


EXPERIMENTOS = (
    Tarea("momentos", _script("regenerar_momentos.py", "momentos")),
    Tarea("transformadas", _script("regenerar_transformadas.py", "transformadas")),
    Tarea("invariancia", _script("regenerar_invariancia.py", "invariancia")),
    Tarea(
        "reordenamiento",
        _script("regenerar_reordenamiento.py", "reordenamiento"),
    ),
    Tarea(
        "comparacion_generadores",
        _script("regenerar_comparacion_generadores.py", "comparacion_generadores"),
    ),
    Tarea(
        "coleccionista",
        _script("regenerar_coleccionista.py", "coleccionista"),
    ),
)

FIGURAS_ADICIONALES = (
    Tarea(
        "conceptuales",
        _script("regenerar_figuras_conceptuales.py", "figuras_tesis"),
    ),
    Tarea(
        "tikz",
        _script("regenerar_figuras_tikz.py", "figuras_tikz"),
        ("latexmk", "pdftoppm"),
    ),
    Tarea(
        "revision_mcf",
        _script("regenerar_figuras_revision_mcf.py", "revision_mcf"),
        ("latexmk",),
    ),
    Tarea(
        "bifurcaciones",
        _script("regenerar_bifurcaciones.py", "bifurcaciones_publicacion"),
        ("latex", "dvipng"),
    ),
)

VERIFICACIONES = (
    Tarea(
        "manifest_figuras",
        (
            sys.executable,
            str(Path("scripts") / "verificar_figuras_tesis.py"),
        ),
    ),
    Tarea(
        "compileall",
        (
            sys.executable,
            "-m",
            "compileall",
            "-q",
            "src",
            "scripts",
        ),
    ),
    Tarea(
        "tests",
        (
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests",
            "-p",
            "test_*.py",
            "-v",
        ),
    ),
)


def seleccionar_tareas(modo: str) -> tuple[Tarea, ...]:
    if modo == "experiments":
        return EXPERIMENTOS
    if modo == "figures":
        return (*EXPERIMENTOS, *FIGURAS_ADICIONALES)
    if modo == "verify":
        return VERIFICACIONES
    if modo == "all":
        return (*EXPERIMENTOS, *FIGURAS_ADICIONALES, *VERIFICACIONES)
    raise ValueError(f"modo desconocido: {modo}")


def _validar_herramientas(tareas: Iterable[Tarea]) -> None:
    faltantes = sorted(
        {
            herramienta
            for tarea in tareas
            for herramienta in tarea.herramientas
            if shutil.which(herramienta) is None
        }
    )
    if faltantes:
        raise SystemExit(
            "Faltan herramientas externas necesarias: " + ", ".join(faltantes)
        )


def _representar_comando(argumentos: tuple[str, ...]) -> str:
    representados = ["python" if parte == sys.executable else parte for parte in argumentos]
    return " ".join(representados)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--all", action="store_const", const="all", dest="modo")
    grupo.add_argument(
        "--experiments", action="store_const", const="experiments", dest="modo"
    )
    grupo.add_argument(
        "--figures", action="store_const", const="figures", dest="modo"
    )
    grupo.add_argument("--verify", action="store_const", const="verify", dest="modo")
    parser.add_argument(
        "--plan",
        action="store_true",
        help="muestra las tareas seleccionadas sin ejecutarlas",
    )
    argumentos = parser.parse_args()

    tareas = seleccionar_tareas(argumentos.modo)
    plan = {
        "modo": argumentos.modo,
        "tareas": [
            {
                "nombre": tarea.nombre,
                "comando": _representar_comando(tarea.argumentos),
                "herramientas": list(tarea.herramientas),
            }
            for tarea in tareas
        ],
    }
    if argumentos.plan:
        print(json.dumps(plan, indent=2, ensure_ascii=False))
        return

    _validar_herramientas(tareas)
    output_root = REPO_ROOT / "outputs"
    output_root.mkdir(parents=True, exist_ok=True)
    entorno = os.environ.copy()
    entorno.setdefault("MPLBACKEND", "Agg")
    entorno.setdefault("MPLCONFIGDIR", str(output_root / ".matplotlib"))
    entorno.setdefault("PYTHONPYCACHEPREFIX", str(output_root / ".pycache"))

    ejecuciones = []
    inicio_total = time.monotonic()
    for tarea in tareas:
        print(f"\n==> {tarea.nombre}", flush=True)
        inicio = time.monotonic()
        subprocess.run(
            tarea.argumentos,
            cwd=REPO_ROOT,
            env=entorno,
            check=True,
        )
        ejecuciones.append(
            {
                "nombre": tarea.nombre,
                "comando": _representar_comando(tarea.argumentos),
                "segundos": round(time.monotonic() - inicio, 3),
                "estado": "ok",
            }
        )

    reporte = {
        **plan,
        "fecha_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "ejecuciones": ejecuciones,
        "segundos_totales": round(time.monotonic() - inicio_total, 3),
        "promocion_canonica": False,
    }
    ruta_reporte = output_root / "reporte_reproduccion.json"
    ruta_reporte.write_text(
        json.dumps(reporte, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"\nReporte: {ruta_reporte.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
