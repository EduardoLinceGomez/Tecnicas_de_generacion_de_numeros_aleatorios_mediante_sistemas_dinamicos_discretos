"""Pruebas de figuras y referencias del reordenamiento."""

import hashlib
import json
import os
import platform
import tempfile
import unittest
from pathlib import Path

import matplotlib
import numpy as np
import scipy
from PIL import __version__ as pillow_version

from tesis_generacion.visualizacion.reordenamiento import (
    ARCHIVOS_REFERENCIA_REORDENAMIENTO,
    ARCHIVOS_TESIS_REORDENAMIENTO,
    copiar_referencias_reordenamiento,
    regenerar_reordenamiento,
)


DATA_DIR = Path(__file__).resolve().parent / "data"
VARIABLE_PNG_ESTRICTO = "VERIFICAR_PNG_REORDENAMIENTO"


def _baseline() -> dict:
    return json.loads(
        (DATA_DIR / "reordenamiento_baseline.json").read_text(encoding="utf-8")
    )


class RegeneracionReordenamientoTest(unittest.TestCase):
    def test_genera_figuras_csv_y_resumen(self) -> None:
        with tempfile.TemporaryDirectory(prefix="visual-reordenamiento-") as temporal:
            directorio = Path(temporal)
            resumen = regenerar_reordenamiento(directorio)
            esperados = set(ARCHIVOS_REFERENCIA_REORDENAMIENTO) | set(
                ARCHIVOS_TESIS_REORDENAMIENTO.values()
            )
            self.assertEqual({ruta.name for ruta in directorio.iterdir()}, esperados)
            self.assertEqual(set(resumen["archivos"]), esperados)
            self.assertEqual(resumen["parametros"]["n"], 1000)
            self.assertEqual(resumen["parametros"]["seed_reordenamiento"], 2024)
            self.assertEqual(len(resumen["figuras"]), 13)

    def test_copia_solo_referencias_explicitas(self) -> None:
        with tempfile.TemporaryDirectory(prefix="refs-reordenamiento-") as temporal:
            raiz = Path(temporal)
            salida = raiz / "output"
            referencias = raiz / "referencias"
            regenerar_reordenamiento(salida)
            copiar_referencias_reordenamiento(salida, referencias)
            self.assertEqual(
                {ruta.name for ruta in referencias.iterdir()},
                set(ARCHIVOS_REFERENCIA_REORDENAMIENTO),
            )
            for nombre in ARCHIVOS_REFERENCIA_REORDENAMIENTO:
                self.assertEqual(
                    (salida / nombre).read_bytes(),
                    (referencias / nombre).read_bytes(),
                )


@unittest.skipUnless(
    os.environ.get(VARIABLE_PNG_ESTRICTO) == "1",
    f"active {VARIABLE_PNG_ESTRICTO}=1 para validar las referencias exactas",
)
class BaselineGraficoReordenamientoEstrictoTest(unittest.TestCase):
    def test_referencias_en_entorno_baseline(self) -> None:
        baseline = _baseline()
        observado = {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "matplotlib": matplotlib.__version__,
            "pillow": pillow_version,
            "backend": str(matplotlib.get_backend()),
        }
        self.assertEqual(observado, baseline["entorno_referencia"])
        with tempfile.TemporaryDirectory(prefix="reordenamiento-png-") as temporal:
            directorio = Path(temporal)
            regenerar_reordenamiento(directorio)
            for nombre, sha256 in baseline["referencias_sha256"].items():
                observado_sha = hashlib.sha256(
                    (directorio / nombre).read_bytes()
                ).hexdigest()
                self.assertEqual(observado_sha, sha256)


if __name__ == "__main__":
    unittest.main()
