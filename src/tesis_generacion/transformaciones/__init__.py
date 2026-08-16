"""Transformaciones puras usadas por los experimentos de la tesis."""

from .codificacion_binaria import (
    codificar_matriz_por_columnas,
    codificar_matriz_por_filas,
    codificar_palabra_binaria,
    factor_normalizacion_binaria,
)
from .codificacion_decimal import PRECISION_DECIMAL, extraer_digitos
from .uniformizacion import uniformizar_beta
from .reordenamiento import (
    aplicar_permutacion,
    generar_permutacion_por_ranking,
    validar_permutacion,
)

__all__ = (
    "PRECISION_DECIMAL",
    "codificar_matriz_por_columnas",
    "codificar_matriz_por_filas",
    "codificar_palabra_binaria",
    "extraer_digitos",
    "factor_normalizacion_binaria",
    "aplicar_permutacion",
    "generar_permutacion_por_ranking",
    "validar_permutacion",
    "uniformizar_beta",
)
