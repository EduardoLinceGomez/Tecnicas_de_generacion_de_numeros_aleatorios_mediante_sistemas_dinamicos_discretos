"""Pruebas de momentos ordinarios, centrales y estandarizados."""

import hashlib
import json
import math
import unittest
from pathlib import Path

import numpy as np

from tesis_generacion.estadistica import (
    asimetria_fisher_pearson,
    curtosis_pearson,
    exceso_curtosis,
    momento_central,
    momento_ordinario,
    momentos_ordinarios,
    momentos_teoricos_uniforme,
    resumen_momentos,
    resumen_uniforme_teorica,
    varianza_empirica,
)
from tesis_generacion.experimentos import construir_muestras


DATA_DIR = Path(__file__).resolve().parent / "data"


def _fingerprint(valores: np.ndarray) -> str:
    muestra = np.ascontiguousarray(valores, dtype=np.dtype("<f8"))
    return hashlib.sha256(muestra.tobytes(order="C")).hexdigest()


class MomentosControladosTest(unittest.TestCase):
    def setUp(self) -> None:
        self.valores = np.asarray([1.0, 2.0, 3.0, 4.0])

    def test_momentos_ordinarios_m1_a_m4(self) -> None:
        self.assertEqual(
            momentos_ordinarios(self.valores, 4),
            [2.5, 7.5, 25.0, 88.5],
        )
        for orden, esperado in enumerate([2.5, 7.5, 25.0, 88.5], 1):
            with self.subTest(orden=orden):
                self.assertEqual(
                    momento_ordinario(self.valores, orden), esperado
                )

    def test_momentos_centrales_y_varianza_con_divisor_n(self) -> None:
        esperados = {1: 0.0, 2: 1.25, 3: 0.0, 4: 2.5625}
        for orden, esperado in esperados.items():
            with self.subTest(orden=orden):
                self.assertEqual(
                    momento_central(self.valores, orden), esperado
                )
        self.assertEqual(varianza_empirica(self.valores), 1.25)
        self.assertEqual(np.var(self.valores, ddof=0), 1.25)
        self.assertNotEqual(np.var(self.valores, ddof=1), 1.25)

    def test_asimetria_curtosis_y_exceso(self) -> None:
        self.assertEqual(asimetria_fisher_pearson(self.valores), 0.0)
        self.assertTrue(
            math.isclose(
                curtosis_pearson(self.valores),
                1.64,
                rel_tol=0.0,
                abs_tol=1e-15,
            )
        )
        self.assertTrue(
            math.isclose(
                exceso_curtosis(self.valores),
                -1.36,
                rel_tol=0.0,
                abs_tol=1e-15,
            )
        )

    def test_varianza_cero_produce_error_claro(self) -> None:
        constantes = np.ones(5)
        with self.assertRaisesRegex(ValueError, "varianza es cero"):
            asimetria_fisher_pearson(constantes)
        with self.assertRaisesRegex(ValueError, "varianza es cero"):
            curtosis_pearson(constantes)

    def test_validaciones(self) -> None:
        with self.assertRaisesRegex(ValueError, "no puede estar vacío"):
            momento_ordinario([], 1)
        with self.assertRaisesRegex(ValueError, "NaN o infinito"):
            momento_ordinario([1.0, np.nan], 1)
        with self.assertRaisesRegex(ValueError, "unidimensional"):
            momento_ordinario([[1.0, 2.0]], 1)
        for orden in (0, -1):
            with self.subTest(orden=orden):
                with self.assertRaises(ValueError):
                    momento_ordinario(self.valores, orden)
        for orden in (True, 1.5):
            with self.subTest(orden=orden):
                with self.assertRaises(TypeError):
                    momento_ordinario(self.valores, orden)


class UniformeTeoricaTest(unittest.TestCase):
    def test_valores_teoricos(self) -> None:
        self.assertEqual(
            momentos_teoricos_uniforme(4),
            [0.5, 1.0 / 3.0, 0.25, 0.2],
        )
        resumen = resumen_uniforme_teorica(4)
        self.assertIsNone(resumen["n"])
        self.assertEqual(resumen["media"], 0.5)
        self.assertEqual(resumen["varianza"], 1.0 / 12.0)
        self.assertEqual(resumen["asimetria_fisher_pearson"], 0.0)
        self.assertEqual(resumen["curtosis_pearson"], 1.8)
        self.assertEqual(resumen["exceso_curtosis"], -1.2)


class BaselineMomentosTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.baseline = json.loads(
            (DATA_DIR / "momentos_baseline.json").read_text(encoding="utf-8")
        )
        cls.muestras = construir_muestras()

    def test_cuatro_muestras_tienen_n_1000(self) -> None:
        self.assertEqual(
            list(self.muestras),
            ["logistico", "tienda", "r30_columnas", "r30_filas"],
        )
        for nombre, valores in self.muestras.items():
            with self.subTest(nombre=nombre):
                self.assertEqual(len(valores), 1000)

    def test_resumenes_y_fingerprints_exactos(self) -> None:
        for nombre, valores in self.muestras.items():
            with self.subTest(nombre=nombre):
                esperado = self.baseline["muestras"][nombre]
                observado = resumen_momentos(valores, 4)
                self.assertEqual(observado, esperado["resumen"])
                self.assertEqual(
                    _fingerprint(valores),
                    esperado["fingerprint"]["sha256"],
                )


if __name__ == "__main__":
    unittest.main()
