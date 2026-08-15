"""Figuras y resumen reproducibles del reordenamiento serial."""

import csv
import hashlib
from pathlib import Path
import shutil
from typing import Dict, Mapping

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from tesis_generacion.estadistica.dependencia_serial import (
    autocorrelaciones_empiricas,
    pmf_geometrica,
    tiempos_espera_brechas,
)
from tesis_generacion.experimentos.reordenamiento import (
    LAGS_REORDENAMIENTO,
    construir_experimentos_reordenamiento,
)


ETIQUETAS_MUESTRAS = {
    "logistico": "Logístico uniformizado",
    "tienda": "Mapeo tienda",
    "r30_columnas": "R30 columnas",
    "r30_filas": "R30 filas",
}

ARCHIVOS_TESIS_REORDENAMIENTO = {
    "logistico": "Log_PG.png",
    "tienda": "Tent_PG.png",
    "r30_columnas": "R30_col_PG.png",
    "r30_filas": "R30_fila_PG.png",
}

ARCHIVOS_REFERENCIA_REORDENAMIENTO = (
    "acf_antes_despues_logistico.png",
    "acf_antes_despues_tienda.png",
    "acf_antes_despues_r30_columnas.png",
    "acf_antes_despues_r30_filas.png",
    "brechas_antes_despues_logistico.png",
    "brechas_antes_despues_tienda.png",
    "brechas_antes_despues_r30_columnas.png",
    "brechas_antes_despues_r30_filas.png",
    "permutacion_indices.png",
    "resumen_reordenamiento.csv",
)


def _guardar_figura(figura: plt.Figure, ruta: Path) -> None:
    figura.savefig(
        ruta,
        dpi=200,
        metadata={"Software": "regenerar_reordenamiento.py"},
    )
    plt.close(figura)


