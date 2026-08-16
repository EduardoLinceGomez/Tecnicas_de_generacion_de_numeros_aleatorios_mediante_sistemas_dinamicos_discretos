# Figuras canónicas de la tesis

Esta carpeta contiene las salidas que se integran realmente en el documento.
Se distingue de `graficas_auxiliares/`, que conserva diagnósticos científicos
versionados que no necesariamente aparecen en la tesis. El commit que contiene
este archivo identifica la versión de implementación asociada.

`manifest_figuras.csv` relaciona cada archivo usado por LaTeX con su copia
canónica, procedencia, generador, parámetros, referencia y SHA-256. Los nombres
históricos del repositorio de tesis pueden mantenerse: antes de integrarlos se
copia la salida canónica a `archivo_tesis` y ambos hashes deben coincidir.

## Regeneración

| Familia | Comando | Entorno o condición |
|---|---|---|
| Conceptuales, diagramas, bifurcaciones e histogramas básicos | `python3 scripts/regenerar_figuras_conceptuales.py --output-dir outputs/figuras_tesis --reference-dir figuras_tesis` | Entorno actual; solo copia al directorio canónico las salidas todavía activas |
| PCC y PG | `python3 scripts/regenerar_figuras_tikz.py --output-dir outputs/figuras_tikz --reference-dir figuras_tesis` | TeX Live y Poppler; rasterización a 200 dpi |
| Momentos e histogramas Normal/Cauchy | `python3 scripts/regenerar_momentos.py --output-dir outputs/momentos` | Entorno baseline gráfico |
| FGM y función característica | `python3 scripts/regenerar_transformadas.py --output-dir outputs/transformadas` | Entorno baseline gráfico |
| Invariancia | `python3 scripts/regenerar_invariancia.py --output-dir outputs/invariancia` | Entorno documentado por el bloque 11 |
| Reordenamiento | `python3 scripts/regenerar_reordenamiento.py --output-dir outputs/reordenamiento` | Entorno documentado por el bloque 12 |
| Coleccionista | `PYTHONPATH=src python3 scripts/regenerar_coleccionista.py --output-dir outputs/coleccionista` | Python 3.14.5; NumPy 2.5.2; SciPy 1.18.0; Matplotlib 3.11.1; Pillow 12.3.0; Agg |

Las salidas de `outputs/` son temporales. La copia a esta carpeta requiere una
acción explícita y debe validarse después con:

```bash
python3 scripts/verificar_figuras_tesis.py
python3 scripts/verificar_figuras_tesis.py --tesis-root "/ruta/a/Tesis UNAM"
```

`--actualizar-sha` actualiza únicamente los hashes registrados y debe usarse de
forma consciente después de aprobar visualmente una regeneración.

## Procedencia de figuras propias

El manifest distingue dos situaciones de autoría propia:

- `repo_reproducible`: existe un generador y un comando versionados que producen
  la figura canónica.
- `propia_documentada`: la autoría es conocida y se conserva la versión histórica
  preferida por el autor, pero el script original no está integrado actualmente
  en el pipeline modular. Esta categoría no significa procedencia ambigua.

Las alternativas creadas por `regenerar_figuras_conceptuales.py` pueden seguir
generándose en `outputs/`, pero no reemplazan automáticamente una selección
histórica registrada como `propia_documentada`. No se buscaron los scripts
históricos en este ajuste porque esa recuperación documental tiene un alcance
separado.

## Procedencia externa conservada

- Los escudos de la UNAM y de la Facultad de Ciencias son elementos de identidad
  gráfica institucional empleados en la portada.
- La fotografía de *Conus textile* es de Richard Ling; la versión utilizada es
  un recorte de Chiswick Chap publicado en Wikimedia Commons con licencia
  CC BY-SA 3.0: <https://commons.wikimedia.org/wiki/File:Textile_cone_(cropped).JPG>.

El resto de las figuras finales son elaboraciones propias, reproducibles o
documentadas según el manifest. La procedencia visual no sustituye las citas que
respaldan definiciones o resultados matemáticos.
