#!/usr/bin/env python3
"""Regenera las figuras TeX estáticas de la primera revisión manual MCF."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


REPO_ROOT = Path(__file__).resolve().parents[1]
FUENTES = REPO_ROOT / "figuras_tesis" / "fuentes" / "revision_mcf"
FIGURAS = {
    "SDD_estatico": "conceptuales/sistema_dinamico.pdf",
    "inestable": "conceptuales/punto_fijo_repulsor.pdf",
    "estable": "conceptuales/punto_fijo_atractor.pdf",
}


def sha256(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def regenerar(output_dir: Path) -> dict[str, object]:
    """Compila las fuentes en un temporal y devuelve rutas y SHA-256."""

    output_dir = Path(output_dir)
    hashes: dict[str, str] = {}
    entorno = dict(os.environ)
    entorno.update({"SOURCE_DATE_EPOCH": "0", "FORCE_SOURCE_DATE": "1"})
    with tempfile.TemporaryDirectory(prefix="revision-mcf-") as temporal_nombre:
        temporal = Path(temporal_nombre)
        for nombre, destino_relativo in FIGURAS.items():
            fuente = FUENTES / f"{nombre}.tex"
            shutil.copy2(fuente, temporal / fuente.name)
            subprocess.run(
                [
                    "latexmk",
                    "-pdf",
                    "-interaction=nonstopmode",
                    "-file-line-error",
                    "-halt-on-error",
                    fuente.name,
                ],
                cwd=temporal,
                env=entorno,
                check=True,
                stdout=subprocess.DEVNULL,
            )
            destino = output_dir / destino_relativo
            destino.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(temporal / f"{nombre}.pdf", destino)
            hashes[destino_relativo] = sha256(destino)
    return {"archivos": list(FIGURAS.values()), "sha256": hashes}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir", type=Path, default=Path("outputs/revision_mcf")
    )
    parser.add_argument("--reference-dir", type=Path)
    argumentos = parser.parse_args()
    resumen = regenerar(argumentos.output_dir)
    if argumentos.reference_dir is not None:
        for nombre in resumen["archivos"]:
            fuente = argumentos.output_dir / nombre
            destino = argumentos.reference_dir / nombre
            destino.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(fuente, destino)
        resumen["reference_dir"] = str(argumentos.reference_dir.resolve())
    print(json.dumps(resumen, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
