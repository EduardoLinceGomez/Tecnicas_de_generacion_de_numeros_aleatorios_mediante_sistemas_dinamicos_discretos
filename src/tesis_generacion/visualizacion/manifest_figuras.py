"""Lectura y verificación del manifiesto canónico de figuras de la tesis."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path
import re
from typing import Dict, Iterable, List, Mapping, Sequence, Set


COLUMNAS_REQUERIDAS = (
    "id",
    "archivo_tesis",
    "archivo_canonico",
    "label_latex",
    "categoria",
    "procedencia",
    "generador",
    "comando",
    "parametros",
    "referencia",
    "sha256",
    "notas",
)
PROCEDENCIAS_VALIDAS = {
    "repo_reproducible",
    "propia_documentada",
    "externa_citada",
}


def sha256(ruta: Path) -> str:
    return hashlib.sha256(Path(ruta).read_bytes()).hexdigest()


def leer_manifest(ruta: Path) -> List[Dict[str, str]]:
    with Path(ruta).open(newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        if tuple(lector.fieldnames or ()) != COLUMNAS_REQUERIDAS:
            raise ValueError("columnas inesperadas en manifest_figuras.csv")
        return [dict(fila) for fila in lector]


def _duplicados(valores: Iterable[str]) -> Set[str]:
    vistos: Set[str] = set()
    duplicados: Set[str] = set()
    for valor in valores:
        if not valor:
            continue
        if valor in vistos:
            duplicados.add(valor)
        vistos.add(valor)
    return duplicados


def verificar_manifest(ruta: Path) -> Dict[str, object]:
    ruta = Path(ruta)
    raiz = ruta.parent
    filas = leer_manifest(ruta)
    errores: List[str] = []
    for campo in ("id", "archivo_tesis", "archivo_canonico", "label_latex"):
        duplicados = _duplicados(fila[campo] for fila in filas)
        if duplicados:
            errores.append(f"{campo} duplicado: {sorted(duplicados)}")
    for fila in filas:
        procedencia = fila["procedencia"]
        if procedencia not in PROCEDENCIAS_VALIDAS:
            errores.append(f"procedencia inválida en {fila['id']}: {procedencia}")
        archivo = raiz / fila["archivo_canonico"]
        if not archivo.is_file():
            errores.append(f"archivo canónico inexistente: {archivo}")
        elif fila["sha256"] != sha256(archivo):
            errores.append(f"SHA-256 diferente: {fila['id']}")
        if procedencia == "repo_reproducible" and not (
            fila["generador"].strip() and fila["comando"].strip()
        ):
            errores.append(f"generador/comando vacío: {fila['id']}")
        if procedencia == "propia_documentada" and "Elaboración propia" not in fila[
            "notas"
        ]:
            errores.append(f"autoría propia no documentada: {fila['id']}")
        if procedencia == "externa_citada" and not fila["referencia"].strip():
            errores.append(f"referencia externa vacía: {fila['id']}")
    return {
        "entradas": len(filas),
        "errores": errores,
        "procedencias": {
            nombre: sum(fila["procedencia"] == nombre for fila in filas)
            for nombre in sorted(PROCEDENCIAS_VALIDAS)
        },
    }


def _sin_comentarios(texto: str) -> str:
    lineas = []
    for linea in texto.splitlines():
        corte = None
        for posicion, caracter in enumerate(linea):
            if caracter == "%" and (posicion == 0 or linea[posicion - 1] != "\\"):
                corte = posicion
                break
        lineas.append(linea if corte is None else linea[:corte])
    return "\n".join(lineas)


def figuras_usadas_por_latex(tesis_root: Path) -> Set[str]:
    """Extrae las rutas gráficas activas de la estructura actual de la tesis."""

    tesis_root = Path(tesis_root)
    archivos_tex = [tesis_root / "Main.tex"]
    archivos_tex.extend(sorted((tesis_root / "capitulos").glob("*.tex")))
    archivos_tex.extend(sorted((tesis_root / "estilos").glob("*.sty")))
    texto = "\n".join(
        _sin_comentarios(ruta.read_text(encoding="utf-8"))
        for ruta in archivos_tex
        if ruta.is_file()
    )
    if re.search(r"\\animategraphics(?:\[[^]]*\])?", texto):
        raise ValueError("la tesis aún contiene animategraphics")
    rutas = set(
        re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", texto)
    )
    rutas.discard(r"\chapterimage")
    for nombre in re.findall(r"\\setchapterimage\{([^}]+)\}", texto):
        rutas.add(f"recursos/imagenes/{nombre}")
    for comando, carpeta in (
        ("logouni", "recursos/portada"),
        ("logofac", "recursos/portada"),
    ):
        for nombre in re.findall(rf"\\{comando}\{{([^}}]+)\}}", texto):
            rutas.add(nombre if "/" in nombre else f"{carpeta}/{nombre}")
    return {ruta.removeprefix("./") for ruta in rutas if not ruta.startswith("\\")}


def verificar_tesis(
    manifest_path: Path, tesis_root: Path
) -> Dict[str, object]:
    filas = leer_manifest(manifest_path)
    por_ruta = {fila["archivo_tesis"]: fila for fila in filas}
    usadas = figuras_usadas_por_latex(tesis_root)
    declaradas = set(por_ruta)
    errores: List[str] = []
    for ruta in sorted(usadas & declaradas):
        archivo = Path(tesis_root) / ruta
        if not archivo.is_file():
            errores.append(f"figura LaTeX inexistente: {ruta}")
        elif sha256(archivo) != por_ruta[ruta]["sha256"]:
            errores.append(f"figura de tesis difiere de la canónica: {ruta}")
    errores.extend(f"ausente del manifest: {ruta}" for ruta in sorted(usadas - declaradas))
    errores.extend(f"no utilizada por LaTeX: {ruta}" for ruta in sorted(declaradas - usadas))
    return {
        "usadas": len(usadas),
        "declaradas": len(declaradas),
        "errores": errores,
    }


def actualizar_sha(manifest_path: Path) -> None:
    """Actualiza únicamente la columna sha256 desde las copias canónicas."""

    manifest_path = Path(manifest_path)
    filas = leer_manifest(manifest_path)
    for fila in filas:
        fila["sha256"] = sha256(manifest_path.parent / fila["archivo_canonico"])
    with manifest_path.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(
            archivo, fieldnames=COLUMNAS_REQUERIDAS, lineterminator="\n"
        )
        escritor.writeheader()
        escritor.writerows(filas)
