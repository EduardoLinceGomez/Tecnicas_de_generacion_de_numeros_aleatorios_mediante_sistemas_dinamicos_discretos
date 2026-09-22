import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class CliBifurcacionesTest(unittest.TestCase):
    @unittest.skipUnless(
        shutil.which("latex") and shutil.which("dvipng"),
        "la exportación editorial requiere LaTeX y dvipng",
    )
    def test_cli_regenera_pdf_svg_png_y_reporte(self) -> None:
        with tempfile.TemporaryDirectory() as temporal:
            raiz = Path(temporal)
            salida = raiz / "salida"
            entorno = os.environ.copy()
            entorno["MPLBACKEND"] = "Agg"
            entorno["MPLCONFIGDIR"] = str(raiz / "matplotlib")
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
            self.assertEqual(reporte_stdout, reporte_archivo)
            self.assertTrue(reporte_archivo["renderizado"]["latex"])
            self.assertEqual(len(reporte_archivo["archivos"]), 6)
            self.assertTrue(
                all((salida / nombre).is_file() for nombre in reporte_archivo["archivos"])
            )


if __name__ == "__main__":
    unittest.main()
