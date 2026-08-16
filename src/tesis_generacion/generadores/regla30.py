"""Dinámica determinista del autómata celular regla 30."""

import numbers

import numpy as np


def paso_regla30(fila: np.ndarray) -> np.ndarray:
    """Calcula un paso de regla 30 con vecindad (izq., centro, der.)."""

    fila = np.asarray(fila)
    if fila.ndim != 1 or fila.size == 0:
        raise ValueError("fila debe ser un arreglo unidimensional no vacío")
    if not np.all((fila == 0) | (fila == 1)):
        raise ValueError("fila debe contener únicamente ceros y unos")
    fila = fila.astype(np.uint8, copy=False)

    izquierda = np.roll(fila, 1)
    derecha = np.roll(fila, -1)
    return np.bitwise_xor(izquierda, np.bitwise_or(fila, derecha))


def evolucion_regla30(
    condicion_inicial: np.ndarray, numero_instantes: int
) -> np.ndarray:
    """Construye A[t,j] con frontera periódica e incluye A[0,:]."""

    if isinstance(numero_instantes, bool) or not isinstance(
        numero_instantes, numbers.Integral
    ):
        raise TypeError("numero_instantes debe ser un entero")
    numero_instantes = int(numero_instantes)
    if numero_instantes < 1:
        raise ValueError("numero_instantes debe ser mayor o igual que 1")
    inicial = np.asarray(condicion_inicial)
    if inicial.ndim != 1 or inicial.size == 0:
        raise ValueError(
            "condicion_inicial debe ser un arreglo unidimensional no vacío"
        )
    if not np.all((inicial == 0) | (inicial == 1)):
        raise ValueError("condicion_inicial debe contener únicamente ceros y unos")
    inicial = inicial.astype(np.uint8, copy=False)

    matriz = np.empty((numero_instantes, inicial.size), dtype=np.uint8)
    matriz[0] = inicial
    for instante in range(1, numero_instantes):
        matriz[instante] = paso_regla30(matriz[instante - 1])
    return matriz
