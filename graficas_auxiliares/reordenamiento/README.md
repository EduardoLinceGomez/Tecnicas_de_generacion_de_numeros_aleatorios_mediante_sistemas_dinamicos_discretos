# Reordenamiento y dependencia serial

Este bloque compara cada una de las cuatro muestras canónicas con su propia
permutación. El protocolo de brechas usa en todos los casos los intervalos
abiertos `i1=(0.1,0.3)`, `i2=(0.4,0.6)` e `i3=(0.7,0.9)`. Todos tienen
longitud y probabilidad teórica `p=0.2`; la convención es `W=G+1`.

Regeneración explícita:

```bash
python3 scripts/regenerar_reordenamiento.py \
  --output-dir outputs/reordenamiento \
  --reference-dir graficas_auxiliares/reordenamiento
```

`resumen_reordenamiento.csv` contiene sólo magnitudes independientes del
intervalo: método, fingerprints y ACF. `resumen_brechas_reordenamiento.csv`
contiene 12 filas en formato largo, una por muestra e intervalo, con métricas
originales y reordenadas. Los cuatro `brechas_antes_despues_*.png` muestran
tres paneles y son las referencias auxiliares de los cuatro nombres PG
canónicos conservados por la tesis. Los PNG y CSV de esta carpeta son
referencias versionadas; `outputs/` es temporal.

El logístico usa un `RandomState(2024)` local para la órbita auxiliar. Tienda y
R30 comparten la órbita con `r=4` y `x0=0.02024`. Las ACF conservan los lags
1 a 20. Reordenar no cambia la pertenencia al intervalo, por lo que original y
reordenada tienen el mismo número de tiempos completos para cada intervalo.

Este bloque estudia el efecto del orden. No es la comparación de cinco muestras
originales con MINSTD y no produce promedio, puntuación ni ranking global.
