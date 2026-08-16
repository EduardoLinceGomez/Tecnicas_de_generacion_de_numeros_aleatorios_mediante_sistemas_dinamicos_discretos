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
    assert resumen["manifest"]["entradas"] == 64


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
