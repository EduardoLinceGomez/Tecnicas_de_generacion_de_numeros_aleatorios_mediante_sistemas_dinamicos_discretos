"""Fuente única de la malla común para el EAM del coleccionista."""

from typing import Mapping, Optional, Sequence

from tesis_generacion.estadistica.coleccionista import (
    longitudes_coleccionista,
)
from tesis_generacion.transformaciones.codificacion_decimal import (
    PRECISION_DECIMAL,
)

from .muestras import construir_muestras


MUESTRAS_COLECCIONISTA = (
    "logistico",
    "tienda",
    "r30_columnas",
    "r30_filas",
)


def construir_participantes_malla_coleccionista() -> Mapping[str, Sequence[float]]:
    """Construye las cuatro muestras originales incluidas en AUT-105."""

    muestras = construir_muestras()
    return {nombre: muestras[nombre] for nombre in MUESTRAS_COLECCIONISTA}


def calcular_maximo_soporte_coleccionista_comun(
    muestras: Optional[Mapping[str, Sequence[float]]] = None,
) -> int:
    """Deriva M* como el mayor máximo observado entre las cuatro muestras."""

    participantes = (
        construir_participantes_malla_coleccionista()
        if muestras is None
        else muestras
    )
    if tuple(participantes) != MUESTRAS_COLECCIONISTA:
        raise ValueError(
            "la malla común requiere las cuatro muestras originales en orden canónico"
        )

    maximos = []
    for nombre in MUESTRAS_COLECCIONISTA:
        longitudes, _ = longitudes_coleccionista(
            participantes[nombre], PRECISION_DECIMAL
        )
        if not longitudes:
            raise ValueError(f"{nombre}: no se obtuvo ningún bloque completo")
        maximos.append(max(longitudes))
    return max(maximos)
