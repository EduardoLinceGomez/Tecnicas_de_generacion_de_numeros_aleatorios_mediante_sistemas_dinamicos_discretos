# Comparación homogénea de generadores

Este bloque compara las cinco muestras originales: logístico uniformizado,
tienda, R30 por columnas, R30 por filas y Park--Miller MINSTD. MINSTD usa
`a=16807`, `c=0`, `m=2^31-1`, semilla 2024 y 1000 valores posteriores a la
semilla; no se reordena.

La prueba de brechas aplica a todos los generadores los intervalos abiertos
`i1=(0.1,0.3)`, `i2=(0.4,0.6)` e `i3=(0.7,0.9)`. Cada intervalo tiene
longitud y probabilidad teórica `p=0.2`, con la convención `W=G+1`.

Regeneración explícita:

```bash
python3 scripts/regenerar_comparacion_generadores.py \
  --output-dir outputs/comparacion_generadores \
  --reference-dir graficas_auxiliares/comparacion_generadores
```

`resumen_comparacion.csv` conserva las métricas existentes de CDF, momentos,
FGM, función característica, ACF y fingerprints.
`resumen_brechas_comparacion.csv` contiene 15 filas en formato largo, una por
generador e intervalo. Las figuras `brechas_comparacion_i1.png`,
`brechas_comparacion_i2.png` y `brechas_comparacion_i3.png` contienen cinco
paneles cada una y usan una sola referencia geométrica común.

Los PNG y CSV de esta carpeta son referencias versionadas; `outputs/` es
temporal. A diferencia del bloque de reordenamiento, aquí sólo se estudian
muestras originales. No se calcula promedio de intervalos, puntuación de
calidad ni clasificación automática.
