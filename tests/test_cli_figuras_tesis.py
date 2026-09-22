import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class CliFigurasTesisTest(unittest.TestCase):
    def test_cli_regenera_figuras_y_emite_json(self) -> None:
        with tempfile.TemporaryDirectory() as temporal:
            salida = Path(temporal) / "salida"
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
            self.assertEqual(proceso.returncode, 0, proceso.stderr)
            resumen = json.loads(proceso.stdout)
            self.assertEqual(len(resumen["archivos"]), 28)
            self.assertTrue((salida / "conceptuales/sistema_dinamico.pdf").is_file())

    def test_cli_verifica_manifest(self) -> None:
        proceso = subprocess.run(
            [sys.executable, "scripts/verificar_figuras_tesis.py"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proceso.returncode, 0, proceso.stdout + proceso.stderr)
        resumen = json.loads(proceso.stdout)
        self.assertEqual(resumen["manifest"]["entradas"], 65)

    @unittest.skipUnless(
        shutil.which("latexmk") and shutil.which("pdftoppm"),
        "las figuras TikZ requieren latexmk y pdftoppm",
    )
    def test_cli_tikz_regenera_pcc_y_pg_exactas(self) -> None:
        with tempfile.TemporaryDirectory() as temporal:
            salida = Path(temporal) / "tikz"
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
            self.assertEqual(proceso.returncode, 0, proceso.stdout + proceso.stderr)
            resumen = json.loads(proceso.stdout)
            self.assertEqual(
                resumen["sha256"],
                {
                    "conceptuales/coleccionista_bloques.png": (
                        "63ba61dff52ce55107300fdc74b0c4e5c29908f7f207f839b1ef12ba63292e94"
                    ),
                    "conceptuales/prueba_brechas.png": (
                        "a4ce0160a452334131a0e5102d98f74e3aaf6b29300a8888dfdf766eb40f3dfa"
                    ),
                },
            )

    @unittest.skipUnless(
        shutil.which("latexmk"),
        "las figuras TeX requieren latexmk",
    )
    def test_cli_revision_mcf_regenera_tres_pdf_estaticos(self) -> None:
        with tempfile.TemporaryDirectory() as temporal:
            raiz = Path(temporal)
            hashes = []
            for salida in (raiz / "primera", raiz / "segunda"):
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
                self.assertEqual(
                    proceso.returncode, 0, proceso.stdout + proceso.stderr
                )
                resumen = json.loads(proceso.stdout)
                self.assertEqual(
                    resumen["archivos"],
                    [
                        "conceptuales/sistema_dinamico.pdf",
                        "conceptuales/punto_fijo_repulsor.pdf",
                        "conceptuales/punto_fijo_atractor.pdf",
                    ],
                )
                self.assertTrue(
                    all((salida / nombre).is_file() for nombre in resumen["archivos"])
                )
                hashes.append(resumen["sha256"])
            self.assertEqual(hashes[0], hashes[1])
            fuente = Path(
                "figuras_tesis/fuentes/revision_mcf/SDD_estatico.tex"
            ).read_text(encoding="utf-8")
            self.assertNotIn("\\animategraphics", fuente)
            self.assertTrue(all(f"\\panel{{{n}}}" in fuente for n in (0, 1, 3, 4)))


if __name__ == "__main__":
    unittest.main()
