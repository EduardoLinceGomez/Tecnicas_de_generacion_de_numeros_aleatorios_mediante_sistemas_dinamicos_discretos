#!/usr/bin/env python3
"""Regenera los diagramas de bifurcación de calidad editorial."""

import argparse
import json
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from tesis_generacion.visualizacion.bifurcaciones import (
    ConfiguracionBifurcacion,
    regenerar_bifurcaciones,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Regenera las bifurcaciones logística y tienda como PDF híbrido, "
            "SVG híbrido y PNG de inspección."
        )
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/bifurcaciones_publicacion"),
        help="directorio de salida; no se modifica el repositorio de la tesis",
    )
    parser.add_argument("--numero-parametros", type=int, default=6000)
    parser.add_argument("--burn-in", type=int, default=900)
    parser.add_argument("--iteraciones-graficadas", type=int, default=100)
    parser.add_argument("--alpha", type=float, default=0.45)
    parser.add_argument("--tamano-punto", type=float, default=0.20)
    parser.add_argument("--dpi", type=int, default=600)
    parser.add_argument(
        "--sin-svg",
        action="store_true",
        help="omite el SVG híbrido y conserva PDF y PNG",
    )
    argumentos = parser.parse_args()

    configuracion = ConfiguracionBifurcacion(
        numero_parametros=argumentos.numero_parametros,
        burn_in=argumentos.burn_in,
        iteraciones_graficadas=argumentos.iteraciones_graficadas,
        alpha=argumentos.alpha,
        tamano_punto_pt2=argumentos.tamano_punto,
        dpi=argumentos.dpi,
    )
    reporte = regenerar_bifurcaciones(
        argumentos.output_dir,
        configuracion,
        incluir_svg=not argumentos.sin_svg,
    )
    ruta_reporte = argumentos.output_dir / "reporte_bifurcaciones.json"
    ruta_reporte.write_text(
        json.dumps(reporte, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(reporte, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
