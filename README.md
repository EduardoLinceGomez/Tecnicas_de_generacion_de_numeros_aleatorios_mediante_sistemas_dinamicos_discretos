# Técnicas de generación de números aleatorios mediante sistemas dinámicos discretos

Implementación reproducible de la tesis de licenciatura de Eduardo Lince
Gómez. El repositorio permite reconstruir las muestras y análisis científicos,
regenerar figuras candidatas, comprobar baselines y rastrear la procedencia de
las figuras empleadas en el manuscrito.

La tesis estudia secuencias pseudoaleatorias obtenidas del mapeo logístico, el
mapeo tienda y el autómata celular elemental regla 30. Park–Miller MINSTD se
incluye como generador congruencial de referencia para la comparación entre
métodos.

## Estado del proyecto

El código y los baselines corresponden a la versión preparada para publicación
de la tesis. Se preservan las semillas, tamaños de muestra, fingerprints,
parámetros y resultados validados. El repositorio público contiene la
implementación y copias canónicas de las figuras, pero no el manuscrito privado
ni sus fuentes LaTeX completas.

Los análisis implementados son:

- distribución empírica e histogramas;
- momentos ordinarios y centrales;
- función generadora de momentos (FGM);
- función característica;
- autocorrelación;
- prueba de brechas con intervalos comparables;
- prueba del coleccionista de cupones;
- invariancia y evolución de distribuciones;
- reordenamiento reproducible y comparación con MINSTD.

## Requisitos

- Python 3.9 o posterior;
- `pip` y soporte para entornos virtuales;
- para figuras TeX/TikZ: una distribución TeX con `latex`, `dvipng` y
  `latexmk`, además de Poppler (`pdftoppm`).

Los análisis numéricos usan NumPy, SciPy y Matplotlib. `pyproject.toml` es la
definición normal del paquete. `requirements-repro.txt` registra el entorno
exactamente usado para la validación limpia del release; no sustituye los
entornos históricos anotados en cada baseline gráfico.

## Instalación desde cero

```bash
git clone https://github.com/EduardoLinceGomez/generadores-sistemas-dinamicos.git
cd generadores-sistemas-dinamicos
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

Después de la instalación, los scripts importan `tesis_generacion` como paquete
normal; no requieren `PYTHONPATH=src`.

Para recrear el entorno validado de este release:

```bash
python -m pip install -r requirements-repro.txt
python -m pip install -e . --no-deps
```

## Inicio rápido

Mostrar el plan completo sin ejecutar cálculos:

```bash
python scripts/reproducir_tesis.py --all --plan
```

Ejecutar experimentos y escribir métricas, CSV y figuras de diagnóstico en
`outputs/`:

```bash
python scripts/reproducir_tesis.py --experiments
```

Regenerar todas las figuras reproducibles, incluidas las fuentes TeX/TikZ y las
bifurcaciones editoriales:

```bash
python scripts/reproducir_tesis.py --figures
```

Ejecutar el flujo completo —experimentos, figuras, manifiesto, compilación de
Python y tests—:

```bash
python scripts/reproducir_tesis.py --all
```

El orquestador reutiliza los módulos y scripts existentes. Nunca copia
automáticamente resultados a `figuras_tesis/`; el reporte de ejecución queda en
`outputs/reporte_reproduccion.json`.

## Verificación

Suite completa:

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```

Compilación estática y verificación del manifiesto canónico:

```bash
python -m compileall src scripts
python scripts/verificar_figuras_tesis.py
```

Comando principal de verificación:

```bash
python scripts/reproducir_tesis.py --verify
```

Para verificar además que las copias del manuscrito privado corresponden al
manifiesto:

```bash
python scripts/verificar_figuras_tesis.py --tesis-root "/ruta/al/manuscrito"
```

La opción `--actualizar-sha` y las opciones `--reference-dir` de los scripts
individuales son operaciones explícitas de promoción. No forman parte del flujo
normal y sólo deben usarse después de una revisión científica y visual.

