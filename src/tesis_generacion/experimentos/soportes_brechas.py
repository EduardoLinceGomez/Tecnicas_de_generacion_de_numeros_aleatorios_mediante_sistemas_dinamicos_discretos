"""Fuente única de las mallas comunes para el EAM de brechas."""

from typing import Dict

import numpy as np

from tesis_generacion.estadistica.dependencia_serial import tiempos_espera_brechas
from tesis_generacion.generadores import muestra_minstd
from tesis_generacion.generadores.logistico import orbita_logistica
from tesis_generacion.transformaciones.reordenamiento import (
    aplicar_permutacion,
    generar_permutacion_por_ranking,
)

from .muestras import construir_muestras
from .parametros import (
    INTERVALOS_BRECHAS_COMUNES,
    NUM_VALORES,
    SEED_MINSTD,
    SEED_REORDENAMIENTO,
)


def construir_permutaciones_reordenamiento() -> Dict[str, Dict[str, object]]:
    """Construye las dos permutaciones por ranking presentes en el notebook."""

    auxiliar_fija = np.asarray(
        orbita_logistica(4.0, 0.02024, NUM_VALORES)[:NUM_VALORES],
        dtype=float,
    )
    rng = np.random.RandomState(SEED_REORDENAMIENTO)
    inicial_sembrado = float(rng.uniform(0.0, 1.0))
    auxiliar_sembrada = np.asarray(
        orbita_logistica(4.0, inicial_sembrado, NUM_VALORES)[:NUM_VALORES],
        dtype=float,
    )
    if np.unique(auxiliar_fija).size != NUM_VALORES:
        raise ValueError("la órbita auxiliar fija contiene empates")
    if np.unique(auxiliar_sembrada).size != NUM_VALORES:
        raise ValueError("la órbita auxiliar sembrada contiene empates")

    return {
        "fija": {
            "metodo": "ranking de órbita logística auxiliar fija",
            "r": 4.0,
            "x0": 0.02024,
            "seed": None,
            "auxiliar": auxiliar_fija,
            "indices": generar_permutacion_por_ranking(auxiliar_fija),
        },
        "sembrada": {
            "metodo": "ranking de órbita logística auxiliar con estado sembrado",
            "r": 4.0,
            "x0": inicial_sembrado,
            "seed": SEED_REORDENAMIENTO,
            "auxiliar": auxiliar_sembrada,
            "indices": generar_permutacion_por_ranking(auxiliar_sembrada),
        },
    }


def construir_participantes_malla_brechas() -> Dict[str, np.ndarray]:
    """Construye las ocho series dinámicas y MINSTD que fijan cada W_j^*."""

    muestras = construir_muestras()
    permutaciones = construir_permutaciones_reordenamiento()
    participantes = {}
    for nombre, original in muestras.items():
        clave = "sembrada" if nombre == "logistico" else "fija"
        participantes[f"{nombre}_original"] = original
        participantes[f"{nombre}_reordenada"] = aplicar_permutacion(
            original, permutaciones[clave]["indices"]
        )
    participantes["congruencial_minstd_original"] = muestra_minstd(
        NUM_VALORES, semilla=SEED_MINSTD
    )
    return participantes


def calcular_maximos_soporte_brechas_comunes() -> Dict[str, int]:
    """Deriva W_j^* sobre los nueve participantes del protocolo AUT-093."""

    participantes = construir_participantes_malla_brechas()
    return {
        intervalo_id: max(
            int(np.max(tiempos_espera_brechas(valores, alpha, beta)[0]))
            for valores in participantes.values()
        )
        for intervalo_id, (alpha, beta) in INTERVALOS_BRECHAS_COMUNES.items()
    }
