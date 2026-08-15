"""Regresión científica del coleccionista en el punto de control d837e4f."""

import hashlib
import json
import math
import os
import platform
import tempfile
import unittest
from pathlib import Path

import matplotlib
import numpy as np
import scipy

from coleccionista import (
    PRECISION_DECIMAL,
    cdf_coleccionista,
    media_teorica_coleccionista,
    pmf_coleccionista,
)
from regenerar_coleccionista import (
    SEED,
    construir_muestras,
    metricas_muestra,
    regenerar,
)


DATA_DIR = Path(__file__).resolve().parent / "data"
TOLERANCIA_FLOAT = 1e-12
VARIABLE_PNG_ESTRICTO = "VERIFICAR_PNG_EXACTO"


def _cargar_json(nombre: str) -> dict:
    with (DATA_DIR / nombre).open(encoding="utf-8") as archivo:
        return json.load(archivo)


class BaselineCientificoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.baseline = _cargar_json("coleccionista_baseline.json")
        cls.muestras = construir_muestras()

    def test_constantes_y_distribucion_mcf036(self) -> None:
        self.assertEqual(
            self.baseline["commit_origen"],
            "d837e4fc1e3c773b129a7036a36c91a975d185d7",
        )
        self.assertEqual(PRECISION_DECIMAL, self.baseline["precision_decimal"])
        self.assertEqual(SEED, self.baseline["seed"])
        self.assertTrue(
            math.isclose(
                media_teorica_coleccionista(),
                self.baseline["media_teorica"],
                rel_tol=0.0,
                abs_tol=TOLERANCIA_FLOAT,
            )
        )
        self.assertEqual(cdf_coleccionista(9), 0.0)
        self.assertTrue(
            math.isclose(
                cdf_coleccionista(10),
                0.00036288,
                rel_tol=0.0,
                abs_tol=1e-14,
            )
        )
        for m in (10, 11, 15, 20, 30, 50):
            with self.subTest(m=m):
                self.assertTrue(
                    math.isclose(
                        pmf_coleccionista(m),
                        cdf_coleccionista(m) - cdf_coleccionista(m - 1),
                        rel_tol=0.0,
                        abs_tol=1e-15,
                    )
                )

    def test_muestras_metricas_y_fingerprints(self) -> None:
        esperadas = self.baseline["muestras"]
        self.assertEqual(set(self.muestras), set(esperadas))

        campos_enteros = (
            ("total_digitos", "n_digitos"),
            ("bloques_completos", "bloques"),
            ("cola_censurada", "cola"),
            ("minimo", "minimo"),
            ("maximo", "maximo"),
            ("mediana", "mediana"),
        )
        campos_float = (
            ("media", "media"),
            ("distancia_maxima_cdf", "distancia_maxima_cdf"),
            ("mae_cdf", "mae_cdf"),
        )

        for nombre, muestra in self.muestras.items():
            with self.subTest(muestra=nombre):
                esperado = esperadas[nombre]
                valores = np.asarray(muestra, dtype=np.dtype("<f8"))
                fingerprint = esperado["fingerprint"]

                self.assertEqual(len(valores), esperado["n_valores"])
                self.assertEqual(valores.size, fingerprint["n_elementos"])
                self.assertEqual(valores.nbytes, fingerprint["n_bytes"])
                self.assertEqual(valores.dtype.str, fingerprint["dtype"])
                self.assertEqual(fingerprint["endianness"], "little")
                self.assertEqual(
                    hashlib.sha256(valores.tobytes(order="C")).hexdigest(),
                    fingerprint["sha256"],
                )

                _, observadas = metricas_muestra(valores)
                self.assertEqual(observadas["numero_u"], esperado["n_valores"])
                for campo_actual, campo_baseline in campos_enteros:
                    self.assertEqual(
                        observadas[campo_actual], esperado[campo_baseline]
                    )
                for campo_actual, campo_baseline in campos_float:
                    self.assertTrue(
                        math.isclose(
                            observadas[campo_actual],
                            esperado[campo_baseline],
                            rel_tol=0.0,
                            abs_tol=TOLERANCIA_FLOAT,
                        ),
                        msg=(
                            f"{nombre}.{campo_actual}: "
                            f"{observadas[campo_actual]!r} != "
                            f"{esperado[campo_baseline]!r}"
                        ),
                    )


@unittest.skipUnless(
    os.environ.get(VARIABLE_PNG_ESTRICTO) == "1",
    f"active {VARIABLE_PNG_ESTRICTO}=1 para validar los PNG exactos",
)
class BaselineGraficoEstrictoTest(unittest.TestCase):
    def test_png_en_entorno_de_referencia(self) -> None:
        from PIL import __version__ as pillow_version

        manifiesto = _cargar_json("coleccionista_sha256.json")
        entorno = manifiesto["entorno_referencia"]
        observado = {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "matplotlib": matplotlib.__version__,
            "pillow": pillow_version,
            "backend": str(matplotlib.get_backend()),
        }
        self.assertEqual(observado, entorno)

        with tempfile.TemporaryDirectory(prefix="coleccionista-png-") as temporal:
            directorio = Path(temporal)
            regenerar(directorio)
            esperados = manifiesto["figuras"]
            self.assertEqual(
                {ruta.name for ruta in directorio.glob("*.png")}, set(esperados)
            )
            for nombre, sha256 in esperados.items():
                with self.subTest(figura=nombre):
                    observado_sha = hashlib.sha256(
                        (directorio / nombre).read_bytes()
                    ).hexdigest()
                    self.assertEqual(observado_sha, sha256)


if __name__ == "__main__":
    unittest.main()
