"""Pruebas del CLI reproducible de invariancia."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tesis_generacion.visualizacion.invariancia import (
    ARCHIVOS_REFERENCIA_INVARIANCIA,
    ARCHIVOS_TESIS_INVARIANCIA,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "regenerar_invariancia.py"


def _entorno_subprocess(temporal: Path) -> dict:
    entorno = os.environ.copy()
    entorno["MPLBACKEND"] = "Agg"
    entorno["MPLCONFIGDIR"] = str(temporal / "matplotlib")
    entorno["PYTHONPYCACHEPREFIX"] = str(temporal / "pycache")
    return entorno


class CliInvarianciaTest(unittest.TestCase):
    def test_help(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cli-invariancia-help-") as temporal:
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
        self.assertIn("--reference-dir", resultado.stdout)

    def test_ejecucion_json_figuras_y_referencias(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cli-invariancia-") as temporal:
            raiz = Path(temporal)
            salida = raiz / "output"
            referencias = raiz / "referencias"
            resultado = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--output-dir",
                    str(salida),
                    "--reference-dir",
                    str(referencias),
                ],
                cwd=REPO_ROOT,
                env=_entorno_subprocess(raiz),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(resultado.returncode, 0, msg=resultado.stderr)
            resumen = json.loads(resultado.stdout)
            self.assertEqual(resumen["reference_dir"], str(referencias.resolve()))
            self.assertEqual(
                {ruta.name for ruta in salida.iterdir()},
                set(ARCHIVOS_REFERENCIA_INVARIANCIA)
                | set(ARCHIVOS_TESIS_INVARIANCIA),
            )
            self.assertEqual(
                {ruta.name for ruta in referencias.iterdir()},
                set(ARCHIVOS_REFERENCIA_INVARIANCIA),
            )
            self.assertEqual(resumen["parametros"]["n"], 1000)


if __name__ == "__main__":
    unittest.main()
