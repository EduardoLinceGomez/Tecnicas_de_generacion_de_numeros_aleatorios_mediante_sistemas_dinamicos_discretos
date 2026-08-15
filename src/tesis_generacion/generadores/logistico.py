"""Dinámica determinista del mapeo logístico."""

from typing import List


def paso_logistico(r: float, x: float) -> float:
    """Calcula una aplicación del mapeo logístico."""

    return r * x * (1.0 - x)


def orbita_logistica(
    r: float, x_inicial: float, iteraciones: int
) -> List[float]:
    """Devuelve el estado inicial y las aplicaciones posteriores del mapa."""

    resultados = [x_inicial]
    x = x_inicial
    for _ in range(iteraciones):
        x = paso_logistico(r, x)
        resultados.append(x)
    return resultados
