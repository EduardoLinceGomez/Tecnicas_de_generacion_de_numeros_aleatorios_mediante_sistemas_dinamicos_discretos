"""Criterios visuales compartidos para las gráficas usadas en la tesis."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from matplotlib.axes import Axes
from matplotlib.figure import Figure


@dataclass(frozen=True)
class PerfilTipografico:
    """Tamaños adaptados al ancho final de una figura en el PDF."""

    titulo: float
    ejes: float
    ticks: float
    leyenda: float
    anotacion: float
    separacion_leyenda: float


# Figuras que terminan a aproximadamente media página.
PERFIL_MEDIO = PerfilTipografico(22, 19, 16, 14, 14, -0.24)
# Figuras que se insertan al 80 % del ancho del texto.
PERFIL_ANCHO = PerfilTipografico(18, 16, 13, 12, 12, -0.20)
# Los dos histogramas de la Figura 2.13 se muestran lado a lado y requieren
# tipografía ligeramente mayor por la reducción final.
PERFIL_HISTOGRAMA_DOBLE = PerfilTipografico(26, 23, 19, 17, 16, -0.25)


def estilizar_eje(eje: Axes, perfil: PerfilTipografico = PERFIL_MEDIO) -> None:
    """Normaliza título, etiquetas y ticks sin alterar datos ni escalas."""

    eje.title.set_fontsize(perfil.titulo)
    eje.xaxis.label.set_fontsize(perfil.ejes)
    eje.yaxis.label.set_fontsize(perfil.ejes)
    eje.tick_params(axis="both", which="both", labelsize=perfil.ticks)
    eje.xaxis.get_offset_text().set_fontsize(perfil.ticks)
    eje.yaxis.get_offset_text().set_fontsize(perfil.ticks)


def leyenda_externa(
    eje: Axes,
    perfil: PerfilTipografico = PERFIL_MEDIO,
    *,
    ncol: int = 2,
) -> Optional[object]:
    """Sitúa una leyenda existente debajo del eje, cerca del xlabel."""

    manejadores, etiquetas = eje.get_legend_handles_labels()
    if not manejadores:
        return None
    return eje.legend(
        manejadores,
        etiquetas,
        loc="upper center",
        bbox_to_anchor=(0.5, perfil.separacion_leyenda),
        borderaxespad=0.0,
        fontsize=perfil.leyenda,
        ncol=ncol,
        columnspacing=1.1,
        handletextpad=0.55,
        labelspacing=0.45,
    )


def guardar_figura(
    figura: Figure,
    ruta: Path,
    *,
    software: str,
    dpi: int = 200,
) -> None:
    """Guarda sin recortes y con un padding compacto y reproducible."""

    figura.savefig(
        ruta,
        dpi=dpi,
        bbox_inches="tight",
        pad_inches=0.08,
        metadata={"Software": software},
    )
