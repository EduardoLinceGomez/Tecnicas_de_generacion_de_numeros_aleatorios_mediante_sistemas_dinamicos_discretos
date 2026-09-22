# Figuras canónicas de la tesis

Esta carpeta contiene las copias públicas de los recursos usados por el
manuscrito. `manifest_figuras.csv` registra para cada entrada la ruta histórica
en la tesis, su copia canónica, procedencia, generador, parámetros y SHA-256.

Las salidas nuevas se generan en `outputs/`. Ninguno de los comandos de esta
página promueve automáticamente archivos a esta carpeta.

## Regeneración

Después de `python -m pip install -e .`, el punto de entrada recomendado es:

```bash
python scripts/reproducir_tesis.py --figures
```

Comandos individuales:

| Familia | Comando | Requisitos o alcance |
|---|---|---|
| Conceptuales e histogramas básicos | `python scripts/regenerar_figuras_conceptuales.py --output-dir outputs/figuras_tesis` | Python; también genera reconstrucciones no canónicas de bifurcaciones |
| PCC y PG | `python scripts/regenerar_figuras_tikz.py --output-dir outputs/figuras_tikz` | TeX Live, `latexmk` y `pdftoppm` |
| Figuras TeX estáticas | `python scripts/regenerar_figuras_revision_mcf.py --output-dir outputs/revision_mcf` | TeX Live y `latexmk` |
| Bifurcaciones editoriales | `MPLBACKEND=Agg python scripts/regenerar_bifurcaciones.py --output-dir outputs/bifurcaciones_publicacion` | LaTeX y `dvipng`; candidatos PDF/SVG/PNG |
| Momentos | `python scripts/regenerar_momentos.py --output-dir outputs/momentos` | Figuras, CSV y métricas |
| FGM y función característica | `python scripts/regenerar_transformadas.py --output-dir outputs/transformadas` | Figuras, CSV y métricas |
| Invariancia | `python scripts/regenerar_invariancia.py --output-dir outputs/invariancia` | Figuras, CSV y fingerprints |
| Reordenamiento | `python scripts/regenerar_reordenamiento.py --output-dir outputs/reordenamiento` | ACF, brechas, CSV y permutaciones |
| Comparación con MINSTD | `python scripts/regenerar_comparacion_generadores.py --output-dir outputs/comparacion_generadores` | Cinco muestras originales, sin ranking agregado |
| Coleccionista | `python scripts/regenerar_coleccionista.py --output-dir outputs/coleccionista` | Ocho figuras y métricas; precisión decimal 12 |

## Verificación

```bash
python scripts/verificar_figuras_tesis.py
```

Para comprobar además las rutas del manuscrito privado:

```bash
python scripts/verificar_figuras_tesis.py --tesis-root "/ruta/al/manuscrito"
```

La identidad binaria de PNG depende del entorno anotado en `tests/data/`. La
suite normal siempre valida los resultados científicos; los hashes PNG
históricos sólo se activan con las variables descritas en
`docs/reproducibilidad.md`.

## Clasificación de procedencia

- `repo_reproducible`: existe un comando versionado que regenera la figura;
- `propia_documentada`: figura propia histórica conservada sin afirmar que un
  generador actual produzca exactamente el mismo archivo;
- `externa_citada`: recurso externo o institucional con atribución.

Las figuras de bifurcación siguen clasificadas como `propia_documentada`. El
generador recuperado en `regenerar_bifurcaciones.py` reproduce la dinámica y los
parámetros científicos, pero genera candidatos editoriales de mayor resolución,
no los mismos bytes del PNG histórico.

## Promoción intencional

Algunos scripts aceptan `--reference-dir`; esa opción copia resultados y no se
usa en los comandos anteriores ni en el orquestador. Una promoción correcta
requiere:

1. comparar métricas, fingerprints y parámetros;
2. revisar visualmente el candidato;
3. copiar sólo los archivos aprobados;
4. actualizar el SHA del manifiesto de forma explícita;
5. volver a ejecutar tests y `verificar_figuras_tesis.py`.

No se debe copiar `outputs/` completo sobre `figuras_tesis/`.

## Recursos externos

Los escudos de la UNAM y de la Facultad de Ciencias son recursos
institucionales. La fotografía de *Conus textile* es de Richard Ling; la copia
usada deriva del recorte de Chiswick Chap publicado en Wikimedia Commons bajo
CC BY-SA 3.0. El manifiesto conserva la atribución correspondiente.
