"""Figuras y CSV de la comparación homogénea de generadores."""

import csv
import hashlib
from pathlib import Path
import shutil
from typing import Dict, Mapping

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from tesis_generacion.estadistica import (
    autocorrelaciones_empiricas,
    cdf_uniforme_01,
    momentos_ordinarios,
    momentos_teoricos_uniforme,
    pmf_geometrica,
    tiempos_espera_brechas,
)
from tesis_generacion.experimentos.comparacion_generadores import (
    LAGS_COMPARACION,
    ORDEN_MAXIMO_MOMENTOS_COMPARACION,
    construir_comparacion_generadores,
    construir_muestras_comparacion,
)
from tesis_generacion.experimentos.parametros import (
    INTERVALOS_BRECHAS_COMUNES,
    PROBABILIDAD_BRECHAS,
)


ETIQUETAS_COMPARACION = {
    "logistico": "Logístico uniformizado",
    "tienda": "Mapeo tienda",
    "r30_columnas": "R30 columnas",
    "r30_filas": "R30 filas",
    "congruencial_minstd": "Congruencial MINSTD",
}

ARCHIVOS_REFERENCIA_COMPARACION = (
    "cdf_comparacion.png",
    "errores_momentos_comparacion.png",
    "acf_comparacion.png",
    "brechas_comparacion_i1.png",
    "brechas_comparacion_i2.png",
    "brechas_comparacion_i3.png",
    "resumen_comparacion.csv",
    "resumen_brechas_comparacion.csv",
)


def _guardar_figura(figura: plt.Figure, ruta: Path) -> None:
    figura.savefig(
        ruta,
        dpi=200,
        metadata={"Software": "regenerar_comparacion_generadores.py"},
    )
    plt.close(figura)


