"""Momentos y estadísticas descriptivas empíricas explícitas."""

import numbers
from typing import Dict, Sequence

import numpy as np


def _validar_orden(nombre: str, orden: int) -> int:
    if isinstance(orden, bool) or not isinstance(orden, numbers.Integral):
        raise TypeError(f"{nombre} debe ser un entero")
    orden = int(orden)
    if orden < 1:
        raise ValueError(f"{nombre} debe ser mayor o igual que 1")
    return orden


def _validar_valores(valores: Sequence[float]) -> np.ndarray:
    muestra = np.asarray(valores, dtype=float)
    if muestra.ndim != 1:
        raise ValueError("valores debe ser un arreglo unidimensional")
    if muestra.size == 0:
        raise ValueError("valores no puede estar vacío")
    if not np.all(np.isfinite(muestra)):
        raise ValueError("valores contiene NaN o infinito")
    return muestra


def _promedio_potencia(valores: np.ndarray, orden: int) -> float:
    with np.errstate(over="ignore", invalid="ignore"):
        resultado = float(np.mean(valores**orden))
    if not np.isfinite(resultado):
        raise ValueError("el momento no es finito")
    return resultado


def momento_ordinario(valores: Sequence[float], orden: int) -> float:
    """Devuelve (1/n) sum_i x_i^orden, respecto del origen."""

    orden = _validar_orden("orden", orden)
    muestra = _validar_valores(valores)
    return _promedio_potencia(muestra, orden)


def momentos_ordinarios(
    valores: Sequence[float], orden_maximo: int
) -> list[float]:
    """Devuelve los momentos ordinarios de órdenes 1 a orden_maximo."""

    orden_maximo = _validar_orden("orden_maximo", orden_maximo)
    muestra = _validar_valores(valores)
    return [
        _promedio_potencia(muestra, orden)
        for orden in range(1, orden_maximo + 1)
    ]


def momento_central(valores: Sequence[float], orden: int) -> float:
    """Devuelve el momento empírico central con divisor n."""

    orden = _validar_orden("orden", orden)
    muestra = _validar_valores(valores)
    centrados = muestra - float(np.mean(muestra))
    return _promedio_potencia(centrados, orden)


def varianza_empirica(valores: Sequence[float]) -> float:
    """Devuelve el segundo momento central empírico, con divisor n."""

    return momento_central(valores, 2)


def asimetria_fisher_pearson(valores: Sequence[float]) -> float:
    """Devuelve mu_3 / mu_2^(3/2), sin corrección por sesgo."""

    muestra = _validar_valores(valores)
    varianza = momento_central(muestra, 2)
    if varianza == 0.0:
        raise ValueError("la asimetría no está definida si la varianza es cero")
    return momento_central(muestra, 3) / varianza**1.5


def curtosis_pearson(valores: Sequence[float]) -> float:
    """Devuelve beta_2 = mu_4 / mu_2^2, sin corrección por sesgo."""

    muestra = _validar_valores(valores)
    varianza = momento_central(muestra, 2)
    if varianza == 0.0:
        raise ValueError("la curtosis no está definida si la varianza es cero")
    return momento_central(muestra, 4) / varianza**2


def exceso_curtosis(valores: Sequence[float]) -> float:
    """Devuelve el exceso de curtosis gamma_2 = beta_2 - 3."""

    return curtosis_pearson(valores) - 3.0


def momentos_teoricos_uniforme(orden_maximo: int) -> list[float]:
    """Devuelve E[U^k] = 1/(k+1) para U uniforme en [0,1]."""

    orden_maximo = _validar_orden("orden_maximo", orden_maximo)
    return [1.0 / (orden + 1) for orden in range(1, orden_maximo + 1)]


def resumen_momentos(
    valores: Sequence[float], orden_maximo: int
) -> Dict[str, object]:
    """Resume momentos plug-in; ninguna cantidad se corrige por sesgo."""

    orden_maximo = _validar_orden("orden_maximo", orden_maximo)
    muestra = _validar_valores(valores)
    pearson = curtosis_pearson(muestra)
    return {
        "n": int(muestra.size),
        "media": float(np.mean(muestra)),
        "varianza": varianza_empirica(muestra),
        "asimetria_fisher_pearson": asimetria_fisher_pearson(muestra),
        "curtosis_pearson": pearson,
        "exceso_curtosis": pearson - 3.0,
        "momentos_ordinarios": momentos_ordinarios(muestra, orden_maximo),
    }


def resumen_uniforme_teorica(orden_maximo: int) -> Dict[str, object]:
    """Resume los valores poblacionales de la uniforme en [0,1]."""

    return {
        "n": None,
        "media": 0.5,
        "varianza": 1.0 / 12.0,
        "asimetria_fisher_pearson": 0.0,
        "curtosis_pearson": 9.0 / 5.0,
        "exceso_curtosis": -6.0 / 5.0,
        "momentos_ordinarios": momentos_teoricos_uniforme(orden_maximo),
    }
