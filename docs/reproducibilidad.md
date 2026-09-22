# Reproducibilidad científica

Este documento describe el contrato vigente del repositorio. Los informes de
desarrollo se conservan en `docs/historico/`, pero no sustituyen estas reglas.

## Entorno

La instalación normal se define en `pyproject.toml` y admite Python 3.9 o
posterior con NumPy 1.23–2.x, SciPy 1.9–1.x y Matplotlib 3.6–3.x. El release se
validó desde un entorno limpio con las versiones fijadas en
`requirements-repro.txt`.

Los baselines PNG se crearon en más de un entorno histórico. Cada JSON de
`tests/data/` registra el suyo; no existe una única combinación de versiones
que deba fingirse como origen binario de todos los PNG. El backend de referencia
es `Agg`.

Las figuras TikZ y TeX requieren `latexmk` y `pdftoppm`. Las bifurcaciones
editoriales requieren además `latex` y `dvipng` para componer las etiquetas.

## Semillas, tamaños y parámetros

Los parámetros transversales viven en
`src/tesis_generacion/experimentos/parametros.py`:

| Parámetro | Valor |
|---|---:|
| `SEED` | 2024 |
| `SEED_REORDENAMIENTO` | 2024 |
| `SEED_MINSTD` | 2024 |
| `NUM_VALORES` | 1000 |
| `NUM_ITERACIONES` | 1000 |
| `NUM_CELDAS` | 1000 |
| `FACTOR_TIENDA` | 1.999 |

La codificación decimal del coleccionista usa
`PRECISION_DECIMAL = 12`. Cada muestra canónica produce 12 000 dígitos. La
regla 30 se interpreta de forma periódica y se extraen muestras por columnas y
por filas mediante las funciones versionadas en `transformaciones/`.

La prueba de brechas usa los intervalos abiertos comunes
`(0.1, 0.3)`, `(0.4, 0.6)` y `(0.7, 0.9)`. La longitud y probabilidad común es
`0.2`; la convención de espera es `W = G + 1`. Se valida con `math.isclose`
porque `0.3 - 0.1` no tiene representación binaria decimal exacta.

## Fingerprints de muestras

Cada muestra se normaliza como un array contiguo `float64` little-endian y el
SHA-256 se calcula sobre sus 8000 bytes en orden C.

| Muestra | Elementos | SHA-256 |
|---|---:|---|
| Logístico | 1000 | `7b088ec20314081394523a732c4270c531dbf4219c521e146abf87ef59e51491` |
| Tienda | 1000 | `0726a1fb5a0e886bb09ea70fbd2595631d95c9c3592648a905ebdf49dc2223a3` |
| R30 columnas | 1000 | `b81d0a7733d126c104bc778d8a6cc8efcfaab5098291dbc4e517f796744250bb` |
| R30 filas | 1000 | `989b081363d4eb6d6b4a2b3fc9630a03b5c380b3b36075dcb24e19824b16b4c4` |

MINSTD y las muestras reordenadas tienen fingerprints adicionales en
`comparacion_generadores_baseline.json` y `reordenamiento_baseline.json`.

## Baselines

Los archivos de `tests/data/` tienen funciones distintas:

- `coleccionista_baseline.json`: métricas, media teórica y fingerprints;
- `coleccionista_sha256.json`: hashes PNG del entorno histórico;
- `momentos_baseline.json`: momentos, histogramas y convenciones;
- `transformadas_baseline.json`: mallas, puntos de control, FGM y función
  característica;
- `invariancia_baseline.json`: ensembles, iteraciones y fingerprints;
- `reordenamiento_baseline.json`: permutaciones, ACF y 24 resúmenes de brechas;
- `comparacion_generadores_baseline.json`: cinco muestras, MINSTD y 15 resúmenes
  de brechas.

Los CSV versionados de `graficas_auxiliares/` son resultados científicos, no
archivos temporales. No se actualizan a mano: deben regenerarse con el pipeline
y compararse antes de cualquier promoción.

