"""Contratos científicos de evolución y codificación de Regla 30."""

import hashlib
import json
import unittest
from pathlib import Path

import numpy as np

from tesis_generacion.experimentos import muestras_regla_30
from tesis_generacion.generadores import evolucion_regla30, paso_regla30
from tesis_generacion.transformaciones import (
    codificar_matriz_por_columnas,
    codificar_matriz_por_filas,
    codificar_palabra_binaria,
    factor_normalizacion_binaria,
)


DATA_DIR = Path(__file__).resolve().parent / "data"


def _fingerprint(valores: np.ndarray) -> str:
    muestra = np.asarray(valores, dtype=np.dtype("<f8"))
    return hashlib.sha256(muestra.tobytes(order="C")).hexdigest()


class ReglaLocalTest(unittest.TestCase):
    def test_tabla_estandar_regla_30(self) -> None:
        tabla = {
            (1, 1, 1): 0,
            (1, 1, 0): 0,
            (1, 0, 1): 0,
            (1, 0, 0): 1,
            (0, 1, 1): 1,
            (0, 1, 0): 1,
            (0, 0, 1): 1,
            (0, 0, 0): 0,
        }
        for vecindad, esperado in tabla.items():
            with self.subTest(vecindad=vecindad):
                fila = np.asarray(vecindad, dtype=np.uint8)
                self.assertEqual(int(paso_regla30(fila)[1]), esperado)

    def test_frontera_periodica(self) -> None:
        fila = np.asarray([1, 0, 0, 0], dtype=np.uint8)
        np.testing.assert_array_equal(paso_regla30(fila), [1, 1, 0, 1])

    def test_evolucion_manual_incluye_condicion_inicial(self) -> None:
        inicial = np.asarray([0, 0, 1, 0, 0], dtype=np.uint8)
        esperado = np.asarray(
            [[0, 0, 1, 0, 0], [0, 1, 1, 1, 0], [1, 1, 0, 0, 1]],
            dtype=np.uint8,
        )
        np.testing.assert_array_equal(evolucion_regla30(inicial, 3), esperado)


class CodificacionOrientacionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.matriz = np.asarray(
            [[1, 0, 0, 1], [0, 1, 1, 0], [1, 1, 0, 0]],
            dtype=np.uint8,
        )

    def test_matriz_rectangular_elimina_ambiguedad(self) -> None:
        columnas = codificar_matriz_por_columnas(self.matriz)
        filas = codificar_matriz_por_filas(self.matriz)
        self.assertEqual(columnas.shape, (4,))
        self.assertEqual(filas.shape, (3,))
        np.testing.assert_allclose(columnas, [5 / 7, 3 / 7, 2 / 7, 4 / 7])
        np.testing.assert_allclose(filas, [9 / 15, 6 / 15, 12 / 15])

    def test_orden_bits_y_denominador(self) -> None:
        factor = factor_normalizacion_binaria(2)
        self.assertEqual(codificar_palabra_binaria([1, 0], factor), 2 / 3)
        self.assertEqual(codificar_palabra_binaria([0, 1], factor), 1 / 3)
        self.assertEqual(codificar_palabra_binaria([1, 1], factor), 1.0)

    def test_factor_de_1000_bits_es_finito_y_no_subnormal(self) -> None:
        factor = factor_normalizacion_binaria(1000)
        self.assertTrue(np.isfinite(factor))
        self.assertGreaterEqual(factor, np.finfo(float).tiny)

    def test_fingerprints_canonicos(self) -> None:
        baseline = json.loads(
            (DATA_DIR / "coleccionista_baseline.json").read_text(encoding="utf-8")
        )["muestras"]
        columnas, filas = muestras_regla_30()
        self.assertEqual(
            _fingerprint(columnas),
            baseline["r30_columnas"]["fingerprint"]["sha256"],
        )
        self.assertEqual(
            _fingerprint(filas), baseline["r30_filas"]["fingerprint"]["sha256"]
        )


if __name__ == "__main__":
    unittest.main()
