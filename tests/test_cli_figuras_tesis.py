import json
from pathlib import Path
import subprocess
import sys


def test_cli_regenera_figuras_y_emite_json(tmp_path: Path) -> None:
    salida = tmp_path / "salida"
    proceso = subprocess.run(
        [
            sys.executable,
            "scripts/regenerar_figuras_conceptuales.py",
            "--output-dir",
            str(salida),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proceso.returncode == 0, proceso.stderr
    resumen = json.loads(proceso.stdout)
    assert len(resumen["archivos"]) == 28
    assert (salida / "conceptuales/sistema_dinamico.pdf").is_file()


def test_cli_verifica_manifest() -> None:
    proceso = subprocess.run(
        [sys.executable, "scripts/verificar_figuras_tesis.py"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proceso.returncode == 0, proceso.stdout + proceso.stderr
    resumen = json.loads(proceso.stdout)
    assert resumen["manifest"]["entradas"] == 65


def test_cli_tikz_regenera_pcc_y_pg_exactas(tmp_path: Path) -> None:
    salida = tmp_path / "tikz"
    proceso = subprocess.run(
        [
            sys.executable,
            "scripts/regenerar_figuras_tikz.py",
            "--output-dir",
            str(salida),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proceso.returncode == 0, proceso.stdout + proceso.stderr
    resumen = json.loads(proceso.stdout)
    assert resumen["sha256"] == {
        "conceptuales/coleccionista_bloques.png": (
            "63ba61dff52ce55107300fdc74b0c4e5c29908f7f207f839b1ef12ba63292e94"
        ),
        "conceptuales/prueba_brechas.png": (
            "a4ce0160a452334131a0e5102d98f74e3aaf6b29300a8888dfdf766eb40f3dfa"
        ),
    }


def test_cli_revision_mcf_regenera_tres_pdf_estaticos(tmp_path: Path) -> None:
    primera = tmp_path / "primera"
    segunda = tmp_path / "segunda"
    hashes = []
    for salida in (primera, segunda):
        proceso = subprocess.run(
            [
                sys.executable,
                "scripts/regenerar_figuras_revision_mcf.py",
                "--output-dir",
                str(salida),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        assert proceso.returncode == 0, proceso.stdout + proceso.stderr
        resumen = json.loads(proceso.stdout)
        assert resumen["archivos"] == [
            "conceptuales/sistema_dinamico.pdf",
            "conceptuales/punto_fijo_repulsor.pdf",
            "conceptuales/punto_fijo_atractor.pdf",
        ]
        assert all((salida / nombre).is_file() for nombre in resumen["archivos"])
        hashes.append(resumen["sha256"])
    assert hashes[0] == hashes[1]
    fuente = Path("figuras_tesis/fuentes/revision_mcf/SDD_estatico.tex").read_text(
        encoding="utf-8"
    )
    assert "\\animategraphics" not in fuente
    assert all(f"\\panel{{{n}}}" in fuente for n in (0, 1, 3, 4))
