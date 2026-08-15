"""Pruebas del CLI reproducible del bloque 12."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tesis_generacion.visualizacion.reordenamiento import (
    ARCHIVOS_REFERENCIA_REORDENAMIENTO,
    ARCHIVOS_TESIS_REORDENAMIENTO,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "regenerar_reordenamiento.py"


def _entorno_subprocess(temporal: Path) -> dict:
    entorno = os.environ.copy()
    entorno["MPLBACKEND"] = "Agg"
    entorno["MPLCONFIGDIR"] = str(temporal / "matplotlib")
    entorno["PYTHONPYCACHEPREFIX"] = str(temporal / "pycache")
    return entorno


class CliReordenamientoTest(unittest.TestCase):
    def test_help(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cli-reordenamiento-help-") as tmp:
            resultado = subprocess.run(
                [sys.executable, str(SCRIPT), "--help"],
                cwd=REPO_ROOT,
                env=_entorno_subprocess(Path(tmp)),
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(resultado.returncode, 0, msg=resultado.stderr)
        self.assertIn("--output-dir", resultado.stdout)
        self.assertIn("--reference-dir", resultado.stdout)

    def test_ejecucion_json_figuras_y_referencias(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cli-reordenamiento-") as temporal:
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
                set(ARCHIVOS_REFERENCIA_REORDENAMIENTO)
                | set(ARCHIVOS_TESIS_REORDENAMIENTO.values()),
            )
            self.assertEqual(
                {ruta.name for ruta in referencias.iterdir()},
                set(ARCHIVOS_REFERENCIA_REORDENAMIENTO),
            )
            self.assertEqual(resumen["parametros"]["lags"], list(range(1, 21)))


if __name__ == "__main__":
    unittest.main()
