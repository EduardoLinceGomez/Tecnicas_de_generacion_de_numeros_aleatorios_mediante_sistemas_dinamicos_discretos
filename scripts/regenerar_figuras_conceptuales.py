#!/usr/bin/env python3
"""Regenera las figuras conceptuales y canónicas incorporadas en el bloque 14."""

import argparse
import json
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from tesis_generacion.visualizacion.figuras_tesis import (
    copiar_archivos_generados,
    regenerar_figuras_tesis,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Regenera las figuras conceptuales y canónicas del bloque 14."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/figuras_tesis"),
        help="directorio temporal de salida",
    )
    parser.add_argument(
        "--reference-dir",
        type=Path,
        help="directorio canónico al que se copiarán explícitamente las salidas",
    )
    argumentos = parser.parse_args()

    resumen = regenerar_figuras_tesis(argumentos.output_dir)
    if argumentos.reference_dir is not None:
        mapeo = {nombre: nombre for nombre in resumen["archivos"]}
        copiar_archivos_generados(
            argumentos.output_dir, argumentos.reference_dir, mapeo
        )
        resumen["reference_dir"] = str(argumentos.reference_dir.resolve())
    print(json.dumps(resumen, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
