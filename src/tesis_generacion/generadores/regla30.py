"""Dinámica determinista del autómata celular regla 30."""

import numpy as np


def paso_regla30(fila: np.ndarray) -> np.ndarray:
    """Calcula un paso de regla 30 con frontera periódica."""

    izquierda = np.roll(fila, 1)
    derecha = np.roll(fila, -1)
    return np.bitwise_xor(izquierda, np.bitwise_or(fila, derecha))
