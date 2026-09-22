# Regeneración editorial de las bifurcaciones

Este bloque produce candidatos de revisión para las dos figuras de bifurcación.
No copia archivos al repositorio de la tesis ni modifica sus fuentes LaTeX.

## Procedencia revisada

- `legacy/notebooks/MainGenerador.ipynb` contiene las funciones iterativas `logistic_map` y
  `tent_map`, la condición inicial logística `0.02024` y los experimentos de
  muestras, pero no contiene celdas que generen los diagramas de bifurcación.
- `legacy/notebooks/atraccion-densidades-mapeos.nb` estudia la evolución de densidades mediante
  los operadores de transferencia logístico y tienda; no genera los diagramas
  de bifurcación usados por la tesis.
- `src/tesis_generacion/visualizacion/figuras_tesis.py` aporta una
  reconstrucción reproducible posterior: rangos `[2.8, 4.0]` y `[1.0, 2.0]`,
  condición inicial `0.02024`, 900 iteraciones transitorias, 100 iteraciones
  representadas y 2400 valores del parámetro. Las imágenes históricas se
  conservaron como canónicas y esa reconstrucción no las sustituyó.

El nuevo módulo reutiliza esa reconstrucción matemática y aumenta únicamente
la malla horizontal a 6000 valores. Recupera de las imágenes canónicas los
labels breves `$r$`, `$\mu$` y `$x^*$`, la ausencia de título interno, la
retícula punteada, la orientación apaisada y la ocultación de los labels del
eje vertical en la figura del mapeo tienda.

## Comando

```bash
MPLBACKEND=Agg python3 scripts/regenerar_bifurcaciones.py \
  --output-dir outputs/bifurcaciones_publicacion
```

La configuración predeterminada es:

| Parámetro | Valor |
|---|---:|
| Valores del parámetro | 6000 por figura |
| Burn-in | 900 iteraciones |
| Iteraciones graficadas | 100 |
| Condición inicial | 0.02024 |
| Puntos representados | 600000 por figura |
| Alpha | 0.45 |
| Tamaño de punto | 0.20 pt² |
| Tamaño de figura | 12.0 × 8.36 cm |
| Resolución de la nube | 600 dpi |
| Salidas | PDF híbrido, SVG híbrido y PNG de inspección |

En PDF y SVG, la nube de puntos queda rasterizada a alta resolución y los
ejes, ticks y labels permanecen vectoriales. Las etiquetas se componen con una
instalación real de LaTeX y la familia Computer Modern, consistente con el
manuscrito. El script falla de forma explícita si faltan `latex` o `dvipng`.

El archivo `reporte_bifurcaciones.json` registra configuración, versiones,
rutas, tamaños y SHA-256 de cada salida. La eventual sustitución de
`recursos/graficas/Logist/Log_bif3.png` y
`recursos/graficas/Tent/tent_bif.png` queda pendiente de revisión visual y de
una autorización separada para modificar la tesis.
