"""Herramientas reproducibles para la prueba del coleccionista de cupones."""

from fractions import Fraction
import math
import numbers
from typing import Iterable, List, Tuple


PRECISION_DECIMAL = 12
TIPOS_DECIMALES = frozenset("0123456789")


def _validar_entero(nombre: str, valor: int, minimo: int) -> int:
    if isinstance(valor, bool) or not isinstance(valor, numbers.Integral):
        raise TypeError(f"{nombre} debe ser un entero")
    valor = int(valor)
    if valor < minimo:
        raise ValueError(f"{nombre} debe ser mayor o igual que {minimo}")
    return valor


def extraer_digitos(u: float, precision: int = PRECISION_DECIMAL) -> str:
    """Trunca u y devuelve exactamente precision dígitos decimales.

    La conversión mediante la razón binaria exacta del float evita que la
    multiplicación en punto flotante redondee accidentalmente hacia una
    potencia de diez. Los ceros iniciales se conservan.
    """

    precision = _validar_entero("precision", precision, 1)
    valor = float(u)
    if not math.isfinite(valor):
        raise ValueError("u debe ser un número finito")
    if not 0.0 <= valor < 1.0:
        raise ValueError("u debe satisfacer 0 <= u < 1")

    numerador, denominador = valor.as_integer_ratio()
    q = (numerador * 10**precision) // denominador
    digitos = f"{q:0{precision}d}"
    if len(digitos) != precision or not set(digitos) <= TIPOS_DECIMALES:
        raise RuntimeError("la extracción no produjo el alfabeto decimal esperado")
    return digitos


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
