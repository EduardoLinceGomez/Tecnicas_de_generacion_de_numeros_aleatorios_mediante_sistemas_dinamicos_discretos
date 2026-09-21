"""Pruebas del resumen comparativo homogéneo."""

import json
import unittest
from pathlib import Path

from tesis_generacion.experimentos import (
    construir_comparacion_generadores,
    construir_muestras_comparacion,
)


DATA_DIR = Path(__file__).resolve().parent / "data"


class ComparacionGeneradoresTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.baseline = json.loads(
            (DATA_DIR / "comparacion_generadores_baseline.json").read_text(
                encoding="utf-8"
            )
        )

    def test_cinco_muestras_originales_de_1000(self) -> None:
        muestras = construir_muestras_comparacion()
        self.assertEqual(
            list(muestras),
            [
                "logistico",
                "tienda",
                "r30_columnas",
                "r30_filas",
                "congruencial_minstd",
            ],
        )
        self.assertTrue(all(len(muestra) == 1000 for muestra in muestras.values()))

    def test_parametros_homogeneos(self) -> None:
        resumen = construir_comparacion_generadores()
        parametros = resumen["parametros"]
        self.assertEqual(parametros["n"], 1000)
        self.assertEqual(parametros["momentos"], list(range(1, 21)))
        self.assertEqual(parametros["malla_fgm"]["numero_puntos"], 40)
        self.assertEqual(
            parametros["malla_funcion_caracteristica"]["numero_puntos"], 60
        )
        self.assertEqual(parametros["lags_acf"], list(range(1, 21)))
        self.assertFalse(parametros["usa_muestras_reordenadas"])
        self.assertEqual(
            parametros["intervalos_brechas_comunes"],
            {"i1": [0.1, 0.3], "i2": [0.4, 0.6], "i3": [0.7, 0.9]},
        )
        self.assertEqual(parametros["longitud_intervalo_brechas"], 0.2)
        self.assertEqual(parametros["p_brechas"], 0.2)

    def test_quince_resumenes_de_brechas_sin_agregacion(self) -> None:
        resumen = construir_comparacion_generadores()
        self.assertEqual(
            sum(len(datos["brechas"]) for datos in resumen["muestras"].values()),
            15,
        )
        for datos in resumen["muestras"].values():
            self.assertEqual(tuple(datos["brechas"]), ("i1", "i2", "i3"))
            self.assertNotIn("ranking", datos)
            self.assertNotIn("score", datos)
            for brechas in datos["brechas"].values():
                self.assertEqual(brechas["p"], 0.2)

    def test_baseline_cientifico_exacto(self) -> None:
        observado = construir_comparacion_generadores()
        self.assertEqual(observado["benchmark"], self.baseline["benchmark"])
        self.assertEqual(observado["parametros"], self.baseline["parametros"])
        self.assertEqual(observado["muestras"], self.baseline["muestras"])


if __name__ == "__main__":
    unittest.main()
