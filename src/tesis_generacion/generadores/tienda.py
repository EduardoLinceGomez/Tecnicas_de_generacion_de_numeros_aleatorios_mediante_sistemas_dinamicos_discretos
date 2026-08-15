"""Dinámica determinista del mapeo tienda."""


def paso_tienda(x: float, factor: float) -> float:
    """Calcula una aplicación del mapeo tienda con el factor indicado."""

    if 0.0 <= x < 0.5:
        return factor * x
    if 0.5 <= x < 1.0:
        return factor * (1.0 - x)
    raise ValueError("el estado del mapeo tienda salió de [0,1)")
