from pathlib import Path

import numpy as np
from PIL import Image

from tesis_generacion.visualizacion.bifurcaciones import (
    ConfiguracionBifurcacion,
    LOGISTICO,
    TIENDA,
    datos_bifurcacion,
    regenerar_bifurcaciones,
)


def test_datos_bifurcacion_respetan_malla_y_rango() -> None:
    configuracion = ConfiguracionBifurcacion(
        numero_parametros=41,
        burn_in=20,
        iteraciones_graficadas=7,
        dpi=96,
    )
    for especificacion in (LOGISTICO, TIENDA):
        parametros, estados = datos_bifurcacion(especificacion, configuracion)
        assert parametros.shape == estados.shape == (41 * 7,)
        assert np.isclose(parametros.min(), especificacion.parametro_minimo)
        assert np.isclose(parametros.max(), especificacion.parametro_maximo)
        assert np.all((0.0 <= estados) & (estados <= 1.0))


def test_regeneracion_hibrida_documenta_parametros(tmp_path: Path) -> None:
    configuracion = ConfiguracionBifurcacion(
        numero_parametros=64,
        burn_in=20,
        iteraciones_graficadas=8,
        figura_ancho_pulgadas=3.0,
        figura_alto_pulgadas=2.1,
        dpi=96,
    )
    reporte = regenerar_bifurcaciones(
        tmp_path,
        configuracion,
        incluir_svg=True,
        usar_latex=False,
    )

    assert reporte["configuracion"]["numero_parametros"] == 64
    assert reporte["mapas"]["logistico"]["puntos_graficados"] == 512
    assert set(reporte["archivos"]) == {
        "logistico_bifurcacion.pdf",
        "logistico_bifurcacion.svg",
        "logistico_bifurcacion.png",
        "tienda_bifurcacion.pdf",
        "tienda_bifurcacion.svg",
        "tienda_bifurcacion.png",
    }
    assert all(datos["bytes"] > 0 for datos in reporte["archivos"].values())
    assert "<image" in (tmp_path / "logistico_bifurcacion.svg").read_text(
        encoding="utf-8"
    )
    with Image.open(tmp_path / "logistico_bifurcacion.png") as imagen:
        assert imagen.size == (288, 201)

    segunda = tmp_path / "segunda"
    regenerar_bifurcaciones(
        segunda,
        configuracion,
        incluir_svg=True,
        usar_latex=False,
    )
    for nombre in reporte["archivos"]:
        assert (tmp_path / nombre).read_bytes() == (segunda / nombre).read_bytes()
