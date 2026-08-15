"""Pruebas de histogramas y figuras reproducibles de momentos."""

import hashlib
import json
import os
import platform
import tempfile
import unittest
from pathlib import Path

import matplotlib
import numpy as np
import scipy

from tesis_generacion.visualizacion.momentos import (
    ARCHIVOS_REFERENCIA,
    ARCHIVOS_TESIS,
    N_HISTOGRAMAS,
    NUM_BINS_HISTOGRAMAS,
    SEED_HISTOGRAMAS,
    VENTANA_HISTOGRAMAS,
    bordes_histogramas,
    calcular_histograma,
    copiar_referencias,
    generar_muestras_histogramas,
    regenerar_momentos,
)


DATA_DIR = Path(__file__).resolve().parent / "data"
VARIABLE_PNG_ESTRICTO = "VERIFICAR_PNG_EXACTO"


def _baseline() -> dict:
    return json.loads(
        (DATA_DIR / "momentos_baseline.json").read_text(encoding="utf-8")
    )


def _fingerprint(valores: np.ndarray) -> str:
    muestra = np.ascontiguousarray(valores, dtype=np.dtype("<f8"))
    return hashlib.sha256(muestra.tobytes(order="C")).hexdigest()


class MuestrasHistogramasTest(unittest.TestCase):
    def test_rng_local_reproducible_y_orden_documentado(self) -> None:
        primera = generar_muestras_histogramas()
        segunda = generar_muestras_histogramas()
        self.assertEqual(SEED_HISTOGRAMAS, 2024)
        self.assertEqual(list(primera), ["normal", "cauchy"])
        for nombre in primera:
            with self.subTest(nombre=nombre):
                self.assertEqual(len(primera[nombre]), N_HISTOGRAMAS)
                np.testing.assert_array_equal(primera[nombre], segunda[nombre])

        rng = np.random.RandomState(2024)
        np.testing.assert_array_equal(
            primera["normal"], rng.normal(0.0, 1.0, 10_000)
        )
        np.testing.assert_array_equal(
            primera["cauchy"], rng.standard_cauchy(10_000)
        )

        baseline = _baseline()["histogramas"]
        for nombre in ("normal", "cauchy"):
            with self.subTest(baseline=nombre):
                self.assertEqual(
                    _fingerprint(primera[nombre]),
                    baseline[nombre]["fingerprint"]["sha256"],
                )

    def test_bordes_comunes(self) -> None:
        bordes = bordes_histogramas()
        self.assertEqual(len(bordes), 81)
        self.assertEqual(NUM_BINS_HISTOGRAMAS, 80)
        self.assertEqual(bordes[0], VENTANA_HISTOGRAMAS[0])
        self.assertEqual(bordes[-1], VENTANA_HISTOGRAMAS[1])
        np.testing.assert_array_equal(np.diff(bordes), np.full(80, 0.5))

    def test_normalizacion_con_n_total(self) -> None:
        valores = np.asarray([-21.0, -19.75, 0.25, 19.75, 21.0])
        bordes = bordes_histogramas()
        conteos, alturas, resumen = calcular_histograma(valores, bordes)
        self.assertEqual(int(conteos.sum()), 3)
        self.assertEqual(resumen["fuera_ventana"], 2)
        self.assertEqual(int(conteos.sum()) + resumen["fuera_ventana"], 5)
        np.testing.assert_array_equal(alturas, conteos / (5 * 0.5))
        self.assertAlmostEqual(
            float(np.sum(alturas * np.diff(bordes))), 3 / 5
        )
        self.assertAlmostEqual(resumen["masa_visible"], 3 / 5)


class RegeneracionMomentosTest(unittest.TestCase):
    def test_genera_figuras_csv_y_resumen(self) -> None:
        with tempfile.TemporaryDirectory(prefix="visual-momentos-") as temporal:
            directorio = Path(temporal)
            resumen = regenerar_momentos(directorio)
            esperados = set(ARCHIVOS_REFERENCIA) | set(ARCHIVOS_TESIS)
            self.assertEqual(
                {ruta.name for ruta in directorio.iterdir()}, esperados
            )
            self.assertEqual(
                set(resumen["figuras"]),
                esperados - {"resumen_momentos.csv"},
            )
            self.assertEqual(resumen["parametros"]["numero_bordes"], 81)
            self.assertEqual(resumen["parametros"]["ancho_bin"], 0.5)
            for nombre in ("normal", "cauchy"):
                observado = resumen["histogramas"][nombre]
                self.assertEqual(
                    observado["en_ventana"] + observado["fuera_ventana"],
                    N_HISTOGRAMAS,
                )

    def test_copia_referencias_solo_con_opcion_explicita(self) -> None:
        with tempfile.TemporaryDirectory(prefix="referencias-momentos-") as temporal:
            raiz = Path(temporal)
            salida = raiz / "output"
            referencias = raiz / "referencias"
            regenerar_momentos(salida)
            copiar_referencias(salida, referencias)
            self.assertEqual(
                {ruta.name for ruta in referencias.iterdir()},
                set(ARCHIVOS_REFERENCIA),
            )
            for nombre in ARCHIVOS_REFERENCIA:
                with self.subTest(nombre=nombre):
                    self.assertEqual(
                        (salida / nombre).read_bytes(),
                        (referencias / nombre).read_bytes(),
                    )


@unittest.skipUnless(
    os.environ.get(VARIABLE_PNG_ESTRICTO) == "1",
    f"active {VARIABLE_PNG_ESTRICTO}=1 para validar las referencias exactas",
)
class BaselineGraficoMomentosEstrictoTest(unittest.TestCase):
    def test_referencias_en_entorno_baseline(self) -> None:
        from PIL import __version__ as pillow_version

        baseline = _baseline()
        observado = {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "matplotlib": matplotlib.__version__,
            "pillow": pillow_version,
            "backend": str(matplotlib.get_backend()),
        }
        self.assertEqual(observado, baseline["entorno_referencia"])

        with tempfile.TemporaryDirectory(prefix="momentos-png-") as temporal:
            directorio = Path(temporal)
            regenerar_momentos(directorio)
            esperados = baseline["referencias_sha256"]
            for nombre, sha256 in esperados.items():
                with self.subTest(archivo=nombre):
                    observado_sha = hashlib.sha256(
                        (directorio / nombre).read_bytes()
                    ).hexdigest()
                    self.assertEqual(observado_sha, sha256)


if __name__ == "__main__":
    unittest.main()
