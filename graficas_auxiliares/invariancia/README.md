# Invariancia y evolución de distribuciones

Estas referencias documentan el experimento reproducible del bloque 11. Se
regeneran con `python3 scripts/regenerar_invariancia.py --reference-dir
graficas_auxiliares/invariancia`.

Se usa un ensamble fijo de 1000 partículas, semilla 2024 e iteraciones de 0 a
4. El logístico emplea `r=4` y una triangular simétrica `(0, 0.5, 1)`; la
tienda teórica emplea `mu=2` y una inicial `Beta(2,2)`. La comparación con
factor `1.999` es solo diagnóstica y no altera la muestra canónica. `outputs/`
continúa siendo temporal; los archivos de esta carpeta son referencias
versionadas.
