"""Pruebas automáticas de la corrección metodológica MCF-036."""

import math
import unittest

from coleccionista import (
    TIPOS_DECIMALES,
    cdf_coleccionista,
    extraer_digitos,
    longitudes_coleccionista,
    pmf_coleccionista,
)
from regenerar_coleccionista import construir_muestras, validar_muestra


class ExtraccionDecimalTest(unittest.TestCase):
    def test_casos_requeridos_con_precision_12(self) -> None:
        esperados = {
            0.02024: "020240000000",
            0.5: "500000000000",
            0.05: "050000000000",
            0.0: "000000000000",
            1e-8: "000000010000",
        }
        for valor, esperado in esperados.items():
            with self.subTest(valor=valor):
                observado = extraer_digitos(valor)
                self.assertEqual(observado, esperado)
                self.assertEqual(len(observado), 12)
                self.assertLessEqual(set(observado), TIPOS_DECIMALES)
        self.assertNotEqual(extraer_digitos(0.5), extraer_digitos(0.05))

    def test_rechaza_valores_invalidos(self) -> None:
        for valor in (math.nan, math.inf, -math.inf, -0.1, 1.0, 1.2):
            with self.subTest(valor=valor):
                with self.assertRaises(ValueError):
                    extraer_digitos(valor)

    def test_longitudes_ordenadas_y_cola(self) -> None:
        longitudes, cola = longitudes_coleccionista(
            [0.0123456789, 0.0012345678, 0.9], precision=10
        )
        self.assertEqual(longitudes, [10, 11])
        self.assertEqual(cola, 9)


class DistribucionColeccionistaTest(unittest.TestCase):
    def test_valores_conocidos(self) -> None:
        self.assertEqual(cdf_coleccionista(9), 0.0)
        self.assertAlmostEqual(cdf_coleccionista(10), 0.00036288, places=14)

    def test_identidad_pmf(self) -> None:
        for m in (10, 11, 15, 20, 30, 50):
            self.assertAlmostEqual(
                pmf_coleccionista(m),
                cdf_coleccionista(m) - cdf_coleccionista(m - 1),
                places=15,
            )

    def test_cdf_acotada_y_monotona(self) -> None:
        valores = [cdf_coleccionista(m) for m in range(0, 201)]
        self.assertTrue(all(0.0 <= valor <= 1.0 for valor in valores))
        self.assertTrue(
            all(anterior <= siguiente for anterior, siguiente in zip(valores, valores[1:]))
        )

    def test_pmf_no_negativa_y_suma_truncada(self) -> None:
        masas = [pmf_coleccionista(m) for m in range(10, 301)]
        self.assertTrue(all(masa >= -1e-15 for masa in masas))
        self.assertAlmostEqual(sum(masas), cdf_coleccionista(300), places=14)
        self.assertGreater(sum(masas), 0.999999999999)


class MuestrasReproduciblesTest(unittest.TestCase):
    def test_cuatro_muestras_validas(self) -> None:
        muestras = construir_muestras()
        self.assertEqual(
            set(muestras),
            {"logistico", "tienda", "r30_columnas", "r30_filas"},
        )
        for nombre, valores in muestras.items():
            with self.subTest(nombre=nombre):
                validar_muestra(nombre, valores)


if __name__ == "__main__":
    unittest.main()
