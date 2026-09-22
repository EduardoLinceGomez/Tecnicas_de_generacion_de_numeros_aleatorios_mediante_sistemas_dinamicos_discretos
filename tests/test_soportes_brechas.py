"""Pruebas de la fuente compartida de mallas de brechas AUT-093."""

import unittest

import numpy as np

from tesis_generacion.estadistica import resumen_brechas, tiempos_espera_brechas
from tesis_generacion.experimentos import (
    construir_comparacion_generadores,
    construir_experimentos_reordenamiento,
)
from tesis_generacion.experimentos.parametros import INTERVALOS_BRECHAS_COMUNES
from tesis_generacion.experimentos.soportes_brechas import (
    calcular_maximos_soporte_brechas_comunes,
    construir_participantes_malla_brechas,
)


class SoportesBrechasComunesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.participantes = construir_participantes_malla_brechas()
        cls.maximos = calcular_maximos_soporte_brechas_comunes()

    def test_incluye_ocho_series_dinamicas_y_minstd(self) -> None:
        self.assertEqual(len(self.participantes), 9)
        self.assertIn("congruencial_minstd_original", self.participantes)
        for nombre in ("logistico", "tienda", "r30_columnas", "r30_filas"):
            self.assertIn(f"{nombre}_original", self.participantes)
            self.assertIn(f"{nombre}_reordenada", self.participantes)

    def test_maximos_dinamicos_sobre_los_nueve_participantes(self) -> None:
        esperados = {}
        for intervalo_id, (alpha, beta) in INTERVALOS_BRECHAS_COMUNES.items():
            esperados[intervalo_id] = max(
                int(np.max(tiempos_espera_brechas(valores, alpha, beta)[0]))
                for valores in self.participantes.values()
            )
        self.assertEqual(self.maximos, esperados)
        self.assertEqual(self.maximos, {"i1": 43, "i2": 26, "i3": 35})
        sin_minstd = {
            nombre: valores
            for nombre, valores in self.participantes.items()
            if nombre != "congruencial_minstd_original"
        }
        maximo_i1_sin_minstd = max(
            int(np.max(tiempos_espera_brechas(valores, 0.1, 0.3)[0]))
            for valores in sin_minstd.values()
        )
        self.assertLess(maximo_i1_sin_minstd, self.maximos["i1"])

    def test_ambos_experimentos_consumen_los_mismos_maximos(self) -> None:
        reordenamiento = construir_experimentos_reordenamiento()
        comparacion = construir_comparacion_generadores()
        clave = "maximos_soporte_evaluacion_brechas"
        self.assertEqual(reordenamiento["parametros"][clave], self.maximos)
        self.assertEqual(comparacion["parametros"][clave], self.maximos)
        for datos in reordenamiento["muestras"].values():
            for intervalo_id, resultados in datos["brechas"].items():
                for estado in ("original", "reordenada"):
                    self.assertEqual(
                        resultados[estado]["maximo_soporte_evaluacion"],
                        self.maximos[intervalo_id],
                    )
        for datos in comparacion["muestras"].values():
            for intervalo_id, brechas in datos["brechas"].items():
                self.assertEqual(
                    brechas["maximo_soporte_evaluacion"],
                    self.maximos[intervalo_id],
                )

    def test_dmax_invariante_y_eam_exacto_en_malla_comun(self) -> None:
        for nombre, valores in self.participantes.items():
            for intervalo_id, (alpha, beta) in INTERVALOS_BRECHAS_COMUNES.items():
                with self.subTest(nombre=nombre, intervalo=intervalo_id):
                    historico = resumen_brechas(valores, alpha, beta)
                    nuevo = resumen_brechas(
                        valores,
                        alpha,
                        beta,
                        maximo_soporte=self.maximos[intervalo_id],
                    )
                    self.assertEqual(
                        nuevo["maxima_discrepancia_cdf"],
                        historico["maxima_discrepancia_cdf"],
                    )
                    tiempos = tiempos_espera_brechas(valores, alpha, beta)[0]
                    soporte = np.arange(1, self.maximos[intervalo_id] + 1)
                    empirica = np.searchsorted(
                        np.sort(tiempos), soporte, side="right"
                    ) / tiempos.size
                    teorica = 1.0 - (1.0 - (beta - alpha)) ** soporte
                    self.assertEqual(empirica[-1], 1.0)
                    self.assertEqual(
                        nuevo["mae_cdf"],
                        float(np.mean(np.abs(empirica - teorica))),
                    )


if __name__ == "__main__":
    unittest.main()
