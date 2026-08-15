"""Permutaciones explícitas para modificar el orden de una muestra."""

import numbers
from typing import Sequence

import numpy as np


def generar_permutacion_por_ranking(
    secuencia_auxiliar: Sequence[float],
) -> np.ndarray:
    """Devuelve los índices que ordenan de forma estable una secuencia auxiliar."""

    auxiliar = np.asarray(secuencia_auxiliar, dtype=float)
    if auxiliar.ndim != 1:
        raise ValueError("la secuencia auxiliar debe ser unidimensional")
    if auxiliar.size == 0:
        raise ValueError("la secuencia auxiliar no puede estar vacía")
    if not np.all(np.isfinite(auxiliar)):
        raise ValueError("la secuencia auxiliar contiene NaN o infinito")
    return np.argsort(auxiliar, kind="stable").astype(np.int64, copy=False)


def validar_permutacion(indices: Sequence[int], longitud: int) -> np.ndarray:
    """Valida que los índices contengan una vez cada entero entre 0 y n-1."""

    if isinstance(longitud, bool) or not isinstance(longitud, numbers.Integral):
        raise TypeError("longitud debe ser un entero")
    longitud = int(longitud)
    if longitud < 1:
        raise ValueError("longitud debe ser positiva")

    arreglo = np.asarray(indices)
    if arreglo.ndim != 1:
        raise ValueError("los índices deben ser unidimensionales")
    if arreglo.size != longitud:
        raise ValueError("la longitud de los índices no coincide con la muestra")
    if arreglo.dtype.kind not in "iu":
        raise TypeError("los índices deben ser enteros")
    normalizados = arreglo.astype(np.int64, copy=False)
    if np.any((normalizados < 0) | (normalizados >= longitud)):
        raise ValueError("los índices están fuera de rango")
    if np.unique(normalizados).size != longitud:
        raise ValueError("los índices contienen repeticiones")
    return normalizados


def aplicar_permutacion(
    muestra: Sequence[float], indices: Sequence[int]
) -> np.ndarray:
    """Devuelve una copia reordenada sin modificar la muestra de entrada."""

    valores = np.asarray(muestra)
    if valores.ndim != 1:
        raise ValueError("la muestra debe ser unidimensional")
    if valores.size == 0:
        raise ValueError("la muestra no puede estar vacía")
    permutacion = validar_permutacion(indices, valores.size)
    return np.array(valores[permutacion], copy=True)
