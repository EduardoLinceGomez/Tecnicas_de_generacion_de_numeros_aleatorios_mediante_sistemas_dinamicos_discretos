import csv
from pathlib import Path
import tempfile
import unittest

from tesis_generacion.visualizacion.manifest_figuras import (
    COLUMNAS_REQUERIDAS,
    figuras_usadas_por_latex,
    verificar_manifest,
)


class ManifestFigurasTest(unittest.TestCase):
    def test_manifest_canonico_es_valido(self) -> None:
        resultado = verificar_manifest(Path("figuras_tesis/manifest_figuras.csv"))
        self.assertEqual(resultado["entradas"], 65)
        self.assertEqual(resultado["errores"], [])

    def test_manifest_no_tiene_ids_rutas_o_labels_duplicados(self) -> None:
        with Path("figuras_tesis/manifest_figuras.csv").open(
            newline="", encoding="utf-8"
        ) as archivo:
            filas = list(csv.DictReader(archivo))
        for campo in ("id", "archivo_tesis", "archivo_canonico"):
            valores = [fila[campo] for fila in filas]
            self.assertEqual(len(valores), len(set(valores)))
        labels = [fila["label_latex"] for fila in filas if fila["label_latex"]]
        self.assertEqual(len(labels), len(set(labels)))

    def test_repo_reproducible_declara_generador_y_comando(self) -> None:
        with Path("figuras_tesis/manifest_figuras.csv").open(
            newline="", encoding="utf-8"
        ) as archivo:
            filas = list(csv.DictReader(archivo))
        reproducibles = [
            fila for fila in filas if fila["procedencia"] == "repo_reproducible"
        ]
        self.assertTrue(reproducibles)
        self.assertTrue(
            all(fila["generador"] and fila["comando"] for fila in reproducibles)
        )

    def test_figuras_propias_documentan_autoria_sin_fingir_generador(self) -> None:
        with Path("figuras_tesis/manifest_figuras.csv").open(
            newline="", encoding="utf-8"
        ) as archivo:
            filas = list(csv.DictReader(archivo))
        propias = [
            fila for fila in filas if fila["procedencia"] == "propia_documentada"
        ]
        self.assertEqual(len(propias), 10)
        self.assertTrue(all("Elaboración propia" in fila["notas"] for fila in propias))
        self.assertTrue(
            all(not fila["generador"] and not fila["comando"] for fila in propias)
        )

    def test_extractor_rechaza_multimedia(self) -> None:
        with tempfile.TemporaryDirectory() as temporal:
            raiz = Path(temporal)
            (raiz / "capitulos").mkdir()
            (raiz / "estilos").mkdir()
            (raiz / "Main.tex").write_text(
                r"\animategraphics{1}{frame_}{0}{2}", encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "animategraphics"):
                figuras_usadas_por_latex(raiz)

    def test_columnas_del_manifest_son_contractuales(self) -> None:
        self.assertEqual(
            COLUMNAS_REQUERIDAS[0:4],
            ("id", "archivo_tesis", "archivo_canonico", "label_latex"),
        )


if __name__ == "__main__":
    unittest.main()
