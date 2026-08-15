"""CDF objetivo y métricas para evolución de distribuciones."""

import hashlib
from typing import Dict

import numpy as np


def _validar_valores(valores: np.ndarray) -> np.ndarray:
    muestra = np.asarray(valores, dtype=float)
    if muestra.ndim != 1:
        raise ValueError("la muestra debe ser unidimensional")
    if muestra.size == 0:
        raise ValueError("la muestra no puede estar vacía")
    if not np.all(np.isfinite(muestra)):
        raise ValueError("la muestra contiene NaN o infinito")
    return muestra


def cdf_uniforme_01(x):
    """Evalúa la CDF de Uniforme(0,1)."""

    valores = np.asarray(x, dtype=float)
    resultado = np.clip(valores, 0.0, 1.0)
    return float(resultado) if resultado.ndim == 0 else resultado


def cdf_beta_medio(x):
    """Evalúa la CDF de Beta(1/2,1/2) mediante su fórmula cerrada."""

    valores = np.asarray(x, dtype=float)
    recortados = np.clip(valores, 0.0, 1.0)
    resultado = (2.0 / np.pi) * np.arcsin(np.sqrt(recortados))
    resultado = np.where(valores < 0.0, 0.0, resultado)
    resultado = np.where(valores > 1.0, 1.0, resultado)
    return float(resultado) if resultado.ndim == 0 else resultado


def metricas_discrepancia_cdf(
    valores: np.ndarray,
    cdf_objetivo,
    malla: np.ndarray = None,
) -> Dict[str, float]:
    """Calcula máxima discrepancia CDF y MAE sobre una malla fija."""

    muestra = np.sort(_validar_valores(valores))
    n = muestra.size
    objetivo_en_muestra = np.asarray(cdf_objetivo(muestra), dtype=float)
    escalones_derecha = np.arange(1, n + 1, dtype=float) / n
    escalones_izquierda = np.arange(0, n, dtype=float) / n
    maxima = max(
        float(np.max(np.abs(escalones_derecha - objetivo_en_muestra))),
        float(np.max(np.abs(escalones_izquierda - objetivo_en_muestra))),
    )

    if malla is None:
        malla = np.linspace(0.0, 1.0, 1001)
    puntos = np.asarray(malla, dtype=float)
    if puntos.ndim != 1 or puntos.size == 0:
        raise ValueError("la malla debe ser un arreglo unidimensional no vacío")
    if not np.all(np.isfinite(puntos)):
        raise ValueError("la malla contiene NaN o infinito")
    empirica = np.searchsorted(muestra, puntos, side="right") / n
    objetivo = np.asarray(cdf_objetivo(puntos), dtype=float)
    return {
        "maxima_discrepancia_cdf": maxima,
        "mae_cdf": float(np.mean(np.abs(empirica - objetivo))),
    }


def fingerprint_ensemble(valores: np.ndarray) -> Dict[str, object]:
    """Devuelve un fingerprint estable de un ensemble de flotantes."""

    muestra = np.ascontiguousarray(_validar_valores(valores), dtype="<f8")
    return {
        "n_elementos": int(muestra.size),
        "n_bytes": int(muestra.nbytes),
        "dtype": muestra.dtype.str,
        "endianness": "little",
        "sha256": hashlib.sha256(muestra.tobytes(order="C")).hexdigest(),
    }
