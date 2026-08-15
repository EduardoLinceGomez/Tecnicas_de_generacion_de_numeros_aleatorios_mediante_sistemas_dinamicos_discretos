#!/usr/bin/env python3
"""Regenera de forma autónoma las ocho figuras del coleccionista."""

import argparse
import json
from pathlib import Path

from tesis_generacion.estadistica.coleccionista import (
    metricas_coleccionista,
)
from tesis_generacion.experimentos import (
    FACTOR_TIENDA,
    NUM_CELDAS,
    NUM_ITERACIONES,
    NUM_VALORES,
    SEED,
    construir_muestras,
    muestra_logistica,
    muestra_tienda,
    muestras_regla_30,
)
from tesis_generacion.visualizacion import (
    regenerar,
    regenerar_muestra,
    validar_muestra,
)


metricas_muestra = metricas_coleccionista


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
