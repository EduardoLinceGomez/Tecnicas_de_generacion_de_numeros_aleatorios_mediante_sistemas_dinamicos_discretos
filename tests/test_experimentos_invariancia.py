"""Pruebas de los ensembles reproducibles de invariancia."""

import hashlib
import json
import unittest
from pathlib import Path

import numpy as np

from tesis_generacion.experimentos.invariancia import (
    ITERACIONES_INVARIANCIA,
    NUM_PARTICULAS_INVARIANCIA,
    SEED_INVARIANCIA,
    aplicar_logistico,
    aplicar_tienda,
    construir_experimentos_invariancia,
    evolucion_ensemble,
    muestra_inicial_logistica,
    muestra_inicial_tienda,
)


DATA_DIR = Path(__file__).resolve().parent / "data"


def _baseline() -> dict:
    return json.loads(
        (DATA_DIR / "invariancia_baseline.json").read_text(encoding="utf-8")
    )


def _sha256(valores: np.ndarray) -> str:
    muestra = np.ascontiguousarray(valores, dtype=np.dtype("<f8"))
    return hashlib.sha256(muestra.tobytes(order="C")).hexdigest()


class ExperimentosInvarianciaTest(unittest.TestCase):
    def test_parametros_documentados(self) -> None:
        self.assertEqual(SEED_INVARIANCIA, 2024)
        self.assertEqual(NUM_PARTICULAS_INVARIANCIA, 1000)
        self.assertEqual(ITERACIONES_INVARIANCIA, (0, 1, 2, 3, 4))

    def test_aplicaciones_controladas(self) -> None:
        valores = np.asarray([0.0, 0.25, 0.5, 0.75, 1.0])
        np.testing.assert_allclose(
            aplicar_logistico(valores, 4.0),
            [0.0, 0.75, 1.0, 0.75, 0.0],
            rtol=0.0,
            atol=0.0,
        )
        np.testing.assert_allclose(
            aplicar_tienda(valores, 2.0),
            [0.0, 0.5, 1.0, 0.5, 0.0],
            rtol=0.0,
            atol=0.0,
        )

    def test_ensemble_fijo_y_conservacion_de_particulas(self) -> None:
        inicial = np.asarray([0.1, 0.2, 0.3])
        evolucion = evolucion_ensemble(inicial, "logistico", 3, 4.0)
        self.assertEqual(len(evolucion), 4)
        self.assertTrue(np.array_equal(evolucion[0], inicial))
        for valores in evolucion:
            self.assertEqual(len(valores), len(inicial))
            self.assertTrue(np.all((0.0 <= valores) & (valores <= 1.0)))

    def test_iniciales_reproducibles_y_parametros_correctos(self) -> None:
        logistica = muestra_inicial_logistica()
        tienda = muestra_inicial_tienda()
        np.testing.assert_array_equal(logistica, muestra_inicial_logistica())
        np.testing.assert_array_equal(tienda, muestra_inicial_tienda())
        self.assertEqual(len(logistica), 1000)
        self.assertEqual(len(tienda), 1000)
        self.assertTrue(np.all((0.0 <= logistica) & (logistica <= 1.0)))
        self.assertTrue(np.all((0.0 <= tienda) & (tienda <= 1.0)))

    def test_baseline_de_fingerprints_iniciales_y_finales(self) -> None:
        baseline = _baseline()["experimentos"]
        experimentos = construir_experimentos_invariancia()
        for nombre, evolucion in experimentos.items():
            with self.subTest(nombre=nombre):
                self.assertEqual(
                    _sha256(evolucion[0]),
                    baseline[nombre]["fingerprint_inicial"]["sha256"],
                )
                self.assertEqual(
                    _sha256(evolucion[-1]),
                    baseline[nombre]["fingerprint_final"]["sha256"],
                )

    def test_validaciones(self) -> None:
        with self.assertRaisesRegex(ValueError, "positivo"):
            muestra_inicial_logistica(n=0)
        with self.assertRaisesRegex(ValueError, "unidimensional"):
            aplicar_logistico([[0.1, 0.2]])
        with self.assertRaisesRegex(ValueError, r"\[0,1\]"):
            aplicar_tienda([-0.1, 0.2])
        with self.assertRaisesRegex(ValueError, r"\(0,2\]"):
            aplicar_tienda([0.1], 2.1)
        with self.assertRaisesRegex(ValueError, "logistico"):
            evolucion_ensemble([0.1], "desconocido")


if __name__ == "__main__":
    unittest.main()
