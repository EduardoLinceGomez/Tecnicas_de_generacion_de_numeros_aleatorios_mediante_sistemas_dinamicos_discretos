"""Pruebas de la malla común del coleccionista aprobada en AUT-105."""

from bisect import bisect_right
import hashlib
import json
from pathlib import Path
import statistics
import unittest
from unittest.mock import patch

import numpy as np

from tesis_generacion.estadistica import (
    cdf_coleccionista,
    longitudes_coleccionista,
    metricas_coleccionista,
)
from tesis_generacion.experimentos import (
    MUESTRAS_COLECCIONISTA,
    calcular_maximo_soporte_coleccionista_comun,
    construir_participantes_malla_coleccionista,
)


DATA_DIR = Path(__file__).resolve().parent / "data"


class SoporteColeccionistaComunTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.baseline = json.loads(
            (DATA_DIR / "coleccionista_baseline.json").read_text(
                encoding="utf-8"
            )
        )["muestras"]
        cls.muestras = construir_participantes_malla_coleccionista()
        cls.maximo_soporte = calcular_maximo_soporte_coleccionista_comun(
            cls.muestras
        )

    def test_incluye_solo_las_cuatro_muestras_originales(self) -> None:
        self.assertEqual(tuple(self.muestras), MUESTRAS_COLECCIONISTA)
        self.assertEqual(
            MUESTRAS_COLECCIONISTA,
            ("logistico", "tienda", "r30_columnas", "r30_filas"),
        )
        self.assertFalse(
            any(
                "minstd" in nombre or "reorden" in nombre
                for nombre in self.muestras
            )
        )

    def test_maximo_soporte_se_deriva_dinamicamente(self) -> None:
        maximos_observados = {
            nombre: max(longitudes_coleccionista(valores)[0])
            for nombre, valores in self.muestras.items()
        }
        self.assertEqual(self.maximo_soporte, max(maximos_observados.values()))

        participantes_ficticios = {
            nombre: [indice]
            for indice, nombre in enumerate(MUESTRAS_COLECCIONISTA)
        }
        longitudes_ficticias = (
            ([10, 20], 0),
            ([12, 37], 0),
            ([15, 31], 0),
            ([11, 29], 0),
        )
        with patch(
            "tesis_generacion.experimentos.soportes_coleccionista."
            "longitudes_coleccionista",
            side_effect=longitudes_ficticias,
        ):
            self.assertEqual(
                calcular_maximo_soporte_coleccionista_comun(
                    participantes_ficticios
                ),
                37,
            )

    def test_eam_extendido_exacto_y_dmax_invariante(self) -> None:
        for nombre, valores in self.muestras.items():
            with self.subTest(muestra=nombre):
                longitudes, historicas = metricas_coleccionista(valores)
                _, nuevas = metricas_coleccionista(
                    valores, maximo_soporte=self.maximo_soporte
                )
                ordenadas = sorted(longitudes)
                errores = [
                    abs(
                        bisect_right(ordenadas, m) / len(ordenadas)
                        - cdf_coleccionista(m)
                    )
                    for m in range(10, self.maximo_soporte + 1)
                ]

                self.assertEqual(nuevas["mae_cdf"], statistics.fmean(errores))
                self.assertEqual(
                    nuevas["distancia_maxima_cdf"], max(errores)
                )
                self.assertEqual(
                    nuevas["distancia_maxima_cdf"],
                    historicas["distancia_maxima_cdf"],
                )
                self.assertEqual(
                    nuevas["maximo_soporte_evaluacion"], self.maximo_soporte
                )
                self.assertEqual(nuevas["maximo"], max(longitudes))
                if historicas["maximo"] < self.maximo_soporte:
                    self.assertEqual(
                        bisect_right(ordenadas, self.maximo_soporte)
                        / len(ordenadas),
                        1.0,
                    )

    def test_rechaza_soporte_externo_invalido(self) -> None:
        valores = self.muestras["logistico"]
        maximo_observado = metricas_coleccionista(valores)[1]["maximo"]
        for invalido in (True, 91.0, "91"):
            with self.subTest(maximo_soporte=invalido):
                with self.assertRaisesRegex(
                    TypeError, "^maximo_soporte debe ser un entero$"
                ):
                    metricas_coleccionista(
                        valores, maximo_soporte=invalido
                    )
        with self.assertRaisesRegex(
            ValueError,
            "^maximo_soporte debe ser mayor o igual que el máximo observado$",
        ):
            metricas_coleccionista(
                valores, maximo_soporte=maximo_observado - 1
            )

    def test_r30_conserva_exactamente_el_eam_historico(self) -> None:
        for nombre in ("r30_columnas", "r30_filas"):
            with self.subTest(muestra=nombre):
                historicas = metricas_coleccionista(self.muestras[nombre])[1]
                nuevas = metricas_coleccionista(
                    self.muestras[nombre],
                    maximo_soporte=self.maximo_soporte,
                )[1]
                self.assertEqual(nuevas["mae_cdf"], historicas["mae_cdf"])
                self.assertEqual(
                    nuevas["mae_cdf"], self.baseline[nombre]["mae_cdf"]
                )

    def test_fingerprints_e_invariantes_no_cambian(self) -> None:
        campos_invariantes = (
            "numero_u",
            "total_digitos",
            "bloques_completos",
            "cola_censurada",
            "minimo",
            "maximo",
            "media",
            "mediana",
            "media_teorica",
            "diferencia_media",
        )
        for nombre, muestra in self.muestras.items():
            with self.subTest(muestra=nombre):
                valores = np.asarray(muestra, dtype=np.dtype("<f8"))
                fingerprint = self.baseline[nombre]["fingerprint"]
                self.assertEqual(
                    hashlib.sha256(valores.tobytes(order="C")).hexdigest(),
                    fingerprint["sha256"],
                )
                historicas = metricas_coleccionista(valores)[1]
                nuevas = metricas_coleccionista(
                    valores, maximo_soporte=self.maximo_soporte
                )[1]
                self.assertNotIn(
                    "maximo_soporte_evaluacion", historicas
                )
                for campo in campos_invariantes:
                    self.assertEqual(nuevas[campo], historicas[campo])


if __name__ == "__main__":
    unittest.main()
