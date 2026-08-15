"""Transformaciones puras usadas por los experimentos de la tesis."""

from .codificacion_binaria import (
    codificar_palabra_binaria,
    factor_normalizacion_binaria,
)
from .codificacion_decimal import PRECISION_DECIMAL, extraer_digitos
from .uniformizacion import uniformizar_beta

__all__ = (
    "PRECISION_DECIMAL",
    "codificar_palabra_binaria",
    "extraer_digitos",
    "factor_normalizacion_binaria",
    "uniformizar_beta",
)