def _sha256_archivo(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def _preparar_ejes(titulo: str):
    figura, ejes = plt.subplots(
        2, 3, figsize=(11.0, 6.6), sharex=True, constrained_layout=True
    )
    figura.suptitle(titulo)
    ejes_planos = list(ejes.flat)
    ejes_planos[-1].axis("off")
    return figura, ejes_planos[:-1]


def guardar_cdf_comparacion(
    ruta: Path, muestras: Mapping[str, np.ndarray]
) -> None:
    """Compara cada CDF empírica con Uniforme(0,1) en paneles separados."""

    figura, ejes = _preparar_ejes("Diagnóstico marginal por CDF")
    malla = np.linspace(0.0, 1.0, 1001)
    for eje, (nombre, valores) in zip(ejes, muestras.items()):
        ordenados = np.sort(np.asarray(valores, dtype=float))
        empirica = np.searchsorted(ordenados, malla, side="right") / len(
            ordenados
        )
        eje.step(malla, empirica, where="post", linewidth=1.3, label="Empírica")
        eje.plot(
            malla,
            cdf_uniforme_01(malla),
            color="black",
            linestyle="--",
            linewidth=1.4,
            label="Uniforme(0,1)",
        )
        eje.set(title=ETIQUETAS_COMPARACION[nombre], xlim=(0, 1), ylim=(0, 1))
        eje.grid(alpha=0.25)
    ejes[0].legend(fontsize=8)
    figura.supxlabel("x")
    figura.supylabel("Función de distribución acumulada")
    _guardar_figura(figura, ruta)


def guardar_errores_momentos_comparacion(
    ruta: Path, muestras: Mapping[str, np.ndarray]
) -> None:
    """Muestra los errores de los primeros 20 momentos en paneles comunes."""

    figura, ejes = _preparar_ejes("Errores de momentos respecto de Uniforme(0,1)")
    ordenes = np.arange(1, ORDEN_MAXIMO_MOMENTOS_COMPARACION + 1)
    teoricos = np.asarray(
        momentos_teoricos_uniforme(ORDEN_MAXIMO_MOMENTOS_COMPARACION)
    )
    errores = {
        nombre: np.abs(
            np.asarray(
                momentos_ordinarios(
                    valores, ORDEN_MAXIMO_MOMENTOS_COMPARACION
                )
            )
            - teoricos
        )
        for nombre, valores in muestras.items()
    }
    limite = 1.08 * max(float(np.max(valores)) for valores in errores.values())
    for eje, (nombre, valores) in zip(ejes, errores.items()):
        eje.plot(ordenes, valores, marker="o", markersize=3.2, linewidth=1.2)
        eje.set(
            title=ETIQUETAS_COMPARACION[nombre],
            xlim=(1, ORDEN_MAXIMO_MOMENTOS_COMPARACION),
            ylim=(0, limite),
            xticks=(1, 5, 10, 15, 20),
        )
        eje.grid(alpha=0.25)
    figura.supxlabel("Orden k")
    figura.supylabel(r"Error absoluto $|m_k^{emp}-1/(k+1)|$")
    _guardar_figura(figura, ruta)


def guardar_acf_comparacion(
    ruta: Path, muestras: Mapping[str, np.ndarray]
) -> None:
    """Muestra la ACF original para los rezagos 1 a 20."""

    figura, ejes = _preparar_ejes("Dependencia serial: ACF de muestras originales")
    lags = np.asarray(LAGS_COMPARACION)
    coeficientes = {
        nombre: autocorrelaciones_empiricas(valores, lags)
        for nombre, valores in muestras.items()
    }
    limite = max(
        0.1,
        1.08
        * max(float(np.max(np.abs(valores))) for valores in coeficientes.values()),
    )
    for eje, (nombre, valores) in zip(ejes, coeficientes.items()):
        eje.axhline(0.0, color="black", linewidth=0.8)
        eje.plot(lags, valores, marker="o", markersize=3.2, linewidth=1.2)
        eje.set(
            title=ETIQUETAS_COMPARACION[nombre],
            xlim=(1, 20),
            ylim=(-limite, limite),
            xticks=(1, 5, 10, 15, 20),
        )
        eje.grid(alpha=0.25)
    figura.supxlabel("Rezago k")
    figura.supylabel(r"Autocorrelación empírica $\widehat{\rho}(k)$")
    _guardar_figura(figura, ruta)


def _pmf_empirica(tiempos: np.ndarray, maximo: int) -> np.ndarray:
    conteos = np.bincount(tiempos, minlength=maximo + 1)[1 : maximo + 1]
    return conteos / tiempos.size


def guardar_brechas_comparacion(
    ruta: Path,
    muestras: Mapping[str, np.ndarray],
    intervalo_id: str,
    alpha: float,
    beta: float,
) -> None:
    """Compara cinco PMF con una referencia geométrica común."""

    tiempos = {
        nombre: tiempos_espera_brechas(valores, alpha, beta)[0]
        for nombre, valores in muestras.items()
    }
    maximo = max(int(np.max(valores)) for valores in tiempos.values())
    soporte = np.arange(1, maximo + 1, dtype=np.int64)
    teorica = pmf_geometrica(soporte, PROBABILIDAD_BRECHAS)
    figura, ejes = _preparar_ejes(
        "Prueba de brechas común: "
        + rf"{intervalo_id.upper()} $=({alpha:g},{beta:g})$, "
        + rf"$p={PROBABILIDAD_BRECHAS:.1f}$"
    )
    for eje, (nombre, valores) in zip(ejes, tiempos.items()):
        eje.plot(
            soporte,
            _pmf_empirica(valores, maximo),
            marker="o",
            markersize=3.2,
            linewidth=1.2,
            label="Empírica",
        )
        eje.plot(
            soporte,
            teorica,
            color="black",
            linestyle="--",
            linewidth=1.5,
            label="Geométrica teórica",
        )
        eje.set(
            title=ETIQUETAS_COMPARACION[nombre],
            xlim=(0.5, maximo + 0.5),
            ylim=(0.0, None),
        )
        eje.grid(alpha=0.25)
    ejes[0].legend(fontsize=8)
    figura.supxlabel(r"Tiempo de espera $W=G+1$")
    figura.supylabel("Función de masa de probabilidad")
    _guardar_figura(figura, ruta)


def _escribir_csv(ruta: Path, resumen: Mapping[str, object]) -> None:
    campos = (
        "muestra",
        "n",
        "cdf_dmax",
        "cdf_mae",
        "momentos_max_error_20",
        "momentos_mae_20",
        "fgm_dmax",
        "fgm_mae",
        "fc_dmax",
        "fc_mae",
        "acf_rho1",
        "acf_max_abs",
        "acf_mae_abs",
        "fingerprint",
    )
    with ruta.open("w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos, lineterminator="\n")
        escritor.writeheader()
        for nombre, datos in resumen["muestras"].items():
            escritor.writerow(
                {
                    "muestra": nombre,
                    "n": datos["n"],
                    "cdf_dmax": datos["cdf"]["maxima_discrepancia_cdf"],
                    "cdf_mae": datos["cdf"]["mae_cdf"],
                    "momentos_max_error_20": datos["momentos"][
                        "maximo_error_absoluto"
                    ],
                    "momentos_mae_20": datos["momentos"]["mae"],
                    "fgm_dmax": datos["fgm"]["maxima_diferencia_absoluta"],
                    "fgm_mae": datos["fgm"]["mae"],
                    "fc_dmax": datos["funcion_caracteristica"][
                        "maxima_diferencia_absoluta"
                    ],
                    "fc_mae": datos["funcion_caracteristica"]["mae"],
                    "acf_rho1": datos["acf"]["abs_rho_1"],
                    "acf_max_abs": datos["acf"]["max_abs_acf"],
                    "acf_mae_abs": datos["acf"]["mae_abs_acf"],
                    "fingerprint": datos["fingerprint"]["sha256"],
                }
            )


def _escribir_csv_brechas(ruta: Path, resumen: Mapping[str, object]) -> None:
    campos = (
        "muestra",
        "intervalo_id",
        "alpha",
        "beta",
        "p",
        "brechas",
        "racha_final_incompleta",
        "media_w",
        "max_w",
        "dmax",
        "mae",
    )
    with ruta.open("w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos, lineterminator="\n")
        escritor.writeheader()
        for nombre, datos in resumen["muestras"].items():
            for intervalo_id, brechas in datos["brechas"].items():
                escritor.writerow(
                    {
                        "muestra": nombre,
                        "intervalo_id": intervalo_id,
                        "alpha": brechas["alpha"],
                        "beta": brechas["beta"],
                        "p": brechas["p"],
                        "brechas": brechas["brechas_completas"],
                        "racha_final_incompleta": brechas[
                            "racha_final_incompleta"
                        ],
                        "media_w": brechas["media_tiempo_espera"],
                        "max_w": brechas["maximo_tiempo_espera"],
                        "dmax": brechas["maxima_discrepancia_cdf"],
                        "mae": brechas["mae_cdf"],
                    }
                )


def regenerar_comparacion_generadores(directorio: Path) -> Dict[str, object]:
    """Regenera figuras, CSV y resumen numérico del bloque 13."""

    directorio = Path(directorio)
    directorio.mkdir(parents=True, exist_ok=True)
    muestras = construir_muestras_comparacion()
    resumen = construir_comparacion_generadores()
    guardar_cdf_comparacion(directorio / "cdf_comparacion.png", muestras)
    guardar_errores_momentos_comparacion(
        directorio / "errores_momentos_comparacion.png", muestras
    )
    guardar_acf_comparacion(directorio / "acf_comparacion.png", muestras)
    for intervalo_id, (alpha, beta) in INTERVALOS_BRECHAS_COMUNES.items():
        guardar_brechas_comparacion(
            directorio / f"brechas_comparacion_{intervalo_id}.png",
            muestras,
            intervalo_id,
            alpha,
            beta,
        )
    _escribir_csv(directorio / "resumen_comparacion.csv", resumen)
    _escribir_csv_brechas(
        directorio / "resumen_brechas_comparacion.csv", resumen
    )
    resumen["figuras"] = {
        nombre: _sha256_archivo(directorio / nombre)
        for nombre in ARCHIVOS_REFERENCIA_COMPARACION
        if nombre.endswith(".png")
    }
    resumen["archivos"] = list(ARCHIVOS_REFERENCIA_COMPARACION)
    return resumen


def copiar_referencias_comparacion(origen: Path, destino: Path) -> None:
    """Copia las referencias aprobadas solo por solicitud explícita."""

    origen = Path(origen)
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    for nombre in ARCHIVOS_REFERENCIA_COMPARACION:
        shutil.copyfile(origen / nombre, destino / nombre)
