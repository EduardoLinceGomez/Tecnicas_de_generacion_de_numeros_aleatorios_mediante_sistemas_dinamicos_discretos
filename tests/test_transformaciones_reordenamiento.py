"""Pruebas de construcción y aplicación de permutaciones."""

import unittest

import numpy as np

from tesis_generacion.transformaciones.reordenamiento import (
    aplicar_permutacion,
    generar_permutacion_por_ranking,
    validar_permutacion,
)


class ReordenamientoTest(unittest.TestCase):
    def test_identidad_e_inversion(self) -> None:
        muestra = np.asarray([10.0, 20.0, 30.0])
        np.testing.assert_array_equal(
            aplicar_permutacion(muestra, [0, 1, 2]), muestra
        )
        np.testing.assert_array_equal(
            aplicar_permutacion(muestra, [2, 1, 0]), [30.0, 20.0, 10.0]
        )

    def test_no_muta_la_muestra(self) -> None:
        muestra = np.asarray([3.0, 1.0, 2.0])
        copia = muestra.copy()
        resultado = aplicar_permutacion(muestra, [1, 2, 0])
        np.testing.assert_array_equal(muestra, copia)
        self.assertFalse(np.shares_memory(muestra, resultado))

    def test_ranking_estable(self) -> None:
        np.testing.assert_array_equal(
            generar_permutacion_por_ranking([0.2, 0.1, 0.1, 0.4]),
            [1, 2, 0, 3],
        )

    def test_rechaza_repetidos_fuera_de_rango_y_longitud(self) -> None:
        for indices, patron in (
            ([0, 0, 2], "repeticiones"),
            ([0, 1, 3], "fuera de rango"),
            ([0, 1], "longitud"),
        ):
            with self.subTest(indices=indices):
                with self.assertRaisesRegex(ValueError, patron):
                    validar_permutacion(indices, 3)

    def test_rechaza_indices_no_enteros(self) -> None:
        with self.assertRaisesRegex(TypeError, "enteros"):
            validar_permutacion([0.0, 1.0], 2)

    def test_conserva_multiconjunto(self) -> None:
        muestra = np.asarray([0.3, 0.1, 0.4, 0.2])
        reordenada = aplicar_permutacion(muestra, [2, 0, 3, 1])
        np.testing.assert_array_equal(np.sort(muestra), np.sort(reordenada))


if __name__ == "__main__":
    unittest.main()
