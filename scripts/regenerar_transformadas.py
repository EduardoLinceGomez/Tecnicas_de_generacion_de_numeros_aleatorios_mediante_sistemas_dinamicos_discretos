#!/usr/bin/env python3
"""Regenera las FGM y funciones características reproducibles."""

import argparse
import json
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from tesis_generacion.visualizacion.transformadas import (
    copiar_referencias_transformadas,
    regenerar_transformadas,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Regenera FGM y funciones características del bloque 10."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/transformadas"),
        help="directorio temporal para figuras y resumen CSV",
    )
    parser.add_argument(
        "--reference-dir",
        type=Path,
        help="copia explícitamente las referencias diagnósticas regeneradas",
    )
    argumentos = parser.parse_args()

    resumen = regenerar_transformadas(argumentos.output_dir)
    if argumentos.reference_dir is not None:
        copiar_referencias_transformadas(
            argumentos.output_dir, argumentos.reference_dir
        )
        resumen["reference_dir"] = str(argumentos.reference_dir.resolve())
    print(json.dumps(resumen, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
