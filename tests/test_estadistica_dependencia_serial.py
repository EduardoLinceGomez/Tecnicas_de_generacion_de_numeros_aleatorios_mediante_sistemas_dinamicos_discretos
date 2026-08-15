"""Pruebas de ACF y de la prueba de brechas."""

import unittest

import numpy as np

from tesis_generacion.estadistica.dependencia_serial import (
    autocorrelacion_empirica,
    autocorrelaciones_empiricas,
    pmf_geometrica,
    resumen_autocorrelaciones,
    resumen_brechas,
    tiempos_espera_brechas,
)


class AutocorrelacionTest(unittest.TestCase):
    def test_arreglo_controlado(self) -> None:
        self.assertEqual(autocorrelacion_empirica([1.0, 2.0, 3.0], 1), 0.0)
        self.assertEqual(autocorrelacion_empirica([1.0, 2.0, 3.0], 2), -0.5)
        np.testing.assert_array_equal(
            autocorrelaciones_empiricas([1.0, 2.0, 3.0], [1, 2]),
            [0.0, -0.5],
        )

    def test_resumen(self) -> None:
        self.assertEqual(
            resumen_autocorrelaciones([1.0, 2.0, 3.0], [1, 2]),
            {"abs_rho_1": 0.0, "max_abs_acf": 0.5, "mae_abs_acf": 0.25},
        )

    def test_lags_invalidos_y_varianza_cero(self) -> None:
        for lag in (0, 3):
            with self.subTest(lag=lag):
                with self.assertRaisesRegex(ValueError, "1 <= lag < n"):
                    autocorrelacion_empirica([1.0, 2.0, 3.0], lag)
        with self.assertRaisesRegex(ValueError, "varianza es cero"):
            autocorrelacion_empirica([2.0, 2.0, 2.0], 1)


class BrechasTest(unittest.TestCase):
    def test_tiempos_y_cola_censurada(self) -> None:
        tiempos, cola = tiempos_espera_brechas(
            [0.1, 0.3, 0.4, 0.8, 0.2], 0.2, 0.5
        )
        np.testing.assert_array_equal(tiempos, [2, 1])
        self.assertEqual(cola, 2)

    def test_extremos_del_intervalo_son_abiertos(self) -> None:
        tiempos, cola = tiempos_espera_brechas([0.2, 0.5, 0.3], 0.2, 0.5)
        np.testing.assert_array_equal(tiempos, [3])
        self.assertEqual(cola, 0)

    def test_pmf_geometrica(self) -> None:
        np.testing.assert_allclose(
            pmf_geometrica([1, 2, 3], 0.2), [0.2, 0.16, 0.128]
        )

    def test_resumen_controlado(self) -> None:
        resumen = resumen_brechas([0.1, 0.3, 0.4, 0.8, 0.2], 0.2, 0.5)
        self.assertEqual(resumen["brechas_completas"], 2)
        self.assertEqual(resumen["cola_censurada"], 2)
        self.assertEqual(resumen["media_tiempo_espera"], 1.5)
        self.assertEqual(resumen["maximo_tiempo_espera"], 2)
        self.assertAlmostEqual(resumen["maxima_discrepancia_cdf"], 0.49)
        self.assertAlmostEqual(resumen["mae_cdf"], 0.345)

    def test_rechaza_intervalo_y_caso_sin_exitos(self) -> None:
        with self.assertRaisesRegex(ValueError, "intervalo"):
            tiempos_espera_brechas([0.1], 0.5, 0.2)
        with self.assertRaisesRegex(ValueError, "brechas completas"):
            resumen_brechas([0.1, 0.1], 0.2, 0.5)


if __name__ == "__main__":
    unittest.main()
