from pathlib import Path
import tempfile
import unittest

import numpy as np
from PIL import Image

from tesis_generacion.visualizacion.figuras_tesis import (
    ARCHIVOS_GENERADOS,
    CELDAS_R30_PEDAGOGICO,
    INSTANTES_R30_PEDAGOGICO,
    evolucion_regla_elemental,
    matriz_regla30_pedagogica,
    regenerar_figuras_tesis,
    tabla_regla30,
)


class VisualizacionFigurasTesisTest(unittest.TestCase):
    def test_tabla_regla30_derivada_de_la_implementacion(self) -> None:
        self.assertEqual(
            tabla_regla30(),
            (
                ((1, 1, 1), 0),
                ((1, 1, 0), 0),
                ((1, 0, 1), 0),
                ((1, 0, 0), 1),
                ((0, 1, 1), 1),
                ((0, 1, 0), 1),
                ((0, 0, 1), 1),
                ((0, 0, 0), 0),
            ),
        )

    def test_regla184_mueve_un_vehiculo_a_un_hueco(self) -> None:
        inicial = np.asarray([1, 0, 0, 0], dtype=np.uint8)
        matriz = evolucion_regla_elemental(184, inicial, 2)
        self.assertEqual(matriz[1].tolist(), [0, 1, 0, 0])

    def test_matriz_pedagogica_tiene_parametros_documentados(self) -> None:
        matriz = matriz_regla30_pedagogica()
        self.assertEqual(
            matriz.shape, (INSTANTES_R30_PEDAGOGICO, CELDAS_R30_PEDAGOGICO)
        )
        self.assertEqual(int(matriz[0].sum()), 1)
        self.assertEqual(matriz[0, CELDAS_R30_PEDAGOGICO // 2], 1)

    def test_regeneracion_produce_todas_las_figuras(self) -> None:
        with tempfile.TemporaryDirectory() as temporal:
            salida = Path(temporal)
            resumen = regenerar_figuras_tesis(salida)
            self.assertEqual(tuple(resumen["archivos"]), ARCHIVOS_GENERADOS)
            self.assertEqual(len(resumen["sha256"]), len(ARCHIVOS_GENERADOS))
            self.assertTrue(
                all((salida / nombre).is_file() for nombre in ARCHIVOS_GENERADOS)
            )

    def test_png_tienen_resolucion_suficiente(self) -> None:
        with tempfile.TemporaryDirectory() as temporal:
            salida = Path(temporal)
            regenerar_figuras_tesis(salida)
            for nombre in ARCHIVOS_GENERADOS:
                if nombre.endswith(".png"):
                    with Image.open(salida / nombre) as imagen:
                        self.assertGreaterEqual(imagen.width, 600)
                        self.assertGreaterEqual(imagen.height, 400)


if __name__ == "__main__":
    unittest.main()
