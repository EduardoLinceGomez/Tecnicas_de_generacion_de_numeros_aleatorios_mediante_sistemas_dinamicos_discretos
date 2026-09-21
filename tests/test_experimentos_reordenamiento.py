"""Regresión científica de permutaciones y diagnósticos del bloque 12."""

import json
import unittest
from pathlib import Path

import numpy as np

import tesis_generacion.experimentos.reordenamiento as modulo_reordenamiento
from tesis_generacion.experimentos.parametros import (
    INTERVALOS_BRECHAS_COMUNES,
    LONGITUD_INTERVALO_BRECHAS,
    PROBABILIDAD_BRECHAS,
    validar_intervalos_brechas_comunes,
)
from tesis_generacion.experimentos.reordenamiento import (
    LAGS_REORDENAMIENTO,
    SEED_REORDENAMIENTO,
    construir_experimentos_reordenamiento,
)


DATA_DIR = Path(__file__).resolve().parent / "data"


def _baseline() -> dict:
    return json.loads(
        (DATA_DIR / "reordenamiento_baseline.json").read_text(encoding="utf-8")
    )


class ExperimentosReordenamientoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.baseline = _baseline()
        cls.experimentos = construir_experimentos_reordenamiento()

    def test_parametros_y_permutaciones_reproducibles(self) -> None:
        self.assertEqual(SEED_REORDENAMIENTO, 2024)
        self.assertEqual(LAGS_REORDENAMIENTO, tuple(range(1, 21)))
        self.assertEqual(
            INTERVALOS_BRECHAS_COMUNES,
            {"i1": (0.1, 0.3), "i2": (0.4, 0.6), "i3": (0.7, 0.9)},
        )
        self.assertEqual(LONGITUD_INTERVALO_BRECHAS, 0.2)
        self.assertEqual(PROBABILIDAD_BRECHAS, 0.2)
        self.assertEqual(
            self.experimentos["parametros"], self.baseline["parametros"]
        )
        self.assertFalse(hasattr(modulo_reordenamiento, "INTERVALOS_BRECHAS"))
        for clave, esperado in self.baseline["permutaciones"].items():
            observado = self.experimentos["permutaciones"][clave]
            resumen = self.experimentos["resumen_permutaciones"][clave]
            self.assertEqual(observado["x0"], esperado["x0"])
            self.assertEqual(observado["seed"], esperado["seed"])
            self.assertEqual(
                resumen["fingerprint_auxiliar"]["sha256"],
                esperado["fingerprint_auxiliar"],
            )
            self.assertEqual(
                resumen["fingerprint_permutacion"]["sha256"],
                esperado["fingerprint_permutacion"],
            )
            np.testing.assert_array_equal(
                np.sort(observado["indices"]), np.arange(1000)
            )
            self.assertEqual(
                observado["indices"][:10].tolist(),
                esperado["primeros_10_indices"],
            )
            self.assertEqual(
                observado["indices"][-10:].tolist(),
                esperado["ultimos_10_indices"],
            )

    def test_validacion_del_protocolo_comun(self) -> None:
        self.assertEqual(
            validar_intervalos_brechas_comunes(INTERVALOS_BRECHAS_COMUNES),
            0.2,
        )
        with self.assertRaises(ValueError):
            validar_intervalos_brechas_comunes(
                {"i1": (0.1, 0.3), "i2": (0.4, 0.6)}
            )
        with self.assertRaises(ValueError):
            validar_intervalos_brechas_comunes(
                {"i1": (0.1, 0.3), "i2": (0.4, 0.7), "i3": (0.7, 0.9)}
            )

    def test_fingerprints_y_conservacion_marginal(self) -> None:
        for nombre, esperado in self.baseline["muestras"].items():
            observado = self.experimentos["muestras"][nombre]
            with self.subTest(nombre=nombre):
                self.assertEqual(len(observado["original"]), 1000)
                self.assertEqual(len(observado["reordenada"]), 1000)
                self.assertEqual(
                    observado["fingerprint_original"]["sha256"],
                    esperado["fingerprint_original"],
                )
                self.assertEqual(
                    observado["fingerprint_reordenada"]["sha256"],
                    esperado["fingerprint_reordenada"],
                )
                self.assertEqual(observado["permutacion"], esperado["permutacion"])
                conservacion = observado["conservacion_marginal"]
                self.assertTrue(conservacion["n_identico"])
                self.assertTrue(conservacion["multiconjunto_identico"])
                self.assertTrue(conservacion["histograma_40_bins_identico"])
                self.assertTrue(conservacion["cdf_empirica_identica"])
                self.assertLessEqual(
                    conservacion["maxima_diferencia_momentos_m1_m4"], 2e-16
                )

    def test_metricas_exactas(self) -> None:
        campos_acf = ("abs_rho_1", "max_abs_acf", "mae_abs_acf")
        campos_brechas = (
            "brechas_completas",
            "racha_final_incompleta",
            "media_tiempo_espera",
            "maximo_tiempo_espera",
            "maxima_discrepancia_cdf",
            "mae_cdf",
        )
        for nombre, esperado in self.baseline["muestras"].items():
            observado = self.experimentos["muestras"][nombre]
            for sufijo in ("original", "reordenada"):
                with self.subTest(nombre=nombre, estado=sufijo):
                    self.assertEqual(
                        [observado[f"acf_{sufijo}"][campo] for campo in campos_acf],
                        esperado[f"acf_{sufijo}"],
                    )
            self.assertEqual(tuple(observado["brechas"]), ("i1", "i2", "i3"))
            for intervalo_id, resultados in observado["brechas"].items():
                self.assertEqual(
                    resultados["intervalo"],
                    list(INTERVALOS_BRECHAS_COMUNES[intervalo_id]),
                )
                self.assertEqual(resultados["original"]["p"], 0.2)
                self.assertEqual(resultados["reordenada"]["p"], 0.2)
                self.assertEqual(
                    resultados["original"]["brechas_completas"],
                    resultados["reordenada"]["brechas_completas"],
                )
                for estado in ("original", "reordenada"):
                    with self.subTest(
                        nombre=nombre,
                        intervalo=intervalo_id,
                        estado=estado,
                    ):
                        self.assertEqual(
                            [resultados[estado][campo] for campo in campos_brechas],
                            esperado["brechas"][intervalo_id][estado],
                        )

    def test_existen_24_resumenes_de_brechas(self) -> None:
        self.assertEqual(
            sum(
                2 * len(datos["brechas"])
                for datos in self.experimentos["muestras"].values()
            ),
            24,
        )


if __name__ == "__main__":
    unittest.main()
