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

    def test_baseline_cientifico_exacto(self) -> None:
        observado = construir_comparacion_generadores()
        self.assertEqual(observado["benchmark"], self.baseline["benchmark"])
        self.assertEqual(observado["parametros"], self.baseline["parametros"])
        self.assertEqual(observado["muestras"], self.baseline["muestras"])


if __name__ == "__main__":
    unittest.main()
