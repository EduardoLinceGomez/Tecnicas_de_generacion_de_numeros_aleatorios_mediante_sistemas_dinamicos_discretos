"""Comparación homogénea de muestras dinámicas y MINSTD."""

from typing import Dict

import numpy as np

from tesis_generacion.estadistica import (
    cdf_uniforme_01,
    fgm_empirica,
    fgm_uniforme,
    fingerprint_ensemble,
    funcion_caracteristica_empirica,
    funcion_caracteristica_uniforme,
    metricas_discrepancia_cdf,
    metricas_error_transformada,
    momentos_ordinarios,
    momentos_teoricos_uniforme,
    resumen_autocorrelaciones,
)
from tesis_generacion.generadores import (
    INCREMENTO_MINSTD,
    MODULO_MINSTD,
    MULTIPLICADOR_MINSTD,
    estados_minstd,
    muestra_minstd,
)

from .muestras import construir_muestras
from .parametros import NUM_VALORES


SEED_MINSTD = 2024
ORDEN_MAXIMO_MOMENTOS_COMPARACION = 20
LAGS_COMPARACION = tuple(range(1, 21))
MALLA_CDF = np.linspace(0.0, 1.0, 1001)
MALLA_FGM = np.linspace(0.0, 15.0, 40)
MALLA_FC = np.linspace(0.0, 20.0, 60)
REFERENCIA_MINSTD = {
    "autores": "S. K. Park y K. W. Miller",
    "anio": 1988,
    "doi": "10.1145/63039.63042",
}


def construir_muestras_comparacion() -> Dict[str, np.ndarray]:
    """Devuelve cinco muestras originales de n=1000, sin reordenamiento."""

    muestras = construir_muestras()
    muestras["congruencial_minstd"] = muestra_minstd(
        NUM_VALORES, semilla=SEED_MINSTD
    )
    if any(len(muestra) != NUM_VALORES for muestra in muestras.values()):
        raise ValueError("todas las muestras deben contener exactamente 1000 valores")
    return muestras


def _resumen_muestra(valores: np.ndarray) -> Dict[str, object]:
    momentos = np.asarray(
        momentos_ordinarios(valores, ORDEN_MAXIMO_MOMENTOS_COMPARACION)
    )
    teoricos = np.asarray(
        momentos_teoricos_uniforme(ORDEN_MAXIMO_MOMENTOS_COMPARACION)
    )
    errores_momentos = np.abs(momentos - teoricos)
    fgm_observada = np.asarray(fgm_empirica(valores, MALLA_FGM), dtype=float)
    fgm_teorica = np.asarray(fgm_uniforme(MALLA_FGM), dtype=float)
    fc_observada = np.asarray(
        funcion_caracteristica_empirica(valores, MALLA_FC), dtype=complex
    )
    fc_teorica = np.asarray(
        funcion_caracteristica_uniforme(MALLA_FC), dtype=complex
    )
    return {
        "n": int(len(valores)),
        "fingerprint": fingerprint_ensemble(valores),
        "cdf": metricas_discrepancia_cdf(
            valores, cdf_uniforme_01, malla=MALLA_CDF
        ),
        "momentos": {
            "orden_maximo": ORDEN_MAXIMO_MOMENTOS_COMPARACION,
            "maximo_error_absoluto": float(np.max(errores_momentos)),
            "mae": float(np.mean(errores_momentos)),
        },
        "fgm": metricas_error_transformada(fgm_observada, fgm_teorica),
        "funcion_caracteristica": metricas_error_transformada(
            fc_observada, fc_teorica
        ),
        "acf": resumen_autocorrelaciones(valores, LAGS_COMPARACION),
    }


def construir_comparacion_generadores() -> Dict[str, object]:
    """Calcula las métricas comunes sin producir una puntuación agregada."""

    muestras = construir_muestras_comparacion()
    estados_control = estados_minstd(10, semilla=SEED_MINSTD)
    return {
        "benchmark": {
            "nombre": "Park--Miller MINSTD (1988)",
            "referencia": REFERENCIA_MINSTD,
            "formula": "X_(n+1)=(a*X_n+c) mod m; U_n=X_n/m",
            "multiplicador": MULTIPLICADOR_MINSTD,
            "incremento": INCREMENTO_MINSTD,
            "modulo": MODULO_MINSTD,
            "semilla": SEED_MINSTD,
            "incluye_semilla": False,
            "numero_valores": NUM_VALORES,
            "primeros_10_estados": estados_control.tolist(),
            "primeros_10_valores": (
                estados_control.astype(float) / MODULO_MINSTD
            ).tolist(),
        },
        "parametros": {
            "n": NUM_VALORES,
            "malla_cdf": {
                "inicio": 0.0,
                "fin": 1.0,
                "numero_puntos": int(MALLA_CDF.size),
            },
            "momentos": list(
                range(1, ORDEN_MAXIMO_MOMENTOS_COMPARACION + 1)
            ),
            "malla_fgm": {
                "inicio": 0.0,
                "fin": 15.0,
                "numero_puntos": int(MALLA_FGM.size),
            },
            "malla_funcion_caracteristica": {
                "inicio": 0.0,
                "fin": 20.0,
                "numero_puntos": int(MALLA_FC.size),
            },
            "lags_acf": list(LAGS_COMPARACION),
            "usa_muestras_reordenadas": False,
        },
        "muestras": {
            nombre: _resumen_muestra(valores)
            for nombre, valores in muestras.items()
        },
    }
