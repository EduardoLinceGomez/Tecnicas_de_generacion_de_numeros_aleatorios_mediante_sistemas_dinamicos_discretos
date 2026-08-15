"""Pruebas de las figuras reproducibles de invariancia."""

import hashlib
import json
import os
import platform
import tempfile
import unittest
from pathlib import Path

import matplotlib
import numpy as np
from PIL import __version__ as pillow_version

from tesis_generacion.visualizacion.invariancia import (
    ARCHIVOS_REFERENCIA_INVARIANCIA,
    ARCHIVOS_TESIS_INVARIANCIA,
    copiar_referencias_invariancia,
    regenerar_invariancia,
)


DATA_DIR = Path(__file__).resolve().parent / "data"
VARIABLE_PNG_ESTRICTO = "VERIFICAR_PNG_INVARIANCIA"


def _baseline() -> dict:
    return json.loads(
        (DATA_DIR / "invariancia_baseline.json").read_text(encoding="utf-8")
    )


class RegeneracionInvarianciaTest(unittest.TestCase):
    def test_genera_figuras_csv_y_resumen(self) -> None:
        with tempfile.TemporaryDirectory(prefix="visual-invariancia-") as temporal:
            directorio = Path(temporal)
            resumen = regenerar_invariancia(directorio)
            esperados = set(ARCHIVOS_REFERENCIA_INVARIANCIA) | set(
                ARCHIVOS_TESIS_INVARIANCIA
            )
            self.assertEqual({ruta.name for ruta in directorio.iterdir()}, esperados)
            self.assertEqual(set(resumen["archivos"]), esperados)
            self.assertEqual(resumen["parametros"]["seed"], 2024)
            self.assertEqual(resumen["parametros"]["n"], 1000)
            self.assertEqual(resumen["parametros"]["iteraciones"], [0, 1, 2, 3, 4])
            self.assertEqual(len(resumen["figuras"]), 6)

    def test_copia_solo_referencias_explicitas(self) -> None:
        with tempfile.TemporaryDirectory(prefix="refs-invariancia-") as temporal:
            raiz = Path(temporal)
            salida = raiz / "output"
            referencias = raiz / "referencias"
            regenerar_invariancia(salida)
            copiar_referencias_invariancia(salida, referencias)
            self.assertEqual(
                {ruta.name for ruta in referencias.iterdir()},
                set(ARCHIVOS_REFERENCIA_INVARIANCIA),
            )
            for nombre in ARCHIVOS_REFERENCIA_INVARIANCIA:
                self.assertEqual(
                    (salida / nombre).read_bytes(),
                    (referencias / nombre).read_bytes(),
                )


@unittest.skipUnless(
    os.environ.get(VARIABLE_PNG_ESTRICTO) == "1",
    f"active {VARIABLE_PNG_ESTRICTO}=1 para validar las referencias exactas",
)
class BaselineGraficoInvarianciaEstrictoTest(unittest.TestCase):
    def test_referencias_en_entorno_baseline(self) -> None:
        baseline = _baseline()
        observado = {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "matplotlib": matplotlib.__version__,
            "pillow": pillow_version,
            "backend": str(matplotlib.get_backend()),
        }
        self.assertEqual(observado, baseline["entorno_referencia"])
        with tempfile.TemporaryDirectory(prefix="invariancia-png-") as temporal:
            directorio = Path(temporal)
            regenerar_invariancia(directorio)
            for nombre, sha256 in baseline["referencias_sha256"].items():
                observado_sha = hashlib.sha256(
                    (directorio / nombre).read_bytes()
                ).hexdigest()
                self.assertEqual(observado_sha, sha256)


if __name__ == "__main__":
    unittest.main()
