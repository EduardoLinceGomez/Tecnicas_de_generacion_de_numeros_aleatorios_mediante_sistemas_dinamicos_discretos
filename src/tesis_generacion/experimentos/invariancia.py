"""Experimentos reproducibles sobre evolución de distribuciones."""

from typing import Dict, List

import numpy as np


SEED_INVARIANCIA = 2024
NUM_PARTICULAS_INVARIANCIA = 1000
ITERACIONES_INVARIANCIA = tuple(range(5))


def _validar_ensemble(valores: np.ndarray) -> np.ndarray:
    ensemble = np.asarray(valores, dtype=float)
    if ensemble.ndim != 1:
        raise ValueError("el ensemble debe ser un arreglo unidimensional")
    if ensemble.size == 0:
        raise ValueError("el ensemble no puede estar vacío")
    if not np.all(np.isfinite(ensemble)):
        raise ValueError("el ensemble contiene NaN o infinito")
    if np.any((ensemble < 0.0) | (ensemble > 1.0)):
        raise ValueError("el ensemble debe estar contenido en [0,1]")
    return ensemble


def muestra_inicial_logistica(
    seed: int = SEED_INVARIANCIA,
    n: int = NUM_PARTICULAS_INVARIANCIA,
) -> np.ndarray:
    """Genera la triangular simétrica histórica sobre [0,1]."""

    if n <= 0:
        raise ValueError("n debe ser positivo")
    rng = np.random.RandomState(seed)
    return np.asarray(rng.triangular(0.0, 0.5, 1.0, n), dtype=float)


def muestra_inicial_tienda(
    seed: int = SEED_INVARIANCIA,
    n: int = NUM_PARTICULAS_INVARIANCIA,
) -> np.ndarray:
    """Genera la muestra Beta(2,2) histórica sobre [0,1]."""

    if n <= 0:
        raise ValueError("n debe ser positivo")
    rng = np.random.RandomState(seed)
    return np.asarray(rng.beta(2.0, 2.0, n), dtype=float)


def aplicar_logistico(valores: np.ndarray, r: float = 4.0) -> np.ndarray:
    """Aplica una vez el mapa logístico a todo el ensemble."""

    ensemble = _validar_ensemble(valores)
    if not np.isfinite(r) or not 0.0 <= r <= 4.0:
        raise ValueError("r debe pertenecer a [0,4]")
    resultado = r * ensemble * (1.0 - ensemble)
    return _validar_ensemble(resultado)


def aplicar_tienda(valores: np.ndarray, factor: float = 2.0) -> np.ndarray:
    """Aplica una vez el mapa tienda con un factor explícito."""

    ensemble = _validar_ensemble(valores)
    if not np.isfinite(factor) or not 0.0 < factor <= 2.0:
        raise ValueError("el factor debe pertenecer a (0,2]")
    resultado = np.where(
        ensemble <= 0.5,
        factor * ensemble,
        factor * (1.0 - ensemble),
    )
    return _validar_ensemble(resultado)


def evolucion_ensemble(
    valores_iniciales: np.ndarray,
    mapa: str,
    iteracion_maxima: int = 4,
    parametro: float = 4.0,
) -> List[np.ndarray]:
    """Conserva un ensemble y devuelve sus pushforwards de 0 a k."""

    if not isinstance(iteracion_maxima, int) or iteracion_maxima < 0:
        raise ValueError("iteracion_maxima debe ser un entero no negativo")
    actual = _validar_ensemble(valores_iniciales).copy()
    evolucion = [actual.copy()]
    for _ in range(iteracion_maxima):
        if mapa == "logistico":
            actual = aplicar_logistico(actual, parametro)
        elif mapa == "tienda":
            actual = aplicar_tienda(actual, parametro)
        else:
            raise ValueError("mapa debe ser 'logistico' o 'tienda'")
        evolucion.append(actual.copy())
    return evolucion


def construir_experimentos_invariancia() -> Dict[str, List[np.ndarray]]:
    """Construye los dos experimentos teóricos y el diagnóstico 1.999."""

    logistica = muestra_inicial_logistica()
    tienda = muestra_inicial_tienda()
    return {
        "logistico_r4": evolucion_ensemble(
            logistica, "logistico", ITERACIONES_INVARIANCIA[-1], 4.0
        ),
        "tienda_ideal_2": evolucion_ensemble(
            tienda, "tienda", ITERACIONES_INVARIANCIA[-1], 2.0
        ),
        "tienda_diagnostico_1_999": evolucion_ensemble(
            tienda, "tienda", ITERACIONES_INVARIANCIA[-1], 1.999
        ),
    }