## Parámetros científicos centrales

`src/tesis_generacion/experimentos/parametros.py` concentra los valores comunes:

- semilla general, de reordenamiento y de MINSTD: `2024`;
- tamaño de las muestras canónicas: `1000`;
- regla 30: `1000` celdas y `1000` iteraciones;
- factor del mapeo tienda histórico: `1.999`;
- intervalos abiertos de brechas: `(0.1, 0.3)`, `(0.4, 0.6)` y `(0.7, 0.9)`;
- probabilidad común de brecha: `p = 0.2`, con convención `W = G + 1`.

La precisión decimal del coleccionista es `12` y está definida en
`src/tesis_generacion/transformaciones/codificacion_decimal.py`. Los detalles,
fingerprints y tolerancias están en `docs/reproducibilidad.md` y
`tests/data/`.

## Estructura del repositorio

```text
src/tesis_generacion/   paquete: generadores, transformaciones y análisis
scripts/                comandos de reproducción y verificación
tests/                  invariantes, baselines, CLI y regresión visual
tests/data/             baselines científicos y entornos gráficos históricos
figuras_tesis/          copias canónicas y manifiesto de procedencia
graficas_auxiliares/    diagnósticos científicos versionados
docs/                   arquitectura y contrato de reproducibilidad
legacy/                 notebooks y adaptadores históricos preservados
outputs/                resultados regenerados locales; ignorados por Git
```

La arquitectura detallada está en `docs/arquitectura.md`.

## Figuras y procedencia

`figuras_tesis/manifest_figuras.csv` clasifica las 65 figuras o recursos como:

- `repo_reproducible`: el generador y el comando están versionados;
- `propia_documentada`: creación propia histórica conservada sin afirmar una
  regeneración binaria equivalente;
- `externa_citada`: recurso externo o institucional con procedencia declarada.

`figuras_tesis/` contiene las copias canónicas usadas por la tesis.
`graficas_auxiliares/` contiene resultados útiles para diagnóstico o
comparación que no necesariamente aparecen en el manuscrito. `outputs/` es el
área desechable donde se regeneran candidatos; no es una fuente canónica.

Las bifurcaciones históricas permanecen como `propia_documentada`. El generador
editorial recuperado produce candidatos científicamente equivalentes y de alta
resolución, pero no se presenta como reproducción binaria de los PNG originales.

## Reproducibilidad científica y binaria

La reproducibilidad científica significa conservar muestras, orden,
fingerprints, parámetros, métricas y tolerancias. Es el criterio principal.
La identidad binaria de un PNG es más estricta: puede variar entre versiones de
Matplotlib, Pillow, FreeType o por metadatos y compresión sin alterar los datos
ni los píxeles relevantes.

Por eso los tests científicos siempre se ejecutan y las comparaciones SHA-256
de PNG sólo se activan con las variables de entorno documentadas en
`docs/reproducibilidad.md`, usando el entorno histórico correspondiente.

## Relación con el manuscrito

Este repositorio es público y contiene la implementación científica. El
manuscrito de la tesis se mantiene en un repositorio privado independiente.
`archivo_tesis` en el manifiesto registra la ruta histórica dentro de ese
manuscrito, mientras `archivo_canonico` identifica la copia pública verificada.
Ningún comando normal modifica el repositorio privado.

## Cita

Los metadatos legibles por gestores bibliográficos están en `CITATION.cff`. En
forma breve:

> Lince Gómez, Eduardo. *Técnicas de generación de números aleatorios mediante
> sistemas dinámicos discretos*. Implementación de tesis, 2026.

## Licencia

El código y la documentación se distribuyen bajo la licencia MIT; consulte
`LICENSE`. Los recursos externos conservan sus atribuciones y licencias propias,
documentadas en el manifiesto y en `figuras_tesis/README.md`.
