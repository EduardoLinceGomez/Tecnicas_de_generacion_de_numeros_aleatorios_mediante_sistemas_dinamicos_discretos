"""Estadística reproducible para la prueba del coleccionista de cupones."""

from collections import Counter
from fractions import Fraction
import math
import numbers
import statistics
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from tesis_generacion.transformaciones.codificacion_decimal import (
    PRECISION_DECIMAL,
    TIPOS_DECIMALES,
    extraer_digitos,
)


def _validar_entero(nombre: str, valor: int, minimo: int) -> int:
    if isinstance(valor, bool) or not isinstance(valor, numbers.Integral):
        raise TypeError(f"{nombre} debe ser un entero")
    valor = int(valor)
    if valor < minimo:
        raise ValueError(f"{nombre} debe ser mayor o igual que {minimo}")
    return valor


def longitudes_coleccionista(
    datos: Iterable[float], precision: int = PRECISION_DECIMAL
) -> Tuple[List[int], int]:
    """Devuelve las longitudes ordenadas y la cola censurada final."""

    precision = _validar_entero("precision", precision, 1)
    longitudes = []  # type: List[int]
    vistos = set()
    longitud_actual = 0

    for u in datos:
        for digito in extraer_digitos(u, precision):
            vistos.add(digito)
            longitud_actual += 1
            if vistos == TIPOS_DECIMALES:
                longitudes.append(longitud_actual)
                vistos.clear()
                longitud_actual = 0

    return longitudes, longitud_actual


def cdf_coleccionista(m: int, k: int = 10) -> float:
    """Función de distribución acumulada del tiempo de colección."""

    m = _validar_entero("m", m, 0)
    k = _validar_entero("k", k, 1)
    if m < k:
        return 0.0

    total = Fraction(0, 1)
    for j in range(k + 1):
        total += (
            (-1) ** j
            * math.comb(k, j)
            * Fraction(k - j, k) ** m
        )
    return float(total)


def pmf_coleccionista(m: int, k: int = 10) -> float:
    """Función de masa de probabilidad del tiempo de colección."""

    m = _validar_entero("m", m, 0)
    k = _validar_entero("k", k, 1)
    return cdf_coleccionista(m, k) - (
        cdf_coleccionista(m - 1, k) if m > 0 else 0.0
    )


def media_teorica_coleccionista(k: int = 10) -> float:
    """Devuelve k H_k, la longitud media teórica de un bloque."""

    k = _validar_entero("k", k, 1)
    return k * sum(1.0 / j for j in range(1, k + 1))


def metricas_coleccionista(
    valores: Sequence[float],
    maximo_soporte: Optional[int] = None,
) -> Tuple[List[int], Dict[str, float]]:
    """Calcula las métricas del coleccionista para una muestra uniforme.

    Si ``maximo_soporte`` se omite, conserva exactamente la convención
    histórica de evaluar hasta la longitud máxima observada. Un soporte
    externo permite comparar el EAM entre muestras sobre la misma malla sin
    alterar los bloques observados.
    """

    longitudes, cola = longitudes_coleccionista(valores, PRECISION_DECIMAL)
    if not longitudes:
        raise ValueError("no se obtuvo ningún bloque completo")

    frecuencias = Counter(longitudes)
    maximo = max(longitudes)
    if maximo_soporte is None:
        maximo_evaluacion = maximo
    else:
        if isinstance(maximo_soporte, bool) or not isinstance(
            maximo_soporte, numbers.Integral
        ):
            raise TypeError("maximo_soporte debe ser un entero")
        maximo_evaluacion = int(maximo_soporte)
        if maximo_evaluacion < maximo:
            raise ValueError(
                "maximo_soporte debe ser mayor o igual que el máximo observado"
            )
    acumulada = 0
    errores = []
    for m in range(10, maximo_evaluacion + 1):
        acumulada += frecuencias.get(m, 0)
        cdf_empirica = acumulada / len(longitudes)
        errores.append(abs(cdf_empirica - cdf_coleccionista(m)))

    media = statistics.fmean(longitudes)
    media_teorica = media_teorica_coleccionista()
    metricas = {
        "numero_u": len(valores),
        "total_digitos": len(valores) * PRECISION_DECIMAL,
        "bloques_completos": len(longitudes),
        "cola_censurada": cola,
        "minimo": min(longitudes),
        "maximo": maximo,
        "media": media,
        "mediana": statistics.median(longitudes),
        "media_teorica": media_teorica,
        "diferencia_media": media - media_teorica,
        "distancia_maxima_cdf": max(errores),
        "mae_cdf": statistics.fmean(errores),
    }
    if maximo_soporte is not None:
        metricas["maximo_soporte_evaluacion"] = maximo_evaluacion
    return longitudes, metricas