def _sha256_archivo(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def guardar_acf_antes_despues(
    ruta: Path,
    original: np.ndarray,
    reordenada: np.ndarray,
    titulo: str,
) -> None:
    """Grafica la ACF descriptiva para los mismos lags antes y después."""

    lags = np.asarray(LAGS_REORDENAMIENTO)
    acf_original = autocorrelaciones_empiricas(original, lags)
    acf_reordenada = autocorrelaciones_empiricas(reordenada, lags)
    limite = max(
        0.1,
        1.12 * float(np.max(np.abs(np.concatenate((acf_original, acf_reordenada))))),
    )
    figura, eje = plt.subplots(figsize=(7.4, 4.5), constrained_layout=True)
    eje.plot(lags, acf_original, marker="o", markersize=4, label="Original")
    eje.plot(
        lags,
        acf_reordenada,
        marker="s",
        markersize=4,
        label="Reordenada",
    )
    eje.axhline(0.0, color="black", linewidth=0.8)
    eje.set(
        title=f"ACF antes y después: {titulo}",
        xlabel="Rezago k",
        ylabel=r"Autocorrelación empírica $\widehat{\rho}(k)$",
        xticks=lags,
        ylim=(-limite, limite),
    )
    eje.grid(alpha=0.25)
    eje.legend()
    _guardar_figura(figura, ruta)


def _pmf_empirica(tiempos: np.ndarray, maximo: int) -> np.ndarray:
    conteos = np.bincount(tiempos, minlength=maximo + 1)[1 : maximo + 1]
    return conteos / tiempos.size


def guardar_brechas_antes_despues(
    ruta: Path,
    original: np.ndarray,
    reordenada: np.ndarray,
    alpha: float,
    beta: float,
    titulo: str,
) -> None:
    """Compara las PMF empíricas de W=G+1 con la geométrica teórica."""

    tiempos_original, _ = tiempos_espera_brechas(original, alpha, beta)
    tiempos_reordenados, _ = tiempos_espera_brechas(reordenada, alpha, beta)
    maximo = int(max(np.max(tiempos_original), np.max(tiempos_reordenados)))
    soporte = np.arange(1, maximo + 1, dtype=np.int64)
    figura, eje = plt.subplots(figsize=(7.4, 4.5), constrained_layout=True)
    eje.plot(
        soporte,
        _pmf_empirica(tiempos_original, maximo),
        marker="o",
        markersize=4,
        linewidth=1.2,
        label="Original",
    )
    eje.plot(
        soporte,
        _pmf_empirica(tiempos_reordenados, maximo),
        marker="s",
        markersize=4,
        linewidth=1.2,
        label="Reordenada",
    )
    eje.plot(
        soporte,
        pmf_geometrica(soporte, beta - alpha),
        color="black",
        linestyle="--",
        linewidth=1.8,
        label=rf"Geométrica teórica, $p={beta-alpha:.1f}$",
    )
    eje.set(
        title=f"Prueba de brechas: {titulo}",
        xlabel=r"Tiempo de espera $W=G+1$",
        ylabel="Función de masa de probabilidad",
        xlim=(0.5, maximo + 0.5),
    )
    eje.set_ylim(bottom=0.0)
    eje.grid(alpha=0.25)
    eje.legend()
    eje.text(
        0.99,
        0.97,
        rf"Intervalo $({alpha:g},{beta:g})$",
        transform=eje.transAxes,
        ha="right",
        va="top",
        fontsize=9,
    )
    _guardar_figura(figura, ruta)


def guardar_permutaciones(ruta: Path, permutaciones: Mapping[str, object]) -> None:
    """Muestra los índices inducidos por las dos órbitas auxiliares."""

    figura, ejes = plt.subplots(2, 1, figsize=(8.0, 6.2), constrained_layout=True)
    for eje, clave, titulo in (
        (ejes[0], "sembrada", "Auxiliar sembrada: usada en logístico"),
        (ejes[1], "fija", "Auxiliar fija: usada en tienda y R30"),
    ):
        indices = np.asarray(permutaciones[clave]["indices"])
        eje.scatter(np.arange(indices.size), indices, s=4, alpha=0.65)
        eje.set(title=titulo, xlabel="Posición j", ylabel=r"Índice $\pi(j)$")
        eje.set_xlim(0, indices.size - 1)
        eje.set_ylim(0, indices.size - 1)
        eje.grid(alpha=0.2)
    _guardar_figura(figura, ruta)


def _escribir_csv(ruta: Path, muestras: Mapping[str, Mapping[str, object]]) -> None:
    campos = (
        "muestra",
        "n",
        "metodo_reordenamiento",
        "fingerprint_original",
        "fingerprint_permutacion",
        "fingerprint_reordenada",
        "alpha",
        "beta",
        "rho1_original",
        "rho1_reordenada",
        "max_abs_acf_original",
        "max_abs_acf_reordenada",
        "mae_abs_acf_original",
        "mae_abs_acf_reordenada",
        "brechas_original",
        "brechas_reordenada",
        "cola_original",
        "cola_reordenada",
        "dmax_brechas_original",
        "dmax_brechas_reordenada",
        "mae_brechas_original",
        "mae_brechas_reordenada",
    )
    with ruta.open("w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos, lineterminator="\n")
        escritor.writeheader()
        for nombre, datos in muestras.items():
            acf_o = datos["acf_original"]
            acf_r = datos["acf_reordenada"]
            brechas_o = datos["brechas_original"]
            brechas_r = datos["brechas_reordenada"]
            escritor.writerow(
                {
                    "muestra": nombre,
                    "n": len(datos["original"]),
                    "metodo_reordenamiento": datos["metodo"],
                    "fingerprint_original": datos["fingerprint_original"]["sha256"],
                    "fingerprint_permutacion": datos["fingerprint_permutacion"]["sha256"],
                    "fingerprint_reordenada": datos["fingerprint_reordenada"]["sha256"],
                    "alpha": brechas_o["alpha"],
                    "beta": brechas_o["beta"],
                    "rho1_original": acf_o["abs_rho_1"],
                    "rho1_reordenada": acf_r["abs_rho_1"],
                    "max_abs_acf_original": acf_o["max_abs_acf"],
                    "max_abs_acf_reordenada": acf_r["max_abs_acf"],
                    "mae_abs_acf_original": acf_o["mae_abs_acf"],
                    "mae_abs_acf_reordenada": acf_r["mae_abs_acf"],
                    "brechas_original": brechas_o["brechas_completas"],
                    "brechas_reordenada": brechas_r["brechas_completas"],
                    "cola_original": brechas_o["cola_censurada"],
                    "cola_reordenada": brechas_r["cola_censurada"],
                    "dmax_brechas_original": brechas_o["maxima_discrepancia_cdf"],
                    "dmax_brechas_reordenada": brechas_r["maxima_discrepancia_cdf"],
                    "mae_brechas_original": brechas_o["mae_cdf"],
                    "mae_brechas_reordenada": brechas_r["mae_cdf"],
                }
            )


def _resumen_jsonable(experimentos: Mapping[str, object]) -> Dict[str, object]:
    resumen_muestras = {}
    for nombre, datos in experimentos["muestras"].items():
        resumen_muestras[nombre] = {
            clave: valor
            for clave, valor in datos.items()
            if clave not in {"original", "reordenada", "indices"}
        }
    return {
        "parametros": experimentos["parametros"],
        "permutaciones": experimentos["resumen_permutaciones"],
        "muestras": resumen_muestras,
    }


def regenerar_reordenamiento(directorio: Path) -> Dict[str, object]:
    """Regenera figuras, CSV y el resumen científico del bloque 12."""

    directorio = Path(directorio)
    directorio.mkdir(parents=True, exist_ok=True)
    experimentos = construir_experimentos_reordenamiento()
    muestras = experimentos["muestras"]
    for nombre, datos in muestras.items():
        etiqueta = ETIQUETAS_MUESTRAS[nombre]
        guardar_acf_antes_despues(
            directorio / f"acf_antes_despues_{nombre}.png",
            datos["original"],
            datos["reordenada"],
            etiqueta,
        )
        alpha, beta = datos["intervalo_brechas"]
        referencia = directorio / f"brechas_antes_despues_{nombre}.png"
        guardar_brechas_antes_despues(
            referencia,
            datos["original"],
            datos["reordenada"],
            alpha,
            beta,
            etiqueta,
        )
        shutil.copyfile(
            referencia, directorio / ARCHIVOS_TESIS_REORDENAMIENTO[nombre]
        )
    guardar_permutaciones(
        directorio / "permutacion_indices.png", experimentos["permutaciones"]
    )
    _escribir_csv(directorio / "resumen_reordenamiento.csv", muestras)

    resumen = _resumen_jsonable(experimentos)
    nombres_png = tuple(ARCHIVOS_TESIS_REORDENAMIENTO.values()) + tuple(
        nombre
        for nombre in ARCHIVOS_REFERENCIA_REORDENAMIENTO
        if nombre.endswith(".png")
    )
    resumen["figuras"] = {
        nombre: _sha256_archivo(directorio / nombre) for nombre in nombres_png
    }
    resumen["archivos"] = list(nombres_png) + ["resumen_reordenamiento.csv"]
    return resumen


def copiar_referencias_reordenamiento(origen: Path, destino: Path) -> None:
    """Copia las referencias auxiliares solo cuando se solicita explícitamente."""

    origen = Path(origen)
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    for nombre in ARCHIVOS_REFERENCIA_REORDENAMIENTO:
        shutil.copyfile(origen / nombre, destino / nombre)
