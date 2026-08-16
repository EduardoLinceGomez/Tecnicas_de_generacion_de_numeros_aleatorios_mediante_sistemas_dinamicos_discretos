import csv
from pathlib import Path

import pytest

from tesis_generacion.visualizacion.manifest_figuras import (
    COLUMNAS_REQUERIDAS,
    figuras_usadas_por_latex,
    verificar_manifest,
)


def test_manifest_canonico_es_valido() -> None:
    resultado = verificar_manifest(Path("figuras_tesis/manifest_figuras.csv"))
    assert resultado["entradas"] == 64
    assert resultado["errores"] == []


def test_manifest_no_tiene_ids_rutas_o_labels_duplicados() -> None:
    with Path("figuras_tesis/manifest_figuras.csv").open(
        newline="", encoding="utf-8"
    ) as archivo:
        filas = list(csv.DictReader(archivo))
    for campo in ("id", "archivo_tesis", "archivo_canonico"):
        valores = [fila[campo] for fila in filas]
        assert len(valores) == len(set(valores))
    labels = [fila["label_latex"] for fila in filas if fila["label_latex"]]
    assert len(labels) == len(set(labels))


def test_repo_reproducible_declara_generador_y_comando() -> None:
    with Path("figuras_tesis/manifest_figuras.csv").open(
        newline="", encoding="utf-8"
    ) as archivo:
        filas = list(csv.DictReader(archivo))
    reproducibles = [f for f in filas if f["procedencia"] == "repo_reproducible"]
    assert reproducibles
    assert all(f["generador"] and f["comando"] for f in reproducibles)


def test_figuras_propias_documentan_autoria_sin_fingir_generador() -> None:
    with Path("figuras_tesis/manifest_figuras.csv").open(
        newline="", encoding="utf-8"
    ) as archivo:
        filas = list(csv.DictReader(archivo))
    propias = [f for f in filas if f["procedencia"] == "propia_documentada"]
    assert len(propias) == 12
    assert all("Elaboración propia" in f["notas"] for f in propias)
    assert all(not f["generador"] and not f["comando"] for f in propias)


def test_extractor_rechaza_multimedia(tmp_path: Path) -> None:
    (tmp_path / "capitulos").mkdir()
    (tmp_path / "estilos").mkdir()
    (tmp_path / "Main.tex").write_text(
        r"\animategraphics{1}{frame_}{0}{2}", encoding="utf-8"
    )
    with pytest.raises(ValueError, match="animategraphics"):
        figuras_usadas_por_latex(tmp_path)


def test_columnas_del_manifest_son_contractuales() -> None:
    assert COLUMNAS_REQUERIDAS[0:4] == (
        "id",
        "archivo_tesis",
        "archivo_canonico",
        "label_latex",
    )
