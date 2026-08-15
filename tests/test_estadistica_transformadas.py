"""Pruebas de FGM y función característica empíricas."""

import hashlib
import json
import math
import unittest
from pathlib import Path

import numpy as np

from tesis_generacion.estadistica import (
    fgm_empirica,
    fgm_uniforme,
    funcion_caracteristica_empirica,
    funcion_caracteristica_uniforme,
    metricas_error_transformada,
)
from tesis_generacion.experimentos import construir_muestras
from tesis_generacion.visualizacion.transformadas import T_FC, T_FGM


DATA_DIR = Path(__file__).resolve().parent / "data"


class TransformadasControladasTest(unittest.TestCase):
    def setUp(self) -> None:
        self.valores = np.asarray([0.0, 1.0])

    def test_fgm_empirica_es_promedio_de_exponenciales(self) -> None:
        self.assertEqual(fgm_empirica(self.valores, 0.0), 1.0)
        observado = fgm_empirica(self.valores, [0.0, 1.0])
        esperado = np.asarray([1.0, (1.0 + math.e) / 2.0])
        np.testing.assert_allclose(observado, esperado, rtol=0.0, atol=1e-15)

    def test_funcion_caracteristica_empirica_es_compleja(self) -> None:
        self.assertEqual(
            funcion_caracteristica_empirica(self.valores, 0.0), 1.0 + 0.0j
        )
        observado = funcion_caracteristica_empirica(self.valores, [0.0, 1.0])
        esperado = np.asarray([1.0 + 0.0j, (1.0 + np.exp(1j)) / 2.0])
        np.testing.assert_allclose(observado, esperado, rtol=0.0, atol=1e-15)

    def test_transformadas_uniformes_y_caso_t_cero(self) -> None:
        self.assertEqual(fgm_uniforme(0.0), 1.0)
        self.assertEqual(funcion_caracteristica_uniforme(0.0), 1.0 + 0.0j)
        np.testing.assert_allclose(
            fgm_uniforme([0.0, 1e-12, 1.0]),
            [1.0, np.expm1(1e-12) / 1e-12, np.expm1(1.0)],
            rtol=0.0,
            atol=1e-15,
        )
        esperado_fc = np.expm1(1j) / 1j
        self.assertAlmostEqual(
            funcion_caracteristica_uniforme(1.0).real, esperado_fc.real
        )
        self.assertAlmostEqual(
            funcion_caracteristica_uniforme(1.0).imag, esperado_fc.imag
        )

    def test_propiedades_de_la_funcion_caracteristica_uniforme(self) -> None:
        t = np.linspace(-20.0, 20.0, 121)
        positiva = np.asarray(funcion_caracteristica_uniforme(t))
        negativa = np.asarray(funcion_caracteristica_uniforme(-t))
        np.testing.assert_allclose(
            negativa, np.conjugate(positiva), rtol=0.0, atol=1e-15
        )
        self.assertTrue(np.all(np.abs(positiva) <= 1.0 + 1e-15))

    def test_metricas_usan_modulo_complejo(self) -> None:
        observado = np.asarray([1.0 + 1.0j, 2.0 + 0.0j])
        teorico = np.asarray([1.0 + 0.0j, 0.0 + 0.0j])
        self.assertEqual(
            metricas_error_transformada(observado, teorico),
            {"maxima_diferencia_absoluta": 2.0, "mae": 1.5},
        )

    def test_validaciones(self) -> None:
        for funcion in (fgm_empirica, funcion_caracteristica_empirica):
            with self.subTest(funcion=funcion.__name__):
                with self.assertRaisesRegex(ValueError, "vacío"):
                    funcion([], 0.0)
                with self.assertRaisesRegex(ValueError, "NaN o infinito"):
                    funcion([0.0, np.nan], 0.0)
                with self.assertRaisesRegex(ValueError, "unidimensional"):
                    funcion([[0.0, 1.0]], 0.0)
                with self.assertRaisesRegex(ValueError, "t contiene"):
                    funcion([0.0, 1.0], np.inf)
        with self.assertRaisesRegex(ValueError, "misma forma"):
            metricas_error_transformada([1.0], [1.0, 2.0])


class BaselineTransformadasTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.baseline = json.loads(
            (DATA_DIR / "transformadas_baseline.json").read_text(
                encoding="utf-8"
            )
        )
        cls.muestras = construir_muestras()

    def test_mallas_comunes(self) -> None:
        np.testing.assert_array_equal(T_FGM, np.linspace(0.0, 15.0, 40))
        np.testing.assert_array_equal(T_FC, np.linspace(0.0, 20.0, 60))

    def test_baseline_de_cuatro_muestras(self) -> None:
        for nombre, valores in self.muestras.items():
            with self.subTest(nombre=nombre):
                esperado = self.baseline["muestras"][nombre]
                muestra_le = np.ascontiguousarray(valores, dtype=np.dtype("<f8"))
                fingerprint = hashlib.sha256(
                    muestra_le.tobytes(order="C")
                ).hexdigest()
                self.assertEqual(len(valores), 1000)
                self.assertEqual(fingerprint, esperado["fingerprint"]["sha256"])
                fgm_observada = fgm_empirica(valores, T_FGM)
                fc_observada = funcion_caracteristica_empirica(valores, T_FC)
                self.assertEqual(
                    metricas_error_transformada(
                        fgm_observada, fgm_uniforme(T_FGM)
                    ),
                    esperado["fgm"],
                )
                self.assertEqual(
                    metricas_error_transformada(
                        fc_observada, funcion_caracteristica_uniforme(T_FC)
                    ),
                    esperado["funcion_caracteristica"],
                )

    def test_puntos_de_control_exactos(self) -> None:
        controles_fgm = self.baseline["puntos_control"]["fgm"]
        indices_fgm = controles_fgm["indices"]
        np.testing.assert_array_equal(T_FGM[indices_fgm], controles_fgm["t"])
        np.testing.assert_array_equal(
            np.asarray(fgm_uniforme(T_FGM))[indices_fgm],
            controles_fgm["teorica"],
        )

        controles_fc = self.baseline["puntos_control"][
            "funcion_caracteristica"
        ]
        indices_fc = controles_fc["indices"]
        np.testing.assert_array_equal(T_FC[indices_fc], controles_fc["t"])
        teorica_fc = np.asarray(
            [complex(valor["real"], valor["imag"]) for valor in controles_fc["teorica"]]
        )
        np.testing.assert_array_equal(
            np.asarray(funcion_caracteristica_uniforme(T_FC))[indices_fc],
            teorica_fc,
        )

        for nombre, valores in self.muestras.items():
            with self.subTest(nombre=nombre):
                np.testing.assert_array_equal(
                    np.asarray(fgm_empirica(valores, T_FGM))[indices_fgm],
                    controles_fgm["muestras"][nombre],
                )
                esperado_fc = np.asarray(
                    [
                        complex(valor["real"], valor["imag"])
                        for valor in controles_fc["muestras"][nombre]
                    ]
                )
                np.testing.assert_array_equal(
                    np.asarray(funcion_caracteristica_empirica(valores, T_FC))[
                        indices_fc
                    ],
                    esperado_fc,
                )


if __name__ == "__main__":
    unittest.main()
