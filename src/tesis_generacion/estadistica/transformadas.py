"""Transformadas empíricas y teóricas usadas en la tesis."""

from typing import Dict, Sequence, Union

import numpy as np


EscalarOArreglo = Union[float, complex, np.ndarray]


def _validar_valores(valores: Sequence[float]) -> np.ndarray:
    muestra = np.asarray(valores, dtype=float)
    if muestra.ndim != 1:
        raise ValueError("valores debe ser un arreglo unidimensional")
    if muestra.size == 0:
        raise ValueError("valores no puede estar vacío")
    if not np.all(np.isfinite(muestra)):
        raise ValueError("valores contiene NaN o infinito")
    return muestra


def _validar_parametro(t: Union[float, Sequence[float]]) -> np.ndarray:
    parametro = np.asarray(t, dtype=float)
    if parametro.ndim > 1:
        raise ValueError("t debe ser escalar o un arreglo unidimensional")
    if not np.all(np.isfinite(parametro)):
        raise ValueError("t contiene NaN o infinito")
    return parametro


def _restaurar_forma(resultado: np.ndarray, escalar: bool) -> EscalarOArreglo:
    if escalar:
        return resultado.reshape(-1)[0].item()
    return resultado


def fgm_empirica(
    valores: Sequence[float], t: Union[float, Sequence[float]]
) -> EscalarOArreglo:
    """Evalúa (1/n) sum_j exp(t x_j) en uno o varios valores de t."""

    muestra = _validar_valores(valores)
    parametro = _validar_parametro(t)
    escalar = parametro.ndim == 0
    parametro_plano = np.atleast_1d(parametro)
    with np.errstate(over="ignore", invalid="ignore"):
        resultado = np.mean(
            np.exp(np.multiply.outer(parametro_plano, muestra)), axis=1
        )
    if not np.all(np.isfinite(resultado)):
        raise ValueError("la FGM empírica no es finita para el dominio indicado")
    return _restaurar_forma(resultado, escalar)


def funcion_caracteristica_empirica(
    valores: Sequence[float], t: Union[float, Sequence[float]]
) -> EscalarOArreglo:
    """Evalúa (1/n) sum_j exp(i t x_j) en uno o varios valores de t."""

    muestra = _validar_valores(valores)
    parametro = _validar_parametro(t)
    escalar = parametro.ndim == 0
    parametro_plano = np.atleast_1d(parametro)
    resultado = np.mean(
        np.exp(1j * np.multiply.outer(parametro_plano, muestra)), axis=1
    )
    if not np.all(np.isfinite(resultado)):
        raise ValueError(
            "la función característica empírica no es finita para el dominio indicado"
        )
    return _restaurar_forma(resultado, escalar)


def fgm_uniforme(t: Union[float, Sequence[float]]) -> EscalarOArreglo:
    """Evalúa M_U(t) = (exp(t)-1)/t, con M_U(0)=1."""

    parametro = _validar_parametro(t)
    escalar = parametro.ndim == 0
    parametro_plano = np.atleast_1d(parametro)
    resultado = np.ones_like(parametro_plano, dtype=float)
    no_cero = parametro_plano != 0.0
    with np.errstate(over="ignore", invalid="ignore"):
        resultado[no_cero] = (
            np.expm1(parametro_plano[no_cero]) / parametro_plano[no_cero]
        )
    if not np.all(np.isfinite(resultado)):
        raise ValueError("la FGM uniforme no es finita para el dominio indicado")
    return _restaurar_forma(resultado, escalar)


def funcion_caracteristica_uniforme(
    t: Union[float, Sequence[float]],
) -> EscalarOArreglo:
    """Evalúa phi_U(t) = (exp(i t)-1)/(i t), con phi_U(0)=1."""

    parametro = _validar_parametro(t)
    escalar = parametro.ndim == 0
    parametro_plano = np.atleast_1d(parametro)
    resultado = np.ones_like(parametro_plano, dtype=complex)
    no_cero = parametro_plano != 0.0
    argumento = 1j * parametro_plano[no_cero]
    resultado[no_cero] = np.expm1(argumento) / argumento
    return _restaurar_forma(resultado, escalar)


def metricas_error_transformada(
    observado: Sequence[complex], teorico: Sequence[complex]
) -> Dict[str, float]:
    """Resume el máximo y la media del error absoluto complejo."""

    observado_arr = np.asarray(observado)
    teorico_arr = np.asarray(teorico)
    if observado_arr.ndim != 1 or teorico_arr.ndim != 1:
        raise ValueError("las transformadas deben ser arreglos unidimensionales")
    if observado_arr.size == 0:
        raise ValueError("las transformadas no pueden estar vacías")
    if observado_arr.shape != teorico_arr.shape:
        raise ValueError("las transformadas deben tener la misma forma")
    if not np.all(np.isfinite(observado_arr)) or not np.all(
        np.isfinite(teorico_arr)
    ):
        raise ValueError("las transformadas contienen NaN o infinito")
    errores = np.abs(observado_arr - teorico_arr)
    return {
        "maxima_diferencia_absoluta": float(np.max(errores)),
        "mae": float(np.mean(errores)),
    }
