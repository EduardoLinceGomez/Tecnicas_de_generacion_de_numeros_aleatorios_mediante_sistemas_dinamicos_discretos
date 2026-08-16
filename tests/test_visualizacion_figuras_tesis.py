from pathlib import Path

import numpy as np
from PIL import Image

from tesis_generacion.visualizacion.figuras_tesis import (
    ARCHIVOS_GENERADOS,
    CELDAS_R30_PEDAGOGICO,
    INSTANTES_R30_PEDAGOGICO,
    evolucion_regla_elemental,
    matriz_regla30_pedagogica,
    regenerar_figuras_tesis,
    tabla_regla30,
)


def test_tabla_regla30_derivada_de_la_implementacion() -> None:
    assert tabla_regla30() == (
        ((1, 1, 1), 0),
        ((1, 1, 0), 0),
        ((1, 0, 1), 0),
        ((1, 0, 0), 1),
        ((0, 1, 1), 1),
        ((0, 1, 0), 1),
        ((0, 0, 1), 1),
        ((0, 0, 0), 0),
    )


def test_regla184_mueve_un_vehiculo_a_un_hueco() -> None:
    inicial = np.asarray([1, 0, 0, 0], dtype=np.uint8)
    matriz = evolucion_regla_elemental(184, inicial, 2)
    assert matriz[1].tolist() == [0, 1, 0, 0]


def test_matriz_pedagogica_tiene_parametros_documentados() -> None:
    matriz = matriz_regla30_pedagogica()
    assert matriz.shape == (INSTANTES_R30_PEDAGOGICO, CELDAS_R30_PEDAGOGICO)
    assert int(matriz[0].sum()) == 1
    assert matriz[0, CELDAS_R30_PEDAGOGICO // 2] == 1


def test_regeneracion_produce_todas_las_figuras(tmp_path: Path) -> None:
    resumen = regenerar_figuras_tesis(tmp_path)
    assert tuple(resumen["archivos"]) == ARCHIVOS_GENERADOS
    assert len(resumen["sha256"]) == len(ARCHIVOS_GENERADOS)
    assert all((tmp_path / nombre).is_file() for nombre in ARCHIVOS_GENERADOS)


def test_png_tienen_resolucion_suficiente(tmp_path: Path) -> None:
    regenerar_figuras_tesis(tmp_path)
    for nombre in ARCHIVOS_GENERADOS:
        if nombre.endswith(".png"):
            with Image.open(tmp_path / nombre) as imagen:
                assert imagen.width >= 600
                assert imagen.height >= 400
