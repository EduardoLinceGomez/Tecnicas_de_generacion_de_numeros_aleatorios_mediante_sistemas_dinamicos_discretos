"""Pruebas de figuras y referencias del reordenamiento."""

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
            self.assertEqual(
                resumen["parametros"]["intervalos_brechas_comunes"],
                {"i1": [0.1, 0.3], "i2": [0.4, 0.6], "i3": [0.7, 0.9]},
            )
            self.assertEqual(resumen["parametros"]["p_brechas"], 0.2)
            self.assertEqual(len(resumen["figuras"]), 13)
            with (directorio / "resumen_reordenamiento.csv").open(
                encoding="utf-8", newline=""
            ) as archivo:
                filas_generales = list(csv.DictReader(archivo))
            with (directorio / "resumen_brechas_reordenamiento.csv").open(
                encoding="utf-8", newline=""
            ) as archivo:
                filas_brechas = list(csv.DictReader(archivo))
            self.assertEqual(len(filas_generales), 4)
            self.assertEqual(len(filas_brechas), 12)
            self.assertNotIn("alpha", filas_generales[0])
            self.assertEqual(
                {fila["intervalo_id"] for fila in filas_brechas},
                {"i1", "i2", "i3"},
            )
            self.assertTrue(all(float(fila["p"]) == 0.2 for fila in filas_brechas))
            self.assertEqual(
                {int(fila["maximo_soporte_evaluacion"]) for fila in filas_brechas},
                {26, 35, 43},
            )

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
