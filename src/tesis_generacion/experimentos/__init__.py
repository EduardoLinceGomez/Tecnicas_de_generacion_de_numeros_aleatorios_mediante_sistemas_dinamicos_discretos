"""Experimento reproducible que construye las muestras de la tesis."""

from .comparacion_generadores import (
    LAGS_COMPARACION,
    MALLA_CDF,
    MALLA_FC,
    MALLA_FGM,
    ORDEN_MAXIMO_MOMENTOS_COMPARACION,
    SEED_MINSTD,
    construir_comparacion_generadores,
    construir_muestras_comparacion,
)
from .muestras import (
    construir_muestras,
    muestra_logistica,
    muestra_tienda,
    muestras_regla_30,
)
from .invariancia import (
    ITERACIONES_INVARIANCIA,
    NUM_PARTICULAS_INVARIANCIA,
    SEED_INVARIANCIA,
    aplicar_logistico,
    aplicar_tienda,
    construir_experimentos_invariancia,
    evolucion_ensemble,
    muestra_inicial_logistica,
    muestra_inicial_tienda,
)
from .parametros import (
    FACTOR_TIENDA,
    NUM_CELDAS,
    NUM_ITERACIONES,
    NUM_VALORES,
    SEED,
)
from .reordenamiento import (
    INTERVALOS_BRECHAS,
    LAGS_REORDENAMIENTO,
    SEED_REORDENAMIENTO,
    construir_experimentos_reordenamiento,
    construir_permutaciones_reordenamiento,
    fingerprint_permutacion,
)

__all__ = (
    "LAGS_COMPARACION",
    "MALLA_CDF",
    "MALLA_FC",
    "MALLA_FGM",
    "ORDEN_MAXIMO_MOMENTOS_COMPARACION",
    "SEED_MINSTD",
    "construir_comparacion_generadores",
    "construir_muestras_comparacion",
    "FACTOR_TIENDA",
    "NUM_CELDAS",
    "NUM_ITERACIONES",
    "NUM_VALORES",
    "SEED",
    "ITERACIONES_INVARIANCIA",
    "NUM_PARTICULAS_INVARIANCIA",
    "SEED_INVARIANCIA",
    "aplicar_logistico",
    "aplicar_tienda",
    "construir_experimentos_invariancia",
    "evolucion_ensemble",
    "muestra_inicial_logistica",
    "muestra_inicial_tienda",
    "construir_muestras",
    "muestra_logistica",
    "muestra_tienda",
    "muestras_regla_30",
    "INTERVALOS_BRECHAS",
    "LAGS_REORDENAMIENTO",
    "SEED_REORDENAMIENTO",
    "construir_experimentos_reordenamiento",
    "construir_permutaciones_reordenamiento",
    "fingerprint_permutacion",
)
