# Reordenamiento y dependencia serial

Estas referencias documentan el commit científico `Añade análisis reproducible
del reordenamiento serial`. El procedimiento aplica el ranking de una órbita
logística auxiliar como permutación y nunca modifica las muestras canónicas.

Regeneración explícita:

```bash
python3 scripts/regenerar_reordenamiento.py \
  --output-dir outputs/reordenamiento \
  --reference-dir graficas_auxiliares/reordenamiento
```

El caso logístico usa un `RandomState(2024)` local para fijar el estado inicial
de su órbita auxiliar. Tienda y ambas lecturas de R30 comparten la órbita
auxiliar histórica con (r=4) y (x_0=0.02024). Las ACF usan los rezagos 1 a
20; la prueba de brechas conserva los cuatro intervalos del notebook.
`outputs/` es temporal y los PNG y el CSV de esta carpeta son referencias
versionadas.
