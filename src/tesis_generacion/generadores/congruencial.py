"""Benchmark congruencial multiplicativo MINSTD de Park y Miller (1988)."""

import numbers

import numpy as np


MULTIPLICADOR_MINSTD = 16807
INCREMENTO_MINSTD = 0
MODULO_MINSTD = 2**31 - 1


def _validar_entero(nombre: str, valor: int) -> int:
    if isinstance(valor, bool) or not isinstance(valor, numbers.Integral):
        raise TypeError(f"{nombre} debe ser un entero")
    return int(valor)


def paso_congruencial(
    estado: int,
    multiplicador: int,
    incremento: int,
    modulo: int,
) -> int:
    """Evalúa (multiplicador*estado+incremento) mod modulo."""

    estado = _validar_entero("estado", estado)
    multiplicador = _validar_entero("multiplicador", multiplicador)
    incremento = _validar_entero("incremento", incremento)
    modulo = _validar_entero("modulo", modulo)
    if modulo <= 1:
        raise ValueError("modulo debe ser mayor que 1")
    if not 0 <= estado < modulo:
        raise ValueError("estado debe satisfacer 0 <= estado < modulo")
    if not 0 <= multiplicador < modulo:
        raise ValueError("multiplicador debe satisfacer 0 <= multiplicador < modulo")
    if not 0 <= incremento < modulo:
        raise ValueError("incremento debe satisfacer 0 <= incremento < modulo")
    return (multiplicador * estado + incremento) % modulo


def estados_minstd(numero_valores: int, semilla: int = 2024) -> np.ndarray:
    """Genera X_1,...,X_n; la semilla X_0 no se incluye."""

    numero_valores = _validar_entero("numero_valores", numero_valores)
    semilla = _validar_entero("semilla", semilla)
    if numero_valores < 1:
        raise ValueError("numero_valores debe ser mayor o igual que 1")
    if not 1 <= semilla < MODULO_MINSTD:
        raise ValueError("semilla debe satisfacer 1 <= semilla < MODULO_MINSTD")

    estados = np.empty(numero_valores, dtype=np.int64)
    estado = semilla
    for indice in range(numero_valores):
        estado = paso_congruencial(
            estado,
            MULTIPLICADOR_MINSTD,
            INCREMENTO_MINSTD,
            MODULO_MINSTD,
        )
        estados[indice] = estado
    return estados


def muestra_minstd(numero_valores: int, semilla: int = 2024) -> np.ndarray:
    """Devuelve U_i=X_i/m para los estados posteriores a la semilla."""

    return estados_minstd(numero_valores, semilla).astype(float) / MODULO_MINSTD
