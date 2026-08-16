# Comparación homogénea de generadores

Estas referencias documentan el commit científico `Documenta R30 y añade
comparación con generador congruencial`. El benchmark es Park--Miller MINSTD
(1988), con (a=16807), (c=0), (m=2^{31}-1), semilla 2024 y 1000 valores
posteriores a la semilla.

Regeneración explícita:

```bash
python3 scripts/regenerar_comparacion_generadores.py \
  --output-dir outputs/comparacion_generadores \
  --reference-dir graficas_auxiliares/comparacion_generadores
```

La comparación usa las cinco muestras originales, los primeros 20 momentos,
las mallas FGM/FC de los bloques previos y la ACF en rezagos 1 a 20. No produce
una puntuación agregada. `outputs/` es temporal; los PNG y el CSV de esta
carpeta son referencias versionadas.
