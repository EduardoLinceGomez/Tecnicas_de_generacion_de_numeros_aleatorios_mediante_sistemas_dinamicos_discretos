"""Construcción reproducible de las cuatro muestras del baseline."""

from typing import Dict, Tuple

import numpy as np

from tesis_generacion.generadores.logistico import orbita_logistica
from tesis_generacion.generadores.regla30 import evolucion_regla30
from tesis_generacion.generadores.tienda import paso_tienda
from tesis_generacion.transformaciones.codificacion_binaria import (
    codificar_matriz_por_columnas,
    codificar_matriz_por_filas,
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
    matriz = evolucion_regla30(
        rng.binomial(size=NUM_CELDAS, n=1, p=0.5),
        NUM_ITERACIONES,
    )
    columnas = codificar_matriz_por_columnas(matriz)
    filas = codificar_matriz_por_filas(matriz)
    return columnas, filas


def construir_muestras() -> Dict[str, np.ndarray]:
    columnas, filas = muestras_regla_30()
    return {
        "logistico": muestra_logistica(),
        "tienda": muestra_tienda(),
        "r30_columnas": columnas,
        "r30_filas": filas,
    }
