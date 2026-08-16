"""Pruebas del benchmark Park--Miller MINSTD."""

import hashlib
import inspect
import unittest

import numpy as np

import tesis_generacion.generadores.congruencial as modulo_congruencial
from tesis_generacion.generadores import (
    MODULO_MINSTD,
    estados_minstd,
    muestra_minstd,
    paso_congruencial,
)


class GeneradorMinstdTest(unittest.TestCase):
    def test_primeros_estados_semilla_2024(self) -> None:
        esperado = [
            34017368,
            499253874,
            741251489,
            661139376,
            689102854,
            372358907,
            468802591,
            47646094,
            1923985174,
            1757546539,
        ]
        np.testing.assert_array_equal(estados_minstd(10, 2024), esperado)

    def test_reproducibilidad_rango_y_n(self) -> None:
        primera = muestra_minstd(1000, 2024)
        segunda = muestra_minstd(1000, 2024)
        np.testing.assert_array_equal(primera, segunda)
        self.assertEqual(primera.shape, (1000,))
        self.assertTrue(np.all((0.0 < primera) & (primera < 1.0)))

    def test_fingerprint_exacto(self) -> None:
        muestra = np.asarray(muestra_minstd(1000, 2024), dtype="<f8")
        self.assertEqual(
            hashlib.sha256(muestra.tobytes(order="C")).hexdigest(),
            "2ad4f3c5dee1991799ce98f134efa9a6ac7e8ab1ed57208ab8110c5e46f29131",
        )

    def test_semillas_invalidas(self) -> None:
        for semilla in (0, MODULO_MINSTD, -1, True, 1.5):
            with self.subTest(semilla=semilla):
                with self.assertRaises((TypeError, ValueError)):
                    muestra_minstd(2, semilla)

    def test_parametros_genericos_invalidos(self) -> None:
        casos = (
            (1, 1, 0, 1),
            (-1, 1, 0, 7),
            (1, -1, 0, 7),
            (1, 1, -1, 7),
            (1, 7, 0, 7),
        )
        for caso in casos:
            with self.subTest(caso=caso):
                with self.assertRaises(ValueError):
                    paso_congruencial(*caso)

    def test_no_depende_de_rng_externo(self) -> None:
        fuente = inspect.getsource(modulo_congruencial)
        self.assertNotIn("np.random", fuente)
        self.assertNotIn("random.", fuente)


if __name__ == "__main__":
    unittest.main()
