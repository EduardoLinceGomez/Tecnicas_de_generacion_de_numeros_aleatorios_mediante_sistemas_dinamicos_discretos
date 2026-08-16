"""Codificación histórica de palabras binarias como valores normalizados."""

import numbers

import numpy as np


def factor_normalizacion_binaria(longitud: int) -> float:
    """Devuelve 1/(2**longitud-1), el factor histórico de R30."""

    if isinstance(longitud, bool) or not isinstance(longitud, numbers.Integral):
        raise TypeError("longitud debe ser un entero")
    longitud = int(longitud)
    if longitud < 1:
        raise ValueError("longitud debe ser mayor o igual que 1")

    return 1 / int("1" * longitud, 2)


def codificar_palabra_binaria(bits, factor_normalizacion: float) -> float:
    """Interpreta el primer bit como el más significativo y normaliza."""

    valores = bits.tolist() if hasattr(bits, "tolist") else bits
    valores = list(valores)
    if not valores:
        raise ValueError("bits no puede estar vacío")
    if any(valor not in (0, 1) for valor in valores):
        raise ValueError("bits debe contener únicamente ceros y unos")
    factor_normalizacion = float(factor_normalizacion)
    if not np.isfinite(factor_normalizacion) or factor_normalizacion <= 0.0:
        raise ValueError("factor_normalizacion debe ser finito y positivo")
    return int("".join(map(str, valores)), 2) * factor_normalizacion


def _validar_matriz_binaria(matriz) -> np.ndarray:
    arreglo = np.asarray(matriz)
    if arreglo.ndim != 2 or 0 in arreglo.shape:
        raise ValueError("matriz debe ser un arreglo bidimensional no vacío")
    if not np.all((arreglo == 0) | (arreglo == 1)):
        raise ValueError("matriz debe contener únicamente ceros y unos")
    return arreglo.astype(np.uint8, copy=False)


def codificar_matriz_por_columnas(matriz) -> np.ndarray:
    """Codifica cada historia temporal A[:,j] con denominador 2**T-1."""

    arreglo = _validar_matriz_binaria(matriz)
    factor = factor_normalizacion_binaria(arreglo.shape[0])
    return np.asarray(
        [
            codificar_palabra_binaria(arreglo[:, posicion], factor)
            for posicion in range(arreglo.shape[1])
        ],
        dtype=float,
    )


def codificar_matriz_por_filas(matriz) -> np.ndarray:
    """Codifica cada configuración A[t,:] con denominador 2**J-1."""

    arreglo = _validar_matriz_binaria(matriz)
    factor = factor_normalizacion_binaria(arreglo.shape[1])
    return np.asarray(
        [
            codificar_palabra_binaria(arreglo[instante], factor)
            for instante in range(arreglo.shape[0])
        ],
        dtype=float,
    )
