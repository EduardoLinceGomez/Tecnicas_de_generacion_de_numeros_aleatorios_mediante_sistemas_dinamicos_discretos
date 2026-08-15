"""Pruebas unitarias de los generadores dinámicos puros."""

import unittest

import numpy as np

from tesis_generacion.generadores import (
    orbita_logistica,
    paso_logistico,
    paso_regla30,
    paso_tienda,
)


class GeneradorLogisticoTest(unittest.TestCase):
    def test_paso_logistico(self) -> None:
        self.assertEqual(paso_logistico(4, 0.25), 0.75)

    def test_orbita_incluye_estado_inicial(self) -> None:
        orbita = orbita_logistica(4, 0.25, 2)
        self.assertEqual(orbita, [0.25, 0.75, 0.75])
        self.assertEqual(len(orbita), 3)


class GeneradorTiendaTest(unittest.TestCase):
    def test_ramas_historicas(self) -> None:
        self.assertEqual(paso_tienda(0.25, 1.999), 1.999 * 0.25)
        self.assertEqual(paso_tienda(0.75, 1.999), 1.999 * (1.0 - 0.75))
        self.assertEqual(paso_tienda(0.5, 1.999), 1.999 * (1.0 - 0.5))

    def test_fuera_del_dominio(self) -> None:
        for x in (-0.1, 1.0):
            with self.subTest(x=x):
                with self.assertRaises(ValueError):
                    paso_tienda(x, 1.999)


class GeneradorRegla30Test(unittest.TestCase):
    def test_paso_periodico_no_modifica_entrada(self) -> None:
        fila = np.asarray([0, 0, 1, 0, 0], dtype=np.uint8)
        original = fila.copy()

        resultado = paso_regla30(fila)

        np.testing.assert_array_equal(resultado, [0, 1, 1, 1, 0])
        np.testing.assert_array_equal(fila, original)
        self.assertEqual(resultado.shape, fila.shape)
        self.assertTrue(np.all((resultado == 0) | (resultado == 1)))


if __name__ == "__main__":
    unittest.main()
