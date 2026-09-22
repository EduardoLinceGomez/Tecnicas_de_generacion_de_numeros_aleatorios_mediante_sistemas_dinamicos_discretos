import json
import subprocess
import sys
import unittest


class CliReproducirTesisTest(unittest.TestCase):
    def test_plan_all_no_duplica_tareas_y_no_promueve(self) -> None:
        proceso = subprocess.run(
            [sys.executable, "scripts/reproducir_tesis.py", "--all", "--plan"],
            check=True,
            capture_output=True,
            text=True,
        )
        plan = json.loads(proceso.stdout)
        nombres = [tarea["nombre"] for tarea in plan["tareas"]]
        self.assertEqual(len(nombres), len(set(nombres)))
        self.assertIn("coleccionista", nombres)
        self.assertIn("bifurcaciones", nombres)
        self.assertIn("manifest_figuras", nombres)
        self.assertNotIn("--reference-dir", proceso.stdout)

    def test_requiere_un_modo(self) -> None:
        proceso = subprocess.run(
            [sys.executable, "scripts/reproducir_tesis.py", "--plan"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(proceso.returncode, 0)
        self.assertIn("required", proceso.stderr)


if __name__ == "__main__":
    unittest.main()
