# Transformadas auxiliares

Estas referencias documentan el error histórico de calcular la FGM y la función
característica logísticas con la órbita cruda de 1001 valores, en vez de la
muestra uniformizada canónica de 1000 valores. No se incorporan automáticamente
a la tesis.

Se regeneran, bajo el entorno de referencia, con:

```bash
python scripts/regenerar_transformadas.py \
  --output-dir outputs/transformadas \
  --reference-dir graficas_auxiliares/transformadas
```

La FGM se evalúa en 40 puntos comunes de `[0, 15]` y la función característica
en 60 puntos comunes de `[0, 20]`. `outputs/` es temporal; los dos PNG y el CSV
de esta carpeta son referencias versionadas. Sus valores y SHA-256 exactos se
registran en `tests/data/transformadas_baseline.json`.
