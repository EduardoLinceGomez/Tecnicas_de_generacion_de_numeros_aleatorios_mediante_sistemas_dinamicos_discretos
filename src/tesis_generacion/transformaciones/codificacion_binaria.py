"""Codificación histórica de palabras binarias como valores normalizados."""


def factor_normalizacion_binaria(longitud: int) -> float:
    """Calcula el factor histórico determinado por una palabra de unos."""

    return 1 / int("1" * longitud, 2)


def codificar_palabra_binaria(bits, factor_normalizacion: float) -> float:
    """Interpreta la palabra mediante su cadena binaria y aplica el factor."""

    valores = bits.tolist() if hasattr(bits, "tolist") else bits
    return int("".join(map(str, valores)), 2) * factor_normalizacion
