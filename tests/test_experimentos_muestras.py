"""Pruebas del experimento reproducible que construye las muestras."""

import hashlib
import json
import unittest
from pathlib import Path

import numpy as np

from regenerar_coleccionista import SEED as SEED_HISTORICA
from regenerar_coleccionista import construir_muestras as construir_historica
from regenerar_coleccionista import muestra_logistica as logistica_historica
from regenerar_coleccionista import muestra_tienda as tienda_historica
from regenerar_coleccionista import muestras_regla_30 as r30_historica
from tesis_generacion.experimentos import (
    FACTOR_TIENDA,
    NUM_CELDAS,
    NUM_ITERACIONES,
    NUM_VALORES,
    SEED,
    construir_muestras,
    muestra_logistica,
    muestra_tienda,
    muestras_regla_30,
)


DATA_DIR = Path(__file__).resolve().parent / "data"


def _cargar_baseline() -> dict:
    return json.loads(
        (DATA_DIR / "coleccionista_baseline.json").read_text(encoding="utf-8")
    )["muestras"]


def _fingerprint(valores: np.ndarray) -> str:
    muestra = np.asarray(valores, dtype=np.dtype("<f8"))
    return hashlib.sha256(muestra.tobytes(order="C")).hexdigest()


class ParametrosExperimentoTest(unittest.TestCase):
    def test_parametros_historicos(self) -> None:
        self.assertEqual(SEED, 2024)
        self.assertEqual(NUM_VALORES, 1000)
        self.assertEqual(NUM_ITERACIONES, 1000)
        self.assertEqual(NUM_CELDAS, 1000)
        self.assertEqual(FACTOR_TIENDA, 1.999)


class MuestrasExperimentoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.baseline = _cargar_baseline()

    def assertMuestraBaseline(self, nombre: str, muestra: np.ndarray) -> None:
        self.assertIsInstance(muestra, np.ndarray)
        self.assertEqual(len(muestra), 1000)
        self.assertEqual(muestra.dtype, np.dtype(float))
        self.assertTrue(np.all(np.isfinite(muestra)))
        self.assertTrue(np.all((0.0 <= muestra) & (muestra < 1.0)))
        self.assertEqual(
            _fingerprint(muestra),
            self.baseline[nombre]["fingerprint"]["sha256"],
        )

    def test_muestra_logistica(self) -> None:
        self.assertMuestraBaseline("logistico", muestra_logistica())

    def test_muestra_tienda_reproducible(self) -> None:
        primera = muestra_tienda()
        segunda = muestra_tienda()
        self.assertMuestraBaseline("tienda", primera)
        np.testing.assert_array_equal(primera, segunda)

    def test_muestras_regla_30_reproducibles(self) -> None:
        columnas_1, filas_1 = muestras_regla_30()
        columnas_2, filas_2 = muestras_regla_30()
        self.assertMuestraBaseline("r30_columnas", columnas_1)
        self.assertMuestraBaseline("r30_filas", filas_1)
        np.testing.assert_array_equal(columnas_1, columnas_2)
        np.testing.assert_array_equal(filas_1, filas_2)

    def test_construir_muestras_preserva_orden_y_fingerprints(self) -> None:
        muestras = construir_muestras()
        self.assertEqual(
            list(muestras),
            ["logistico", "tienda", "r30_columnas", "r30_filas"],
        )
        for nombre, muestra in muestras.items():
            with self.subTest(nombre=nombre):
                self.assertMuestraBaseline(nombre, muestra)


class CompatibilidadHistoricaTest(unittest.TestCase):
    def test_orquestador_reexporta_api_canonica(self) -> None:
        self.assertEqual(SEED_HISTORICA, SEED)
        self.assertIs(construir_historica, construir_muestras)
        self.assertIs(logistica_historica, muestra_logistica)
        self.assertIs(tienda_historica, muestra_tienda)
        self.assertIs(r30_historica, muestras_regla_30)


if __name__ == "__main__":
    unittest.main()
