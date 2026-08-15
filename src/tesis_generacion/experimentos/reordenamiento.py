"""Reconstrucción reproducible del reordenamiento serial histórico."""

import hashlib
from typing import Dict

import numpy as np

from tesis_generacion.estadistica.dependencia_serial import (
    resumen_autocorrelaciones,
    resumen_brechas,
)
from tesis_generacion.estadistica.invariancia import fingerprint_ensemble
from tesis_generacion.estadistica.momentos import momentos_ordinarios
from tesis_generacion.generadores.logistico import orbita_logistica
from tesis_generacion.transformaciones.reordenamiento import (
    aplicar_permutacion,
    generar_permutacion_por_ranking,
)

from .muestras import construir_muestras
from .parametros import NUM_VALORES


SEED_REORDENAMIENTO = 2024
LAGS_REORDENAMIENTO = tuple(range(1, 21))
INTERVALOS_BRECHAS = {
    "logistico": (0.2, 0.5),
    "tienda": (0.7, 0.9),
    "r30_columnas": (0.1, 0.3),
    "r30_filas": (0.7, 1.0),
}


def fingerprint_permutacion(indices: np.ndarray) -> Dict[str, object]:
    """Devuelve SHA-256 de índices int64 little-endian en orden C."""

    arreglo = np.ascontiguousarray(indices, dtype="<i8")
    return {
        "n_elementos": int(arreglo.size),
        "n_bytes": int(arreglo.nbytes),
        "dtype": arreglo.dtype.str,
        "endianness": "little",
        "sha256": hashlib.sha256(arreglo.tobytes(order="C")).hexdigest(),
    }


def construir_permutaciones_reordenamiento() -> Dict[str, Dict[str, object]]:
    """Construye las dos permutaciones por ranking presentes en el notebook."""

    auxiliar_fija = np.asarray(
        orbita_logistica(4.0, 0.02024, NUM_VALORES)[:NUM_VALORES],
        dtype=float,
    )
    rng = np.random.RandomState(SEED_REORDENAMIENTO)
    inicial_sembrado = float(rng.uniform(0.0, 1.0))
    auxiliar_sembrada = np.asarray(
        orbita_logistica(4.0, inicial_sembrado, NUM_VALORES)[:NUM_VALORES],
        dtype=float,
    )
    if np.unique(auxiliar_fija).size != NUM_VALORES:
        raise ValueError("la órbita auxiliar fija contiene empates")
    if np.unique(auxiliar_sembrada).size != NUM_VALORES:
        raise ValueError("la órbita auxiliar sembrada contiene empates")

    return {
        "fija": {
            "metodo": "ranking de órbita logística auxiliar fija",
            "r": 4.0,
            "x0": 0.02024,
            "seed": None,
            "auxiliar": auxiliar_fija,
            "indices": generar_permutacion_por_ranking(auxiliar_fija),
        },
        "sembrada": {
            "metodo": "ranking de órbita logística auxiliar con estado sembrado",
            "r": 4.0,
            "x0": inicial_sembrado,
            "seed": SEED_REORDENAMIENTO,
            "auxiliar": auxiliar_sembrada,
            "indices": generar_permutacion_por_ranking(auxiliar_sembrada),
        },
    }


def _verificar_conservacion(
    original: np.ndarray, reordenada: np.ndarray
) -> Dict[str, object]:
    bordes = np.linspace(0.0, 1.0, 41)
    momentos_originales = np.asarray(momentos_ordinarios(original, 4))
    momentos_reordenados = np.asarray(momentos_ordinarios(reordenada, 4))
    hist_original, _ = np.histogram(original, bins=bordes)
    hist_reordenado, _ = np.histogram(reordenada, bins=bordes)
    return {
        "n_identico": bool(original.size == reordenada.size),
        "multiconjunto_identico": bool(
            np.array_equal(np.sort(original), np.sort(reordenada))
        ),
        "minimo_identico": bool(np.min(original) == np.min(reordenada)),
        "maximo_identico": bool(np.max(original) == np.max(reordenada)),
        "diferencia_suma": float(np.sum(reordenada) - np.sum(original)),
        "maxima_diferencia_momentos_m1_m4": float(
            np.max(np.abs(momentos_reordenados - momentos_originales))
        ),
        "histograma_40_bins_identico": bool(
            np.array_equal(hist_original, hist_reordenado)
        ),
        "cdf_empirica_identica": bool(
            np.array_equal(np.sort(original), np.sort(reordenada))
        ),
    }


def construir_experimentos_reordenamiento() -> Dict[str, object]:
    """Construye muestras derivadas y diagnósticos antes/después."""

    muestras = construir_muestras()
    permutaciones = construir_permutaciones_reordenamiento()
    resultados = {}
    for nombre, original in muestras.items():
        clave = "sembrada" if nombre == "logistico" else "fija"
        especificacion = permutaciones[clave]
        indices = especificacion["indices"]
        reordenada = aplicar_permutacion(original, indices)
        alpha, beta = INTERVALOS_BRECHAS[nombre]
        resultados[nombre] = {
            "original": original,
            "reordenada": reordenada,
            "indices": indices,
            "permutacion": clave,
            "metodo": especificacion["metodo"],
            "intervalo_brechas": (alpha, beta),
            "fingerprint_original": fingerprint_ensemble(original),
            "fingerprint_reordenada": fingerprint_ensemble(reordenada),
            "fingerprint_permutacion": fingerprint_permutacion(indices),
            "acf_original": resumen_autocorrelaciones(
                original, LAGS_REORDENAMIENTO
            ),
            "acf_reordenada": resumen_autocorrelaciones(
                reordenada, LAGS_REORDENAMIENTO
            ),
            "brechas_original": resumen_brechas(original, alpha, beta),
            "brechas_reordenada": resumen_brechas(reordenada, alpha, beta),
            "conservacion_marginal": _verificar_conservacion(
                original, reordenada
            ),
        }

    resumen_permutaciones = {}
    for clave, especificacion in permutaciones.items():
        resumen_permutaciones[clave] = {
            "metodo": especificacion["metodo"],
            "r": especificacion["r"],
            "x0": especificacion["x0"],
            "seed": especificacion["seed"],
            "fingerprint_auxiliar": fingerprint_ensemble(
                especificacion["auxiliar"]
            ),
            "fingerprint_permutacion": fingerprint_permutacion(
                especificacion["indices"]
            ),
            "sin_empates": bool(
                np.unique(especificacion["auxiliar"]).size == NUM_VALORES
            ),
        }
    return {
        "parametros": {
            "n": NUM_VALORES,
            "seed_reordenamiento": SEED_REORDENAMIENTO,
            "lags": list(LAGS_REORDENAMIENTO),
            "intervalos_brechas": {
                nombre: list(intervalo)
                for nombre, intervalo in INTERVALOS_BRECHAS.items()
            },
        },
        "permutaciones": permutaciones,
        "resumen_permutaciones": resumen_permutaciones,
        "muestras": resultados,
    }
