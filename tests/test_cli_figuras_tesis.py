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
