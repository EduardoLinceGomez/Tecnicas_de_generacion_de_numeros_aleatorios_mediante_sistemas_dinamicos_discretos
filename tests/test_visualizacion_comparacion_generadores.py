"""Pruebas de figuras y CSV comparativos."""

import csv
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

from tesis_generacion.visualizacion.comparacion_generadores import (
    ARCHIVOS_REFERENCIA_COMPARACION,
    copiar_referencias_comparacion,
    regenerar_comparacion_generadores,
)


DATA_DIR = Path(__file__).resolve().parent / "data"
VARIABLE_PNG_ESTRICTO = "VERIFICAR_PNG_COMPARACION"


def _baseline() -> dict:
    return json.loads(
        (DATA_DIR / "comparacion_generadores_baseline.json").read_text(
            encoding="utf-8"
        )
    )


class RegeneracionComparacionTest(unittest.TestCase):
    def test_genera_seis_figuras_dos_csv_y_resumen(self) -> None:
        with tempfile.TemporaryDirectory(prefix="visual-comparacion-") as temporal:
            directorio = Path(temporal)
            resumen = regenerar_comparacion_generadores(directorio)
            self.assertEqual(
                {ruta.name for ruta in directorio.iterdir()},
                set(ARCHIVOS_REFERENCIA_COMPARACION),
            )
            self.assertEqual(
                set(resumen["archivos"]), set(ARCHIVOS_REFERENCIA_COMPARACION)
            )
            with (directorio / "resumen_comparacion.csv").open(
                encoding="utf-8", newline=""
            ) as archivo:
                filas = list(csv.DictReader(archivo))
            self.assertEqual(len(filas), 5)
            self.assertNotIn("ranking", filas[0])
            self.assertNotIn("score", filas[0])
            with (directorio / "resumen_brechas_comparacion.csv").open(
                encoding="utf-8", newline=""
            ) as archivo:
                filas_brechas = list(csv.DictReader(archivo))
            self.assertEqual(len(filas_brechas), 15)
            self.assertEqual(
                {fila["intervalo_id"] for fila in filas_brechas},
                {"i1", "i2", "i3"},
            )
            self.assertTrue(all(float(fila["p"]) == 0.2 for fila in filas_brechas))
            self.assertNotIn("ranking", filas_brechas[0])
            self.assertNotIn("score", filas_brechas[0])
            self.assertEqual(len(resumen["figuras"]), 6)

    def test_copia_solo_referencias_explicitas(self) -> None:
        with tempfile.TemporaryDirectory(prefix="refs-comparacion-") as temporal:
            raiz = Path(temporal)
            salida = raiz / "output"
            referencias = raiz / "referencias"
            regenerar_comparacion_generadores(salida)
            copiar_referencias_comparacion(salida, referencias)
            self.assertEqual(
                {ruta.name for ruta in referencias.iterdir()},
                set(ARCHIVOS_REFERENCIA_COMPARACION),
            )


@unittest.skipUnless(
    os.environ.get(VARIABLE_PNG_ESTRICTO) == "1",
    f"active {VARIABLE_PNG_ESTRICTO}=1 para validar las referencias exactas",
)
class BaselineGraficoComparacionEstrictoTest(unittest.TestCase):
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
        with tempfile.TemporaryDirectory(prefix="comparacion-png-") as temporal:
            directorio = Path(temporal)
            regenerar_comparacion_generadores(directorio)
            for nombre, sha256 in baseline["referencias_sha256"].items():
                observado_sha = hashlib.sha256(
                    (directorio / nombre).read_bytes()
                ).hexdigest()
                self.assertEqual(observado_sha, sha256)


if __name__ == "__main__":
    unittest.main()
