#!/usr/bin/env python3
"""Regenera PCC y PG desde las fuentes TikZ científicamente validadas."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


REPO_ROOT = Path(__file__).resolve().parents[1]
FUENTES = REPO_ROOT / "figuras_tesis" / "fuentes"
FIGURAS = {
    "PCC": "conceptuales/coleccionista_bloques.png",
    "PG": "conceptuales/prueba_brechas.png",
}


def sha256(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def regenerar(output_dir: Path) -> dict[str, object]:
    output_dir = Path(output_dir)
    hashes = {}
    with tempfile.TemporaryDirectory(prefix="figuras-tikz-") as temporal:
        temporal = Path(temporal)
        for nombre, destino_relativo in FIGURAS.items():
            shutil.copy2(FUENTES / f"{nombre}.tex", temporal / f"{nombre}.tex")
            subprocess.run(
                [
                    "latexmk",
                    "-pdf",
                    "-interaction=nonstopmode",
                    "-file-line-error",
                    f"{nombre}.tex",
                ],
                cwd=temporal,
                check=True,
                stdout=subprocess.DEVNULL,
            )
            destino = output_dir / destino_relativo
            destino.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(
                [
                    "pdftoppm",
                    "-png",
                    "-r",
                    "200",
                    "-singlefile",
                    f"{nombre}.pdf",
                    str(destino.with_suffix("")),
                ],
                cwd=temporal,
                check=True,
                stdout=subprocess.DEVNULL,
            )
            hashes[destino_relativo] = sha256(destino)
    return {"archivos": list(FIGURAS.values()), "sha256": hashes}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir", type=Path, default=Path("outputs/figuras_tikz")
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
