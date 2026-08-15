"""Pruebas de la visualización reproducible del coleccionista."""

import json
import re
import tempfile
import unittest
from pathlib import Path

import numpy as np

from regenerar_coleccionista import regenerar as regenerar_historica
from regenerar_coleccionista import (
    regenerar_muestra as regenerar_muestra_historica,
)
from regenerar_coleccionista import validar_muestra as validar_muestra_historica
from tesis_generacion.estadistica import cdf_coleccionista
from tesis_generacion.experimentos import muestra_logistica
from tesis_generacion.visualizacion import (
    ETIQUETAS,
    NOMBRES_FIGURAS,
    rango_grafica,
    regenerar,
    regenerar_muestra,
    validar_muestra,
)


DATA_DIR = Path(__file__).resolve().parent / "data"
NOMBRES_PNG = {
    "Log_dens_CCT.png",
    "R30_col_densCCT.png",
    "R30_col_distCCT.png",
    "R30_fila_densCCT.png",
    "R30_fila_distCCT.png",
    "Tent_dens_CCT.png",
    "Tent_dsit_CCT.png",
    "log_dist_CCT.png",
}


def _baseline() -> dict:
    return json.loads(
        (DATA_DIR / "coleccionista_baseline.json").read_text(encoding="utf-8")
    )["muestras"]


def _comprobar_metricas(
    caso: unittest.TestCase, observadas: dict, esperadas: dict
) -> None:
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
        caso.assertEqual(observadas[actual], esperadas[esperado])
    for actual, esperado in campos_float.items():
        caso.assertAlmostEqual(
            observadas[actual], esperadas[esperado], delta=1e-12
        )


class ContratoVisualTest(unittest.TestCase):
    def test_nombres_y_etiquetas_historicos(self) -> None:
        self.assertEqual(
            NOMBRES_FIGURAS,
            {
                "logistico": ("log_dist_CCT.png", "Log_dens_CCT.png"),
                "tienda": ("Tent_dsit_CCT.png", "Tent_dens_CCT.png"),
                "r30_columnas": (
                    "R30_col_distCCT.png",
                    "R30_col_densCCT.png",
                ),
                "r30_filas": (
                    "R30_fila_distCCT.png",
                    "R30_fila_densCCT.png",
                ),
            },
        )
        self.assertEqual(
            ETIQUETAS,
            {
                "logistico": "Mapeo logístico transformado",
                "tienda": "Mapeo tienda",
                "r30_columnas": "Regla 30 por columnas",
                "r30_filas": "Regla 30 por filas",
            },
        )

    def test_rango_grafica(self) -> None:
        valores = rango_grafica([10, 20, 30])
        self.assertEqual(valores[0], 10)
        self.assertTrue(np.issubdtype(valores.dtype, np.integer))
        limite = int(valores[-1])
        self.assertGreaterEqual(cdf_coleccionista(limite), 0.9999)
        self.assertLess(cdf_coleccionista(limite - 1), 0.9999)

    def test_validacion_preserva_errores_historicos(self) -> None:
        casos = (
            ("corta", np.zeros(999), "corta: se esperaban 1000 valores"),
            ("nan", np.full(1000, np.nan), "nan: contiene NaN o infinito"),
            ("inf", np.full(1000, np.inf), "inf: contiene NaN o infinito"),
            (
                "negativa",
                np.full(1000, -0.1),
                "negativa: contiene valores fuera de [0,1)",
            ),
            (
                "uno",
                np.ones(1000),
                "uno: contiene valores fuera de [0,1)",
            ),
        )
        for nombre, valores, mensaje in casos:
            with self.subTest(nombre=nombre):
                with self.assertRaisesRegex(
                    ValueError,
                    f"^{re.escape(mensaje)}$",
                ):
                    validar_muestra(nombre, valores)


class RegeneracionVisualTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.baseline = _baseline()

    def test_regenerar_muestra_logistica(self) -> None:
        with tempfile.TemporaryDirectory(prefix="visual-logistica-") as temporal:
            directorio = Path(temporal)
            metricas = regenerar_muestra(
                "logistico", muestra_logistica(), directorio
            )
            self.assertEqual(
                {ruta.name for ruta in directorio.iterdir()},
                {"log_dist_CCT.png", "Log_dens_CCT.png"},
            )
            _comprobar_metricas(self, metricas, self.baseline["logistico"])

    def test_nombre_invalido(self) -> None:
        with tempfile.TemporaryDirectory(prefix="visual-invalida-") as temporal:
            with self.assertRaisesRegex(
                ValueError, "^muestra desconocida: inexistente$"
            ):
                regenerar_muestra(
                    "inexistente", muestra_logistica(), Path(temporal)
                )

    def test_regenerar_todas_las_figuras(self) -> None:
        with tempfile.TemporaryDirectory(prefix="visual-todas-") as temporal:
            directorio = Path(temporal)
            resumen = regenerar(directorio)
            self.assertEqual(
                list(resumen),
                ["logistico", "tienda", "r30_columnas", "r30_filas"],
            )
            self.assertEqual(
                {ruta.name for ruta in directorio.iterdir()}, NOMBRES_PNG
            )
            for nombre, metricas in resumen.items():
                with self.subTest(nombre=nombre):
                    _comprobar_metricas(self, metricas, self.baseline[nombre])


class CompatibilidadHistoricaTest(unittest.TestCase):
    def test_adaptador_reexporta_visualizacion_canonica(self) -> None:
        self.assertIs(regenerar_historica, regenerar)
        self.assertIs(regenerar_muestra_historica, regenerar_muestra)
        self.assertIs(validar_muestra_historica, validar_muestra)


if __name__ == "__main__":
    unittest.main()
