"""Pruebas de CDF y discrepancias para el bloque 11."""

import json
import unittest
from pathlib import Path

import numpy as np

from tesis_generacion.estadistica.invariancia import (
    cdf_beta_medio,
    cdf_uniforme_01,
    metricas_discrepancia_cdf,
)
from tesis_generacion.experimentos.invariancia import (
    construir_experimentos_invariancia,
)


DATA_DIR = Path(__file__).resolve().parent / "data"


def _baseline() -> dict:
    return json.loads(
        (DATA_DIR / "invariancia_baseline.json").read_text(encoding="utf-8")
    )


class EstadisticaInvarianciaTest(unittest.TestCase):
    def test_cdf_uniforme(self) -> None:
        np.testing.assert_array_equal(
            cdf_uniforme_01([-1.0, 0.0, 0.25, 1.0, 2.0]),
            [0.0, 0.0, 0.25, 1.0, 1.0],
        )

    def test_cdf_beta_medio(self) -> None:
        np.testing.assert_allclose(
            cdf_beta_medio([-1.0, 0.0, 0.5, 1.0, 2.0]),
            [0.0, 0.0, 0.5, 1.0, 1.0],
            rtol=0.0,
            atol=1e-15,
        )

    def test_discrepancia_controlada(self) -> None:
        metricas = metricas_discrepancia_cdf(
            [0.25, 0.75], cdf_uniforme_01, np.asarray([0.25, 0.5, 0.75])
        )
        self.assertEqual(metricas["maxima_discrepancia_cdf"], 0.25)
        self.assertAlmostEqual(metricas["mae_cdf"], 1.0 / 6.0)

    def test_metricas_exactas_del_baseline(self) -> None:
        baseline = _baseline()["experimentos"]
        experimentos = construir_experimentos_invariancia()
        objetivos = {
            "logistico_r4": cdf_beta_medio,
            "tienda_ideal_2": cdf_uniforme_01,
            "tienda_diagnostico_1_999": cdf_uniforme_01,
        }
        for nombre, evolucion in experimentos.items():
            for iteracion, valores in enumerate(evolucion):
                with self.subTest(nombre=nombre, iteracion=iteracion):
                    observado = metricas_discrepancia_cdf(
                        valores, objetivos[nombre]
                    )
                    esperado = baseline[nombre]["metricas_por_iteracion"][
                        iteracion
                    ]
                    self.assertEqual(observado, esperado)

    def test_validaciones(self) -> None:
        with self.assertRaisesRegex(ValueError, "vacía"):
            metricas_discrepancia_cdf([], cdf_uniforme_01)
        with self.assertRaisesRegex(ValueError, "NaN"):
            metricas_discrepancia_cdf([0.0, np.nan], cdf_uniforme_01)
        with self.assertRaisesRegex(ValueError, "malla"):
            metricas_discrepancia_cdf([0.0], cdf_uniforme_01, np.asarray([]))


if __name__ == "__main__":
    unittest.main()
