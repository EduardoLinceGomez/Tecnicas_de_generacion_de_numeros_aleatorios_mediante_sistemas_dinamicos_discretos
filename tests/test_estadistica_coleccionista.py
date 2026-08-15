"""Pruebas unitarias de la estadística canónica del coleccionista."""

import json
import unittest
from pathlib import Path

from coleccionista import (
    cdf_coleccionista as cdf_historica,
    longitudes_coleccionista as longitudes_historicas,
    media_teorica_coleccionista as media_historica,
    pmf_coleccionista as pmf_historica,
)
from regenerar_coleccionista import construir_muestras
from tesis_generacion.estadistica import (
    cdf_coleccionista,
    longitudes_coleccionista,
    media_teorica_coleccionista,
    metricas_coleccionista,
    pmf_coleccionista,
)


DATA_DIR = Path(__file__).resolve().parent / "data"


class LongitudesColeccionistaTest(unittest.TestCase):
    def test_bloque_completo_y_cola_censurada(self) -> None:
        valores = [
            0.05,
            0.15,
            0.25,
            0.35,
            0.45,
            0.55,
            0.65,
            0.75,
            0.85,
            0.95,
            0.0,
        ]
        longitudes, cola = longitudes_coleccionista(valores, precision=1)
        self.assertEqual(longitudes, [10])
        self.assertEqual(cola, 1)


class DistribucionColeccionistaTest(unittest.TestCase):
    def test_cdf_conocida_y_monotona(self) -> None:
        self.assertEqual(cdf_coleccionista(9), 0.0)
        self.assertAlmostEqual(cdf_coleccionista(10), 0.00036288, places=14)
        valores = [cdf_coleccionista(m) for m in range(0, 31)]
        self.assertTrue(
            all(
                anterior <= siguiente
                for anterior, siguiente in zip(valores, valores[1:])
            )
        )

    def test_pmf_como_diferencia_de_cdf(self) -> None:
        self.assertAlmostEqual(pmf_coleccionista(10), 0.00036288, places=14)
        for m in (10, 11, 15, 20, 30):
            with self.subTest(m=m):
                self.assertEqual(
                    pmf_coleccionista(m),
                    cdf_coleccionista(m) - cdf_coleccionista(m - 1),
                )

    def test_media_teorica(self) -> None:
        esperada = 10 * sum(1 / j for j in range(1, 11))
        self.assertAlmostEqual(
            media_teorica_coleccionista(10), esperada, places=15
        )


class MetricasColeccionistaTest(unittest.TestCase):
    def test_muestra_logistica_contra_baseline(self) -> None:
        baseline = json.loads(
            (DATA_DIR / "coleccionista_baseline.json").read_text(
                encoding="utf-8"
            )
        )["muestras"]["logistico"]
        muestra = construir_muestras()["logistico"]
        _, metricas = metricas_coleccionista(muestra)

        campos_enteros = {
            "numero_u": "n_valores",
            "total_digitos": "n_digitos",
            "bloques_completos": "bloques",
            "cola_censurada": "cola",
            "minimo": "minimo",
            "maximo": "maximo",
            "mediana": "mediana",
        }
        campos_float = {
            "media": "media",
            "distancia_maxima_cdf": "distancia_maxima_cdf",
            "mae_cdf": "mae_cdf",
        }
        for actual, esperado in campos_enteros.items():
            self.assertEqual(metricas[actual], baseline[esperado])
        for actual, esperado in campos_float.items():
            self.assertAlmostEqual(
                metricas[actual], baseline[esperado], delta=1e-12
            )


class CompatibilidadHistoricaTest(unittest.TestCase):
    def test_adaptador_reexporta_objetos_canonicos(self) -> None:
        self.assertIs(cdf_historica, cdf_coleccionista)
        self.assertIs(longitudes_historicas, longitudes_coleccionista)
        self.assertIs(media_historica, media_teorica_coleccionista)
        self.assertIs(pmf_historica, pmf_coleccionista)


if __name__ == "__main__":
    unittest.main()
