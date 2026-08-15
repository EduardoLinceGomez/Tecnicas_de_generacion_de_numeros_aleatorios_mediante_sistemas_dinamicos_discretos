"""Pruebas unitarias de las transformaciones puras."""

import math
import unittest

import numpy as np
from scipy.stats import beta

from coleccionista import PRECISION_DECIMAL as PRECISION_ANTIGUA
from coleccionista import extraer_digitos as extraer_digitos_antiguo
from tesis_generacion.transformaciones import (
    PRECISION_DECIMAL,
    codificar_palabra_binaria,
    extraer_digitos,
    factor_normalizacion_binaria,
    uniformizar_beta,
)


class UniformizacionBetaTest(unittest.TestCase):
    def test_evaluacion_historica_elemento_a_elemento(self) -> None:
        valores = np.asarray([0.75, 0.02024, 0.25, 0.5], dtype=float)
        originales = valores.copy()
        esperado = np.asarray(
            [beta.cdf(x, 0.5, 0.5) for x in valores],
            dtype=float,
        )

        observado = uniformizar_beta(valores, 0.5, 0.5)

        self.assertIsInstance(observado, np.ndarray)
        self.assertEqual(observado.dtype, np.dtype(float))
        np.testing.assert_array_equal(observado, esperado)
        np.testing.assert_array_equal(valores, originales)


class CodificacionBinariaTest(unittest.TestCase):
    def test_factor_y_palabra_historicos(self) -> None:
        factor = factor_normalizacion_binaria(4)
        self.assertEqual(factor, 1 / int("1111", 2))

        bits = np.asarray([0, 1, 0, 1], dtype=np.uint8)
        originales = bits.copy()
        observado = codificar_palabra_binaria(bits, factor)

        self.assertEqual(observado, int("0101", 2) / int("1111", 2))
        np.testing.assert_array_equal(bits, originales)

    def test_palabra_de_unos_produce_uno(self) -> None:
        bits = [1, 1, 1, 1]
        factor = factor_normalizacion_binaria(4)
        self.assertEqual(codificar_palabra_binaria(bits, factor), 1.0)


class CodificacionDecimalTest(unittest.TestCase):
    def test_casos_mcf036(self) -> None:
        casos = {
            0.02024: "020240000000",
            0.5: "500000000000",
            0.05: "050000000000",
            0.0: "000000000000",
            1e-8: "000000010000",
        }
        for valor, esperado in casos.items():
            with self.subTest(valor=valor):
                self.assertEqual(extraer_digitos(valor, 12), esperado)

    def test_rechaza_valores_fuera_del_dominio(self) -> None:
        for valor in (math.nan, math.inf, -math.inf, -0.1, 1.0, 1.2):
            with self.subTest(valor=valor):
                with self.assertRaises(ValueError):
                    extraer_digitos(valor)

    def test_rechaza_bool_como_precision(self) -> None:
        with self.assertRaises(TypeError):
            extraer_digitos(0.5, precision=True)

    def test_api_historica_reexporta_la_funcion_canonica(self) -> None:
        self.assertIs(extraer_digitos_antiguo, extraer_digitos)
        self.assertEqual(PRECISION_ANTIGUA, PRECISION_DECIMAL)
        self.assertEqual(PRECISION_DECIMAL, 12)
        for valor in (0.02024, 0.5, 0.05, 0.0, 1e-8):
            with self.subTest(valor=valor):
                self.assertEqual(
                    extraer_digitos_antiguo(valor), extraer_digitos(valor)
                )


if __name__ == "__main__":
    unittest.main()
