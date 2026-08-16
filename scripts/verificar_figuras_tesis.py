#!/usr/bin/env python3
"""Verifica el manifiesto y, opcionalmente, su integración en la tesis."""

import argparse
import json
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from tesis_generacion.visualizacion.manifest_figuras import (
    actualizar_sha,
    verificar_manifest,
    verificar_tesis,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("figuras_tesis/manifest_figuras.csv"),
    )
    parser.add_argument("--tesis-root", type=Path)
    parser.add_argument(
        "--actualizar-sha",
        action="store_true",
        help="actualiza de forma explícita los SHA desde las copias canónicas",
    )
    argumentos = parser.parse_args()
    if argumentos.actualizar_sha:
        actualizar_sha(argumentos.manifest)
    resultado = {"manifest": verificar_manifest(argumentos.manifest)}
    if argumentos.tesis_root is not None:
        resultado["tesis"] = verificar_tesis(
            argumentos.manifest, argumentos.tesis_root
        )
    print(json.dumps(resultado, indent=2, ensure_ascii=False, sort_keys=True))
    errores = list(resultado["manifest"]["errores"])
    if "tesis" in resultado:
        errores.extend(resultado["tesis"]["errores"])
    if errores:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
