from pathlib import Path
import tempfile
import unittest

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from tesis_generacion.visualizacion.bifurcaciones import (
    ConfiguracionBifurcacion,
    LOGISTICO,
    TIENDA,
    construir_figura,
    datos_bifurcacion,
    regenerar_bifurcaciones,
)


class VisualizacionBifurcacionesTest(unittest.TestCase):
    def test_datos_bifurcacion_respetan_malla_y_rango(self) -> None:
        configuracion = ConfiguracionBifurcacion(
            numero_parametros=41,
            burn_in=20,
            iteraciones_graficadas=7,
            dpi=96,
        )
        for especificacion in (LOGISTICO, TIENDA):
            parametros, estados = datos_bifurcacion(especificacion, configuracion)
            self.assertEqual(parametros.shape, (41 * 7,))
            self.assertEqual(estados.shape, (41 * 7,))
            self.assertTrue(np.isclose(parametros.min(), especificacion.parametro_minimo))
            self.assertTrue(np.isclose(parametros.max(), especificacion.parametro_maximo))
            self.assertTrue(np.all((0.0 <= estados) & (estados <= 1.0)))

    def test_tienda_oculta_rotulos_verticales(self) -> None:
        configuracion = ConfiguracionBifurcacion(
            numero_parametros=20,
            burn_in=5,
            iteraciones_graficadas=3,
            dpi=96,
        )
        figura = construir_figura(TIENDA, configuracion, usar_latex=False)
        eje = figura.axes[0]
        self.assertEqual(eje.get_ylabel(), "")
        self.assertFalse(any(etiqueta.get_visible() for etiqueta in eje.get_yticklabels()))
        plt.close(figura)

    def test_regeneracion_hibrida_documenta_parametros(self) -> None:
        configuracion = ConfiguracionBifurcacion(
            numero_parametros=64,
            burn_in=20,
            iteraciones_graficadas=8,
            figura_ancho_pulgadas=3.0,
            figura_alto_pulgadas=2.1,
            dpi=96,
        )
        with tempfile.TemporaryDirectory() as temporal:
            salida = Path(temporal)
            reporte = regenerar_bifurcaciones(
                salida, configuracion, incluir_svg=True, usar_latex=False
            )
            self.assertEqual(reporte["configuracion"]["numero_parametros"], 64)
            self.assertEqual(reporte["mapas"]["logistico"]["puntos_graficados"], 512)
            self.assertEqual(
                set(reporte["archivos"]),
                {
                    "logistico_bifurcacion.pdf",
                    "logistico_bifurcacion.svg",
                    "logistico_bifurcacion.png",
                    "tienda_bifurcacion.pdf",
                    "tienda_bifurcacion.svg",
                    "tienda_bifurcacion.png",
                },
            )
            self.assertTrue(
                all(datos["bytes"] > 0 for datos in reporte["archivos"].values())
            )
            self.assertIn(
                "<image",
                (salida / "logistico_bifurcacion.svg").read_text(encoding="utf-8"),
            )
            with Image.open(salida / "logistico_bifurcacion.png") as imagen:
                self.assertEqual(imagen.size, (288, 201))

            segunda = salida / "segunda"
            regenerar_bifurcaciones(
                segunda, configuracion, incluir_svg=True, usar_latex=False
            )
            for nombre in reporte["archivos"]:
                self.assertEqual(
                    (salida / nombre).read_bytes(), (segunda / nombre).read_bytes()
                )


if __name__ == "__main__":
    unittest.main()
