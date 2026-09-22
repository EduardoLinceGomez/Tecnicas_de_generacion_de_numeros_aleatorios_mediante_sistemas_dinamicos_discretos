"""Adaptador temporal para la API histórica del coleccionista de cupones."""

from tesis_generacion.estadistica.coleccionista import (
    cdf_coleccionista,
    longitudes_coleccionista,
    media_teorica_coleccionista,
    pmf_coleccionista,
)
from tesis_generacion.transformaciones.codificacion_decimal import (
    PRECISION_DECIMAL,
    TIPOS_DECIMALES,
    extraer_digitos,
)