## Tolerancias

Los invariantes discretos —tamaños, semillas, permutaciones, conteos,
fingerprints y listas de parámetros— se comparan exactamente. Los tests de
ensembles de invariancia también exigen igualdad numérica con `rtol=0` y
`atol=0`.

Para resultados de punto flotante derivados:

- métricas del coleccionista y adaptadores visuales: tolerancia absoluta
  `1e-12`;
- FGM, función característica y CDF controladas: `rtol=0`, `atol=1e-15`;
- identidades analíticas simples: `assertAlmostEqual` entre 14 y 15 decimales;
- igualdad de la longitud de intervalos: tolerancia absoluta `1e-12`.

Las tolerancias no se aplican para ocultar cambios de muestra. Antes se valida
el fingerprint exacto y después la métrica derivada.

## Figuras

`figuras_tesis/manifest_figuras.csv` es el inventario contractual de 65
recursos. Cada entrada contiene ruta del manuscrito, copia canónica,
procedencia, generador, comando, parámetros y SHA-256.

Las categorías de procedencia son:

1. `repo_reproducible`: existe un comando versionado que regenera la salida;
2. `propia_documentada`: figura propia histórica cuya reconstrucción exacta no
   está integrada o no es binariamente equivalente;
3. `externa_citada`: recurso institucional o externo con atribución.

Las bifurcaciones históricas siguen en la segunda categoría. El script
`regenerar_bifurcaciones.py` recupera la dinámica, rango, condición inicial,
burn-in e iteraciones y produce candidatos editoriales de mayor resolución.
No reemplaza silenciosamente los PNG canónicos.

## Reproducibilidad científica frente a identidad PNG

Una salida es científicamente reproducible cuando mantiene datos, orden,
parámetros, métricas, soporte y convenciones. Un PNG es binariamente idéntico
sólo si coinciden también el stack gráfico, las fuentes, la compresión y los
metadatos.

Matplotlib, Pillow, FreeType y el backend pueden cambiar bytes —e incluso
pequeños detalles de antialiasing— sin cambiar el experimento. Por eso los
hashes PNG son un control secundario. Las pruebas estrictas se habilitan sólo
en su entorno anotado:

```bash
VERIFICAR_PNG_EXACTO=1 \
VERIFICAR_PNG_INVARIANCIA=1 \
VERIFICAR_PNG_REORDENAMIENTO=1 \
VERIFICAR_PNG_COMPARACION=1 \
MPLBACKEND=Agg \
python -m unittest discover -s tests -p 'test_*.py' -v
```

Si el entorno no coincide, se ejecutan todos los invariantes científicos y se
omiten únicamente los hashes gráficos que declaran esa condición.

## Flujo de reproducción

```bash
python scripts/reproducir_tesis.py --experiments
python scripts/reproducir_tesis.py --figures
python scripts/reproducir_tesis.py --verify
python scripts/reproducir_tesis.py --all
```

Todos los candidatos se escriben en `outputs/`. La verificación canónica es:

```bash
python scripts/verificar_figuras_tesis.py
```

Promover una salida requiere comparar métricas y hashes, revisar visualmente y
usar de forma consciente el `--reference-dir` del script correspondiente o
actualizar el manifiesto. El orquestador nunca realiza esa promoción.

## Invariantes que no deben cambiar

- las cuatro muestras canónicas y sus fingerprints;
- la muestra MINSTD y las permutaciones de reordenamiento;
- semillas, tamaños y precisión decimal;
- intervalos abiertos de brechas, `p=0.2` y `W=G+1`;
- métricas y puntos de control de los baselines;
- CSV científicos versionados salvo corrección aprobada;
- las rutas y hashes canónicos del manifiesto salvo promoción explícita.

Un cambio que viole uno de estos puntos es científico, no una limpieza de
código, y requiere revisión independiente.
