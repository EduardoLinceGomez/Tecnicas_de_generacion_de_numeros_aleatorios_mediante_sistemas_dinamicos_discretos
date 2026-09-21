"""Parámetros concretos de los experimentos reproducibles."""

import math
from typing import Mapping, Sequence

SEED = 2024
NUM_VALORES = 1000
NUM_ITERACIONES = 1000
NUM_CELDAS = 1000
FACTOR_TIENDA = 1.999

INTERVALOS_BRECHAS_COMUNES = {
    "i1": (0.1, 0.3),
    "i2": (0.4, 0.6),
    "i3": (0.7, 0.9),
}


def validar_intervalos_brechas_comunes(
    intervalos: Mapping[str, Sequence[float]],
) -> float:
    """Valida el protocolo común y devuelve su longitud/probabilidad."""

    if tuple(intervalos) != ("i1", "i2", "i3"):
        raise ValueError("deben existir exactamente los intervalos i1, i2 e i3")
    longitudes = []
    for identificador, intervalo in intervalos.items():
        if len(intervalo) != 2:
            raise ValueError(f"{identificador} debe tener dos extremos")
        alpha, beta = (float(extremo) for extremo in intervalo)
        if not (math.isfinite(alpha) and math.isfinite(beta)):
            raise ValueError(f"los extremos de {identificador} deben ser finitos")
        if not 0.0 <= alpha < beta <= 1.0:
            raise ValueError(
                f"{identificador} debe satisfacer 0 <= alpha < beta <= 1"
            )
        longitudes.append(beta - alpha)
    longitud = longitudes[0]
    if not all(
        math.isclose(valor, longitud, rel_tol=0.0, abs_tol=1e-12)
        for valor in longitudes[1:]
    ):
        raise ValueError("todos los intervalos deben tener la misma longitud")
    if not math.isclose(longitud, 0.2, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError("la longitud común y la probabilidad deben ser 0.2")
    return 0.2


LONGITUD_INTERVALO_BRECHAS = validar_intervalos_brechas_comunes(
    INTERVALOS_BRECHAS_COMUNES
)
PROBABILIDAD_BRECHAS = LONGITUD_INTERVALO_BRECHAS
