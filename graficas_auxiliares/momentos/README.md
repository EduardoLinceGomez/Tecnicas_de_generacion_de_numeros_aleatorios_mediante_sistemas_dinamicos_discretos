# Referencias gráficas de momentos

Estas figuras documentan la corrección científica del bloque 09 y se generan
desde el commit `Añade análisis reproducible de momentos e histogramas`, cuyo
punto de partida es `385ff07ad47d19206a64cbaaee33532cf5040621`.

Regeneración explícita:

```bash
python3 scripts/regenerar_momentos.py \
  --output-dir outputs/momentos \
  --reference-dir graficas_auxiliares/momentos
```

La Normal y la Cauchy usan un único `RandomState(2024)`, en ese orden, con
`n=10000` cada una, ventana `[-20,20]` y 80 bins comunes de ancho `0.5`.
`outputs/` es temporal; los PNG y el CSV de esta carpeta son las referencias
versionadas aprobadas.
