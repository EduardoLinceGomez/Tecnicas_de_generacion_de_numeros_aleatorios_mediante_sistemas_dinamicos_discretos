"""Diagnósticos descriptivos sensibles al orden serial."""

import numbers
from typing import Dict, Sequence, Tuple

import numpy as np


def _validar_muestra(valores: Sequence[float]) -> np.ndarray:
    muestra = np.asarray(valores, dtype=float)
    if muestra.ndim != 1:
        raise ValueError("la muestra debe ser unidimensional")
    if muestra.size == 0:
        raise ValueError("la muestra no puede estar vacía")
    if not np.all(np.isfinite(muestra)):
        raise ValueError("la muestra contiene NaN o infinito")
    return muestra


def _validar_lag(lag: int, n: int) -> int:
    if isinstance(lag, bool) or not isinstance(lag, numbers.Integral):
        raise TypeError("lag debe ser un entero")
    lag = int(lag)
    if not 1 <= lag < n:
        raise ValueError("lag debe satisfacer 1 <= lag < n")
    return lag


def autocorrelacion_empirica(valores: Sequence[float], lag: int) -> float:
    """Calcula la ACF con denominador común sum_j (x_j-media)^2."""

    muestra = _validar_muestra(valores)
    lag = _validar_lag(lag, muestra.size)
    centrados = muestra - float(np.mean(muestra))
    denominador = float(np.dot(centrados, centrados))
    if denominador == 0.0:
        raise ValueError("la autocorrelación no está definida si la varianza es cero")
    return float(np.dot(centrados[:-lag], centrados[lag:]) / denominador)


def autocorrelaciones_empiricas(
    valores: Sequence[float], lags: Sequence[int]
) -> np.ndarray:
    """Evalúa la misma convención de ACF en todos los lags indicados."""

    muestra = _validar_muestra(valores)
    lags_arr = np.asarray(lags)
    if lags_arr.ndim != 1 or lags_arr.size == 0:
        raise ValueError("lags debe ser un arreglo unidimensional no vacío")
    if lags_arr.dtype.kind not in "iu":
        raise TypeError("los lags deben ser enteros")
    return np.asarray(
        [autocorrelacion_empirica(muestra, int(lag)) for lag in lags_arr],
        dtype=float,
    )


def resumen_autocorrelaciones(
    valores: Sequence[float], lags: Sequence[int]
) -> Dict[str, float]:
    """Resume magnitudes de ACF sin convertirlas en una prueba de hipótesis."""

    coeficientes = autocorrelaciones_empiricas(valores, lags)
    magnitudes = np.abs(coeficientes)
    return {
        "abs_rho_1": abs(autocorrelacion_empirica(valores, 1)),
        "max_abs_acf": float(np.max(magnitudes)),
        "mae_abs_acf": float(np.mean(magnitudes)),
    }


def _validar_intervalo(alpha: float, beta: float) -> Tuple[float, float]:
    alpha = float(alpha)
    beta = float(beta)
    if not np.isfinite(alpha) or not np.isfinite(beta):
        raise ValueError("los extremos del intervalo deben ser finitos")
    if not 0.0 <= alpha < beta <= 1.0:
        raise ValueError("el intervalo debe satisfacer 0 <= alpha < beta <= 1")
    if beta - alpha == 1.0:
        raise ValueError("la probabilidad de éxito debe estar en (0,1)")
    return alpha, beta


def tiempos_espera_brechas(
    valores: Sequence[float], alpha: float, beta: float
) -> Tuple[np.ndarray, int]:
    """Registra W=G+1 para éxitos en (alpha,beta) y la cola censurada."""

    muestra = _validar_muestra(valores)
    alpha, beta = _validar_intervalo(alpha, beta)
    if np.any((muestra < 0.0) | (muestra > 1.0)):
        raise ValueError("la muestra debe estar contenida en [0,1]")
    tiempos = []
    longitud = 1
    for valor in muestra:
        if alpha < valor < beta:
            tiempos.append(longitud)
            longitud = 1
        else:
            longitud += 1
    return np.asarray(tiempos, dtype=np.int64), int(longitud - 1)


def pmf_geometrica(soporte: Sequence[int], p: float) -> np.ndarray:
    """Evalúa p(1-p)^(w-1) para la convención W en {1,2,...}."""

    valores = np.asarray(soporte)
    if valores.ndim != 1 or valores.size == 0:
        raise ValueError("el soporte debe ser unidimensional no vacío")
    if valores.dtype.kind not in "iu" or np.any(valores < 1):
        raise ValueError("el soporte debe contener enteros positivos")
    p = float(p)
    if not np.isfinite(p) or not 0.0 < p < 1.0:
        raise ValueError("p debe pertenecer a (0,1)")
    return p * (1.0 - p) ** (valores.astype(float) - 1.0)


def resumen_brechas(
    valores: Sequence[float], alpha: float, beta: float
) -> Dict[str, float]:
    """Compara la CDF empírica de W con Geom(beta-alpha)."""

    alpha, beta = _validar_intervalo(alpha, beta)
    tiempos, cola = tiempos_espera_brechas(valores, alpha, beta)
    if tiempos.size == 0:
        raise ValueError("la muestra no contiene brechas completas")
    maximo = int(np.max(tiempos))
    soporte = np.arange(1, maximo + 1, dtype=np.int64)
    cdf_empirica = np.searchsorted(np.sort(tiempos), soporte, side="right") / tiempos.size
    p = beta - alpha
    cdf_teorica = 1.0 - (1.0 - p) ** soporte
    diferencias = np.abs(cdf_empirica - cdf_teorica)
    return {
        "alpha": alpha,
        "beta": beta,
        "p": p,
        "brechas_completas": int(tiempos.size),
        "cola_censurada": cola,
        "media_tiempo_espera": float(np.mean(tiempos)),
        "maximo_tiempo_espera": maximo,
        "maxima_discrepancia_cdf": float(np.max(diferencias)),
        "mae_cdf": float(np.mean(diferencias)),
    }
