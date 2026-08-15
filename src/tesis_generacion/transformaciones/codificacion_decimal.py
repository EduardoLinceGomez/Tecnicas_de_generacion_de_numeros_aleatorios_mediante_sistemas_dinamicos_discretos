"""Codificación decimal reproducible establecida para MCF-036."""

import math
import numbers


PRECISION_DECIMAL = 12
TIPOS_DECIMALES = frozenset("0123456789")


def _validar_precision(precision: int) -> int:
    if isinstance(precision, bool) or not isinstance(
        precision, numbers.Integral
    ):
        raise TypeError("precision debe ser un entero")
    precision = int(precision)
    if precision < 1:
        raise ValueError("precision debe ser mayor o igual que 1")
    return precision


def extraer_digitos(u: float, precision: int = PRECISION_DECIMAL) -> str:
    """Trunca u y devuelve exactamente precision dígitos decimales.

    La conversión mediante la razón binaria exacta del float evita que la
    multiplicación en punto flotante redondee accidentalmente hacia una
    potencia de diez. Los ceros iniciales se conservan.
    """

    precision = _validar_precision(precision)
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
