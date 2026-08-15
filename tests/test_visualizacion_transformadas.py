"""Pruebas de figuras reproducibles de transformadas."""

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

from tesis_generacion.visualizacion.transformadas import (
    ARCHIVOS_REFERENCIA_TRANSFORMADAS,
    ARCHIVOS_TESIS_TRANSFORMADAS,
    copiar_referencias_transformadas,
    regenerar_transformadas,
)


DATA_DIR = Path(__file__).resolve().parent / "data"
VARIABLE_PNG_ESTRICTO = "VERIFICAR_PNG_EXACTO"


def _baseline() -> dict:
    return json.loads(
        (DATA_DIR / "transformadas_baseline.json").read_text(encoding="utf-8")
    )


class RegeneracionTransformadasTest(unittest.TestCase):
    def test_genera_figuras_csv_metricas_y_fingerprints(self) -> None:
        with tempfile.TemporaryDirectory(prefix="visual-transformadas-") as temporal:
            directorio = Path(temporal)
            resumen = regenerar_transformadas(directorio)
            esperados = set(ARCHIVOS_REFERENCIA_TRANSFORMADAS) | set(
                ARCHIVOS_TESIS_TRANSFORMADAS
            )
            self.assertEqual(
                {ruta.name for ruta in directorio.iterdir()}, esperados
            )
            self.assertEqual(
                set(resumen["figuras"]),
                esperados - {"resumen_transformadas.csv"},
            )
            self.assertEqual(len(resumen["mallas"]["fgm"]), 40)
            self.assertEqual(
                len(resumen["mallas"]["funcion_caracteristica"]), 60
            )
            for nombre, muestra in resumen["muestras"].items():
                with self.subTest(nombre=nombre):
                    self.assertEqual(muestra["n"], 1000)
                    self.assertEqual(len(muestra["fingerprint"]["sha256"]), 64)
                    self.assertGreaterEqual(muestra["fgm"]["mae"], 0.0)
                    self.assertGreaterEqual(
                        muestra["funcion_caracteristica"]["mae"], 0.0
                    )
            self.assertEqual(
                resumen["muestras"]["logistico"]["fingerprint"]["sha256"],
                _baseline()["muestras"]["logistico"]["fingerprint"]["sha256"],
            )
            self.assertNotEqual(
                resumen["muestras"]["logistico"]["fingerprint"]["sha256"],
                resumen["logistico_historico_crudo"]["fingerprint"]["sha256"],
            )

    def test_copia_solo_referencias_explicitas(self) -> None:
        with tempfile.TemporaryDirectory(prefix="refs-transformadas-") as temporal:
            raiz = Path(temporal)
            salida = raiz / "output"
            referencias = raiz / "referencias"
            regenerar_transformadas(salida)
            copiar_referencias_transformadas(salida, referencias)
            self.assertEqual(
                {ruta.name for ruta in referencias.iterdir()},
                set(ARCHIVOS_REFERENCIA_TRANSFORMADAS),
            )
            for nombre in ARCHIVOS_REFERENCIA_TRANSFORMADAS:
                with self.subTest(nombre=nombre):
                    self.assertEqual(
                        (salida / nombre).read_bytes(),
                        (referencias / nombre).read_bytes(),
                    )


@unittest.skipUnless(
    os.environ.get(VARIABLE_PNG_ESTRICTO) == "1",
    f"active {VARIABLE_PNG_ESTRICTO}=1 para validar las referencias exactas",
)
class BaselineGraficoTransformadasEstrictoTest(unittest.TestCase):
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

        with tempfile.TemporaryDirectory(prefix="transformadas-png-") as temporal:
            directorio = Path(temporal)
            regenerar_transformadas(directorio)
            for nombre, sha256 in baseline["referencias_sha256"].items():
                with self.subTest(nombre=nombre):
                    observado_sha = hashlib.sha256(
                        (directorio / nombre).read_bytes()
                    ).hexdigest()
                    self.assertEqual(observado_sha, sha256)


if __name__ == "__main__":
    unittest.main()
