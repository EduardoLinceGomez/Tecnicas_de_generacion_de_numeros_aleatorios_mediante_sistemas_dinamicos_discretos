#!/usr/bin/env python3
"""Regenera las ocho figuras del coleccionista desde la API canónica."""

import argparse
import json
from pathlib import Path

from tesis_generacion.visualizacion import regenerar


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Regenera las ocho figuras de la prueba del coleccionista."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/coleccionista"),
        help="directorio portable para las ocho imágenes",
    )
    argumentos = parser.parse_args()

    resumen = regenerar(argumentos.output_dir)
    print(json.dumps(resumen, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
