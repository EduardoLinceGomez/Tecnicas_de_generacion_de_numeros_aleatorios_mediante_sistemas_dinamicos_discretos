"""Construcción reproducible de las cuatro muestras del baseline."""

from typing import Dict, Tuple

import numpy as np

from tesis_generacion.generadores.logistico import orbita_logistica
from tesis_generacion.generadores.regla30 import paso_regla30
from tesis_generacion.generadores.tienda import paso_tienda
from tesis_generacion.transformaciones.codificacion_binaria import (
    codificar_palabra_binaria,
    factor_normalizacion_binaria,
)
from tesis_generacion.transformaciones.uniformizacion import uniformizar_beta

from .parametros import (
    FACTOR_TIENDA,
    NUM_CELDAS,
    NUM_ITERACIONES,
    NUM_VALORES,
    SEED,
)


def muestra_logistica() -> np.ndarray:
    trayectoria = np.asarray(
        orbita_logistica(4.0, 0.02024, NUM_ITERACIONES)
    )
    return uniformizar_beta(trayectoria[:NUM_VALORES], 0.5, 0.5)


def muestra_tienda() -> np.ndarray:
    rng = np.random.RandomState(SEED)
    x = float(rng.uniform(0.0, 1.0))
    resultados = []
    for _ in range(NUM_ITERACIONES):
        x = paso_tienda(x, FACTOR_TIENDA)
        resultados.append(x)
    return np.asarray(resultados, dtype=float)


def muestras_regla_30() -> Tuple[np.ndarray, np.ndarray]:
    rng = np.random.RandomState(SEED)
    matriz = np.empty((NUM_ITERACIONES, NUM_CELDAS), dtype=np.uint8)
    matriz[0] = rng.binomial(size=NUM_CELDAS, n=1, p=0.5)
    for indice in range(1, NUM_ITERACIONES):
        matriz[indice] = paso_regla30(matriz[indice - 1])

    precision_columnas = factor_normalizacion_binaria(NUM_ITERACIONES)
    precision_filas = factor_normalizacion_binaria(NUM_CELDAS)
    columnas = np.asarray(
        [
            codificar_palabra_binaria(matriz[:, j], precision_columnas)
            for j in range(NUM_CELDAS)
        ],
        dtype=float,
    )
    filas = np.asarray(
        [
            codificar_palabra_binaria(matriz[j], precision_filas)
            for j in range(NUM_ITERACIONES)
        ],
        dtype=float,
    )
    return columnas, filas


def construir_muestras() -> Dict[str, np.ndarray]:
    columnas, filas = muestras_regla_30()
    return {
        "logistico": muestra_logistica(),
        "tienda": muestra_tienda(),
        "r30_columnas": columnas,
        "r30_filas": filas,
    }
