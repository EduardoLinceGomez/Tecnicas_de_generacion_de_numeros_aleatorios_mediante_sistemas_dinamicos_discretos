"""Pruebas del CLI oficial para regenerar las figuras del coleccionista."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tesis_generacion.visualizacion import regenerar


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "regenerar_coleccionista.py"
NOMBRES_PNG = {
    "Log_dens_CCT.png",
    "R30_col_densCCT.png",
    "R30_col_distCCT.png",
    "R30_fila_densCCT.png",
    "R30_fila_distCCT.png",
    "Tent_dens_CCT.png",
    "Tent_dsit_CCT.png",
    "log_dist_CCT.png",
}


def _entorno_subprocess(temporal: Path) -> dict:
    entorno = os.environ.copy()
    entorno["MPLBACKEND"] = "Agg"
    entorno["MPLCONFIGDIR"] = str(temporal / "matplotlib")
    entorno["PYTHONPYCACHEPREFIX"] = str(temporal / "pycache")
    return entorno


class CliColeccionistaTest(unittest.TestCase):
    def test_script_existe(self) -> None:
        self.assertTrue(SCRIPT.is_file())

    def test_help(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cli-help-") as temporal:
            resultado = subprocess.run(
                [sys.executable, str(SCRIPT), "--help"],
                cwd=REPO_ROOT,
                env=_entorno_subprocess(Path(temporal)),
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(resultado.returncode, 0, msg=resultado.stderr)
        self.assertIn("--output-dir", resultado.stdout)

    def test_ejecucion_coincide_con_api_canonica(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cli-coleccionista-") as temporal:
            directorio = Path(temporal)
            salida_cli = directorio / "cli"
            salida_canonica = directorio / "canonica"
            resultado = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--output-dir",
                    str(salida_cli),
                ],
                cwd=REPO_ROOT,
                env=_entorno_subprocess(directorio),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(resultado.returncode, 0, msg=resultado.stderr)

            resumen_cli = json.loads(resultado.stdout)
            resumen_canonico = regenerar(salida_canonica)

            self.assertEqual(
                list(resumen_cli),
                ["logistico", "r30_columnas", "r30_filas", "tienda"],
            )
            self.assertEqual(resumen_cli, resumen_canonico)
            self.assertEqual(
                {ruta.name for ruta in salida_cli.iterdir()}, NOMBRES_PNG
            )
            self.assertEqual(
                {ruta.name for ruta in salida_canonica.iterdir()}, NOMBRES_PNG
            )
            for nombre in NOMBRES_PNG:
                with self.subTest(figura=nombre):
                    self.assertEqual(
                        (salida_cli / nombre).read_bytes(),
                        (salida_canonica / nombre).read_bytes(),
                    )


if __name__ == "__main__":
    unittest.main()
