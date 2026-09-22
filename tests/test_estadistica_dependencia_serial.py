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
    def test_tiempos_y_racha_final_incompleta(self) -> None:
        tiempos, racha_final = tiempos_espera_brechas(
            [0.1, 0.3, 0.4, 0.8, 0.2], 0.2, 0.5
        )
        np.testing.assert_array_equal(tiempos, [2, 1])
        self.assertEqual(racha_final, 2)

    def test_extremos_del_intervalo_son_abiertos(self) -> None:
        tiempos, racha_final = tiempos_espera_brechas(
            [0.2, 0.5, 0.3], 0.2, 0.5
        )
        np.testing.assert_array_equal(tiempos, [3])
        self.assertEqual(racha_final, 0)

    def test_pmf_geometrica(self) -> None:
        np.testing.assert_allclose(
            pmf_geometrica([1, 2, 3], 0.2), [0.2, 0.16, 0.128]
        )

    def test_resumen_controlado(self) -> None:
        resumen = resumen_brechas([0.1, 0.3, 0.4, 0.8, 0.2], 0.2, 0.5)
        self.assertEqual(resumen["brechas_completas"], 2)
        self.assertEqual(resumen["racha_final_incompleta"], 2)
        self.assertEqual(resumen["media_tiempo_espera"], 1.5)
        self.assertEqual(resumen["maximo_tiempo_espera"], 2)
        self.assertAlmostEqual(resumen["maxima_discrepancia_cdf"], 0.49)
        self.assertAlmostEqual(resumen["mae_cdf"], 0.345)
        self.assertNotIn("maximo_soporte_evaluacion", resumen)

    def test_soporte_comun_extiende_cdf_y_eam_exactamente(self) -> None:
        valores = [0.1, 0.3, 0.4, 0.8, 0.2]
        historico = resumen_brechas(valores, 0.2, 0.5)
        extendido = resumen_brechas(
            valores, 0.2, 0.5, maximo_soporte=4
        )
        # Para W=3,4, mayores que el máximo observado 2, F_emp(W)=1.
        diferencias = [0.2, 0.49, 1.0 - 0.657, 1.0 - 0.7599]
        self.assertEqual(extendido["maximo_tiempo_espera"], 2)
        self.assertEqual(extendido["maximo_soporte_evaluacion"], 4)
        self.assertAlmostEqual(extendido["mae_cdf"], np.mean(diferencias))
        self.assertEqual(
            extendido["maxima_discrepancia_cdf"],
            historico["maxima_discrepancia_cdf"],
        )

    def test_rechaza_soporte_externo_invalido(self) -> None:
        valores = [0.1, 0.3, 0.4, 0.8, 0.2]
        with self.assertRaisesRegex(ValueError, "máximo observado"):
            resumen_brechas(valores, 0.2, 0.5, maximo_soporte=1)
        for invalido in (True, 2.5):
            with self.subTest(maximo_soporte=invalido):
                with self.assertRaisesRegex(TypeError, "entero"):
                    resumen_brechas(
                        valores, 0.2, 0.5, maximo_soporte=invalido
                    )

    def test_rechaza_intervalo_y_caso_sin_exitos(self) -> None:
        with self.assertRaisesRegex(ValueError, "intervalo"):
            tiempos_espera_brechas([0.1], 0.5, 0.2)
        with self.assertRaisesRegex(ValueError, "brechas completas"):
            resumen_brechas([0.1, 0.1], 0.2, 0.5)


if __name__ == "__main__":
    unittest.main()
