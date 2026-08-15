"""Experimento reproducible que construye las muestras de la tesis."""

from .muestras import (
    construir_muestras,
    muestra_logistica,
    muestra_tienda,
    muestras_regla_30,
)
from .parametros import (
    FACTOR_TIENDA,
    NUM_CELDAS,
    NUM_ITERACIONES,
    NUM_VALORES,
    SEED,
)

__all__ = (
    "FACTOR_TIENDA",
    "NUM_CELDAS",
    "NUM_ITERACIONES",
    "NUM_VALORES",
    "SEED",
    "construir_muestras",
    "muestra_logistica",
    "muestra_tienda",
    "muestras_regla_30",
)
