"""Diagramas de bifurcación híbridos para impresión en la tesis.

Los ejes, las etiquetas y la tipografía se conservan como elementos
vectoriales. La nube de puntos se rasteriza al guardar para evitar PDF y SVG
desproporcionadamente grandes.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import platform
from pathlib import Path
import shutil
from typing import Callable, Dict, Optional, Tuple

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np


FIGURA_ANCHO_PULGADAS = 12.0 / 2.54
FIGURA_ALTO_PULGADAS = FIGURA_ANCHO_PULGADAS * 283.0 / 406.0


@dataclass(frozen=True)
class ConfiguracionBifurcacion:
    """Parámetros numéricos y gráficos compartidos por ambas figuras."""

    numero_parametros: int = 6000
    burn_in: int = 900
    iteraciones_graficadas: int = 100
    condicion_inicial: float = 0.02024
    alpha: float = 0.45
    tamano_punto_pt2: float = 0.20
    figura_ancho_pulgadas: float = FIGURA_ANCHO_PULGADAS
    figura_alto_pulgadas: float = FIGURA_ALTO_PULGADAS
    dpi: int = 600

    def validar(self) -> None:
        if self.numero_parametros < 2:
            raise ValueError("numero_parametros debe ser al menos 2")
        if self.burn_in < 0:
            raise ValueError("burn_in no puede ser negativo")
        if self.iteraciones_graficadas < 1:
            raise ValueError("iteraciones_graficadas debe ser positiva")
        if not 0.0 < self.condicion_inicial < 1.0:
            raise ValueError("condicion_inicial debe pertenecer a (0, 1)")
        if not 0.0 < self.alpha <= 1.0:
            raise ValueError("alpha debe pertenecer a (0, 1]")
        if self.tamano_punto_pt2 <= 0.0:
            raise ValueError("tamano_punto_pt2 debe ser positivo")
        if self.figura_ancho_pulgadas <= 0.0 or self.figura_alto_pulgadas <= 0.0:
            raise ValueError("las dimensiones de la figura deben ser positivas")
        if self.dpi < 72:
            raise ValueError("dpi debe ser al menos 72")


@dataclass(frozen=True)
class EspecificacionMapa:
    """Rango, dinámica y rotulación de un diagrama."""

    nombre: str
    parametro_minimo: float
    parametro_maximo: float
    etiqueta_x: str
    etiqueta_y: Optional[str]
    titulo_metadatos: str


LOGISTICO = EspecificacionMapa(
    nombre="logistico",
    parametro_minimo=2.8,
    parametro_maximo=4.0,
    etiqueta_x=r"$r$",
    etiqueta_y=r"$x^*$",
    titulo_metadatos="Diagrama de bifurcación del mapeo logístico",
)

TIENDA = EspecificacionMapa(
    nombre="tienda",
    parametro_minimo=1.0,
    parametro_maximo=2.0,
    etiqueta_x=r"$\mu$",
    etiqueta_y=None,
    titulo_metadatos="Diagrama de bifurcación del mapeo tienda",
)


def _paso_logistico(parametros: np.ndarray, valores: np.ndarray) -> np.ndarray:
    return parametros * valores * (1.0 - valores)


def _paso_tienda(parametros: np.ndarray, valores: np.ndarray) -> np.ndarray:
    return np.where(
        valores <= 0.5,
        parametros * valores,
        parametros * (1.0 - valores),
    )


PASOS: Dict[str, Callable[[np.ndarray, np.ndarray], np.ndarray]] = {
    LOGISTICO.nombre: _paso_logistico,
    TIENDA.nombre: _paso_tienda,
}


def datos_bifurcacion(
    especificacion: EspecificacionMapa,
    configuracion: ConfiguracionBifurcacion,
) -> Tuple[np.ndarray, np.ndarray]:
    """Calcula los estados asintóticos para la malla paramétrica indicada."""

    configuracion.validar()
    parametros = np.linspace(
        especificacion.parametro_minimo,
        especificacion.parametro_maximo,
        configuracion.numero_parametros,
        endpoint=True,
        dtype=np.float64,
    )
    valores = np.full(
        parametros.shape,
        configuracion.condicion_inicial,
        dtype=np.float64,
    )
    paso = PASOS[especificacion.nombre]
    for _ in range(configuracion.burn_in):
        valores = paso(parametros, valores)

    estados = np.empty(
        (configuracion.iteraciones_graficadas, configuracion.numero_parametros),
        dtype=np.float64,
    )
    for indice in range(configuracion.iteraciones_graficadas):
        valores = paso(parametros, valores)
        estados[indice] = valores

    return np.tile(parametros, configuracion.iteraciones_graficadas), estados.ravel()


def _contexto_latex() -> Dict[str, object]:
    if shutil.which("latex") is None or shutil.which("dvipng") is None:
        raise RuntimeError(
            "La exportación requiere latex y dvipng para renderizar las etiquetas."
        )
    return {
        "text.usetex": True,
        "font.family": "serif",
        "font.serif": ["Computer Modern Roman"],
        "text.latex.preamble": r"\usepackage[T1]{fontenc}",
        "axes.unicode_minus": False,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "path",
        "svg.hashsalt": "tesis-generacion-bifurcaciones",
    }


def construir_figura(
    especificacion: EspecificacionMapa,
    configuracion: ConfiguracionBifurcacion,
    *,
    usar_latex: bool = True,
) -> plt.Figure:
    """Construye una figura manteniendo la geometría de la imagen histórica."""

    parametros, estados = datos_bifurcacion(especificacion, configuracion)
    contexto = _contexto_latex() if usar_latex else {"text.usetex": False}
    with matplotlib.rc_context(contexto):
        figura, eje = plt.subplots(
            figsize=(
                configuracion.figura_ancho_pulgadas,
                configuracion.figura_alto_pulgadas,
            )
        )
        figura.patch.set_facecolor("white")
        figura.subplots_adjust(left=0.16, right=0.975, bottom=0.20, top=0.975)
        eje.set_facecolor("white")
        eje.scatter(
            parametros,
            estados,
            s=configuracion.tamano_punto_pt2,
            marker=".",
            color="#111111",
            alpha=configuracion.alpha,
            linewidths=0.0,
            edgecolors="none",
            rasterized=True,
            zorder=1,
        )
        eje.set_xlim(especificacion.parametro_minimo, especificacion.parametro_maximo)
        eje.set_ylim(0.0, 1.0)
        eje.set_xticks(
            np.linspace(
                especificacion.parametro_minimo,
                especificacion.parametro_maximo,
                7 if especificacion.nombre == "logistico" else 6,
            )
        )
        eje.set_yticks(np.linspace(0.0, 1.0, 6))
        eje.xaxis.set_major_formatter(FormatStrFormatter("%.1f"))
        eje.yaxis.set_major_formatter(FormatStrFormatter("%.1f"))
        eje.set_xlabel(especificacion.etiqueta_x, fontsize=22, labelpad=5)
        if especificacion.etiqueta_y is not None:
            eje.set_ylabel(especificacion.etiqueta_y, fontsize=22, labelpad=4)
        else:
            eje.tick_params(axis="y", labelleft=False)
        eje.tick_params(
            axis="both",
            which="major",
            direction="out",
            labelsize=9.0,
            length=3.5,
            width=0.7,
            colors="black",
        )
        eje.grid(
            True,
            which="major",
            color="black",
            linestyle=":",
            linewidth=0.55,
            alpha=0.85,
            zorder=3,
        )
        for borde in eje.spines.values():
            borde.set_color("black")
            borde.set_linewidth(0.7)
    return figura


def _guardar_formatos(
    figura: plt.Figure,
    base: Path,
    especificacion: EspecificacionMapa,
    configuracion: ConfiguracionBifurcacion,
    *,
    incluir_svg: bool,
    usar_latex: bool,
) -> Tuple[Path, ...]:
    base.parent.mkdir(parents=True, exist_ok=True)
    rutas = []
    contexto = _contexto_latex() if usar_latex else {
        "text.usetex": False,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "path",
        "svg.hashsalt": "tesis-generacion-bifurcaciones",
    }
    with matplotlib.rc_context(contexto):
        ruta_pdf = base.with_suffix(".pdf")
        figura.savefig(
            ruta_pdf,
            dpi=configuracion.dpi,
            facecolor="white",
            metadata={
                "Title": especificacion.titulo_metadatos,
                "Author": "Elaboración propia",
                "Creator": "scripts/regenerar_bifurcaciones.py",
                "CreationDate": None,
                "ModDate": None,
            },
        )
        rutas.append(ruta_pdf)

        if incluir_svg:
            ruta_svg = base.with_suffix(".svg")
            figura.savefig(
                ruta_svg,
                dpi=configuracion.dpi,
                facecolor="white",
                metadata={
                    "Title": especificacion.titulo_metadatos,
                    "Creator": "scripts/regenerar_bifurcaciones.py",
                    "Description": (
                        "Ejes y texto vectoriales; nube de puntos rasterizada."
                    ),
                    "Date": None,
                },
            )
            rutas.append(ruta_svg)

        ruta_png = base.with_suffix(".png")
        figura.savefig(
            ruta_png,
            dpi=configuracion.dpi,
            facecolor="white",
            metadata={
                "Title": especificacion.titulo_metadatos,
                "Software": "scripts/regenerar_bifurcaciones.py",
            },
        )
        rutas.append(ruta_png)
    plt.close(figura)
    return tuple(rutas)


def _sha256(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def regenerar_bifurcaciones(
    output_dir: Path,
    configuracion: ConfiguracionBifurcacion = ConfiguracionBifurcacion(),
    *,
    incluir_svg: bool = True,
    usar_latex: bool = True,
) -> Dict[str, object]:
    """Genera ambas figuras y devuelve un reporte serializable."""

    configuracion.validar()
    output_dir.mkdir(parents=True, exist_ok=True)
    archivos = []
    for especificacion in (LOGISTICO, TIENDA):
        figura = construir_figura(
            especificacion,
            configuracion,
            usar_latex=usar_latex,
        )
        archivos.extend(
            _guardar_formatos(
                figura,
                output_dir / f"{especificacion.nombre}_bifurcacion",
                especificacion,
                configuracion,
                incluir_svg=incluir_svg,
                usar_latex=usar_latex,
            )
        )

    return {
        "output_dir": str(output_dir.resolve()),
        "configuracion": asdict(configuracion),
        "mapas": {
            especificacion.nombre: {
                "rango_parametro": [
                    especificacion.parametro_minimo,
                    especificacion.parametro_maximo,
                ],
                "etiqueta_x": especificacion.etiqueta_x,
                "etiqueta_y": especificacion.etiqueta_y,
                "puntos_graficados": (
                    configuracion.numero_parametros
                    * configuracion.iteraciones_graficadas
                ),
            }
            for especificacion in (LOGISTICO, TIENDA)
        },
        "renderizado": {
            "latex": usar_latex,
            "nube_puntos": f"rasterizada a {configuracion.dpi} dpi",
            "texto_y_ejes": "vectoriales en PDF y SVG",
            "formatos": ["pdf", *( ["svg"] if incluir_svg else []), "png"],
        },
        "entorno": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "matplotlib": matplotlib.__version__,
            "backend": str(matplotlib.get_backend()),
        },
        "archivos": {
            ruta.name: {
                "bytes": ruta.stat().st_size,
                "sha256": _sha256(ruta),
            }
            for ruta in archivos
        },
    }
