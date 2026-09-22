import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest


@pytest.mark.skipif(
    shutil.which("latex") is None or shutil.which("dvipng") is None,
    reason="la exportación editorial requiere LaTeX y dvipng",
)
def test_cli_regenera_pdf_svg_png_y_reporte(tmp_path: Path) -> None:
    salida = tmp_path / "salida"
    entorno = os.environ.copy()
    entorno["MPLBACKEND"] = "Agg"
    entorno["MPLCONFIGDIR"] = str(tmp_path / "matplotlib")
    resultado = subprocess.run(
        [
            sys.executable,
            "scripts/regenerar_bifurcaciones.py",
            "--output-dir",
            str(salida),
            "--numero-parametros",
            "80",
            "--burn-in",
            "20",
            "--iteraciones-graficadas",
            "8",
            "--dpi",
            "96",
        ],
        check=True,
        capture_output=True,
        text=True,
        env=entorno,
    )

    reporte_stdout = json.loads(resultado.stdout)
    reporte_archivo = json.loads(
        (salida / "reporte_bifurcaciones.json").read_text(encoding="utf-8")
    )
    assert reporte_stdout == reporte_archivo
    assert reporte_archivo["renderizado"]["latex"] is True
    assert len(reporte_archivo["archivos"]) == 6
    assert all((salida / nombre).is_file() for nombre in reporte_archivo["archivos"])
