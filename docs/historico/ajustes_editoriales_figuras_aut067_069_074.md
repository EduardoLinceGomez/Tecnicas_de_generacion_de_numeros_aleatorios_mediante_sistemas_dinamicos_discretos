# Ajustes editoriales de histogramas — AUT-067, AUT-069 y AUT-074

## Estado y trazabilidad

- **Fecha:** 2026-09-21.
- **Estado:** IMPLEMENTADO y validado.
- **Repositorio:** `EduardoLinceGomez/Tecnicas_de_generacion_de_numeros_aleatorios_mediante_sistemas_dinamicos_discretos`.
- **Rama base:** `reestructuracion/repositorio`.
- **Commit base:** `a95f7e13b5b59ed97bab77dbd66b6cc1d7c77b70`.
- **Rama de implementación:** `feat/ajustes-figuras-aut067-aut069-aut074`.
- **Commit de implementación:** `33e683d5fea12d519a0b07ea16f6a2d7e77177ae`.

El cambio responde a AUT-067, AUT-069 y AUT-074. Su único propósito es
retirar la indicación redundante `(n=1000)` de cuatro títulos internos de
histogramas canónicos. El tamaño real de las muestras continúa siendo 1000.

## Títulos modificados

| AUT | Figura | Título anterior | Título nuevo |
|---|---|---|---|
| AUT-074 | FIG-023 | `Mapeo logístico uniformizado (n=1000)` | `Mapeo logístico uniformizado` |
| AUT-069 | FIG-024 | `Mapeo tienda, factor 1.999 (n=1000)` | `Mapeo tienda, factor 1.999` |
| AUT-067 | FIG-026 | `Regla 30 por columnas (n=1000)` | `Regla 30 por columnas` |
| AUT-067 | FIG-027 | `Regla 30 por filas (n=1000)` | `Regla 30 por filas` |

Las cuatro cadenas se modificaron exclusivamente en
`src/tesis_generacion/visualizacion/figuras_tesis.py`.

## Figuras y hashes

| Figura | Archivo canónico | SHA-256 anterior | SHA-256 nuevo |
|---|---|---|---|
| FIG-023 | `figuras_tesis/cientificas/logistico_histograma.png` | `c13ddf4256a6a23e099be4b771298498a17fa2003707808df5d3a60c1f25ba0f` | `a65dc02be3e517974736ff9613a9175bc14fc89507eeaf06debbf3118b160fa8` |
| FIG-024 | `figuras_tesis/cientificas/tienda_histograma.png` | `4e5b2e3e572ef43194a01774bd0573d081758fb12816035da11bc6e9c85e648e` | `bae79dbb3fd2c0d9775d56eab6b942d14eb4774e7cceebff07352014b3a4a8e1` |
| FIG-026 | `figuras_tesis/cientificas/r30_hist_columnas.png` | `b01f1826616ccb335ab20fbe48f5fd6cec4a8358545bce88eb63852d49b16540` | `fc3506a0797b59047a86a4832e69f5fe1b218623d2ea935040388f2b5494dec1` |
| FIG-027 | `figuras_tesis/cientificas/r30_hist_filas.png` | `f304fcc2abd1f257511fb0cfb2535f07e2e2f62dd205a860d4cf6e197f8b0272` | `391d406f8dbd61aca738b026f275903b4d660e09cdcd74bb4629b6f69904b19c` |

Sólo estos cuatro hashes se actualizaron en
`figuras_tesis/manifest_figuras.csv`.

## Regeneración y validación

La regeneración inicial se realizó en un directorio temporal:

```bash
MPLBACKEND=Agg python3 scripts/regenerar_figuras_conceptuales.py \
  --output-dir outputs/figuras_tesis
```

Después de la comparación e inspección visual se sincronizaron únicamente las
cuatro salidas aprobadas con el directorio canónico. La validación final usó:

```bash
python3 scripts/verificar_figuras_tesis.py
MPLBACKEND=Agg python3 -m pytest -q \
  tests/test_visualizacion_figuras_tesis.py \
  tests/test_manifest_figuras.py \
  tests/test_cli_figuras_tesis.py
MPLBACKEND=Agg python3 -m unittest discover -s tests -p 'test_*.py' -v
git diff --check
```

Resultados:

- manifest: 65 entradas y 0 errores;
- pruebas específicas: 15 aprobadas;
- suite `unittest`: 129 pruebas descubiertas, 123 aprobadas y 6 verificaciones
  PNG opcionales omitidas por defecto;
- `git diff --check`: sin errores.

La comparación byte a byte de las 13 salidas canónicas activas producidas por
el pipeline mostró exactamente cuatro archivos distintos: FIG-023, FIG-024,
FIG-026 y FIG-027. En cada caso, la comparación de píxeles localizó todas las
diferencias en la franja superior ocupada por el título. Las barras, datos,
10 intervalos, densidades, ejes, límites, leyendas y fuentes científicas
permanecieron iguales. Las cuatro figuras se inspeccionaron a resolución
original y sus títulos nuevos resultaron legibles.

## Handoff a la tesis

Las copias que deben sincronizarse sin regeneración independiente son:

- FIG-023 → `recursos/graficas/Logist/Uniformidad/LogUnif_histograma.png`;
- FIG-024 → `recursos/graficas/Tent/Uniformidad/Tent_histograma.png`;
- FIG-026 → `recursos/graficas/R30/Uniformidad/muestra_col.png`;
- FIG-027 → `recursos/graficas/R30/Uniformidad/muestra_fila.png`.

La sincronización debe conservar exactamente los SHA-256 nuevos registrados en
la tabla anterior. Los captions, rutas y etiquetas de la tesis no forman parte
del cambio científico.
