# AUT-105: EAM del coleccionista sobre una malla común

## Estado y alcance

- **Fecha:** 2026-09-22.
- **Estado:** IMPLEMENTADO y validado localmente.
- **Base:** `reestructuracion/repositorio@de052fa68eb6ebb94fd09a7d087fdc4c813555b8`.
- **Rama:** `feat/aut-105-eam-coleccionista-malla-comun`.
- **Participantes:** logístico transformado, tienda, R30 columnas y R30 filas,
  todos en su versión original.
- **Exclusiones:** MINSTD y muestras reordenadas.

AUT-105 hace comparables los errores absolutos medios de las CDF del
coleccionista de cupones. No cambia las muestras, la codificación decimal, los
bloques observados ni la referencia teórica; únicamente amplía el dominio de
evaluación del EAM hasta un máximo común.

## Metodología

Para cada muestra original \(S\), sea \(M(S)\) la mayor longitud de bloque
completo observada. La fuente única
`experimentos/soportes_coleccionista.py` deriva dinámicamente

\[
M^*=\max_S M(S)=91
\]

a partir de las cuatro muestras. El valor 91 no aparece como constante de la
implementación. El EAM comparable es

\[
\operatorname{EAM}_F(S)=\frac{1}{M^*-9}
\sum_{m=10}^{M^*}\left|F_{\mathrm{emp},S}(m)-F_{\mathrm{teo}}(m)\right|.
\]

Para \(m>M(S)\), la búsqueda acumulada sobre las longitudes completas produce
\(F_{\mathrm{emp},S}(m)=1\). La discrepancia máxima \(D_{\max}\) también se
evalúa sobre `10..M*`; en las cuatro muestras coincide exactamente con su valor
histórico.

`metricas_coleccionista()` acepta ahora `maximo_soporte` como argumento
opcional. Al omitirlo conserva exactamente el diccionario y los valores
históricos. Al proporcionarlo, `maximo` continúa siendo el máximo observado y
`maximo_soporte_evaluacion` registra por separado el extremo de la malla. El
soporte externo debe ser entero, no booleano, y al menos tan grande como el
máximo observado.

## Resultados con precisión completa

| Muestra | M | M* | Dmax anterior | Dmax nuevo | EAM anterior | EAM nuevo | Delta |
|---|---:|---:|---:|---:|---:|---:|---:|
| Logístico transformado | 67 | 91 | 0.06239741904102747 | 0.06239741904102747 | 0.0285822127624915 | 0.021084095258261694 | -0.007498117504229806 |
| Tienda | 86 | 91 | 0.030273814306883917 | 0.030273814306883917 | 0.007884894696680737 | 0.007456286994899498 | -0.00042860770178123914 |
| R30 columnas | 91 | 91 | 0.05969646946652962 | 0.05969646946652962 | 0.012624459072199258 | 0.012624459072199258 | 0.0 |
| R30 filas | 91 | 91 | 0.04695242695186852 | 0.04695242695186852 | 0.005696878167701897 | 0.005696878167701897 | 0.0 |

## Resultados redondeados a cuatro decimales

| Muestra | Dmax anterior | Dmax nuevo | EAM anterior | EAM nuevo | Delta |
|---|---:|---:|---:|---:|---:|
| Logístico transformado | 0.0624 | 0.0624 | 0.0286 | 0.0211 | -0.0075 |
| Tienda | 0.0303 | 0.0303 | 0.0079 | 0.0075 | -0.0004 |
| R30 columnas | 0.0597 | 0.0597 | 0.0126 | 0.0126 | 0.0000 |
| R30 filas | 0.0470 | 0.0470 | 0.0057 | 0.0057 | 0.0000 |

## Orden descriptivo entre muestras

De menor a mayor EAM, el orden histórico era:

1. R30 filas;
2. tienda;
3. R30 columnas;
4. logístico transformado.

El orden nuevo es exactamente el mismo. AUT-105 reduce el EAM del logístico y
de tienda porque extiende sus soportes de 67 y 86 a 91, respectivamente. R30
columnas y R30 filas ya se evaluaban hasta 91, por lo que conservan exactamente
su EAM anterior.

## Invariantes comprobados

- `M*` se deriva de los máximos observados `67, 86, 91, 91`.
- Los cuatro fingerprints SHA-256 son idénticos al baseline.
- Se conservan semilla 2024, precisión decimal 12, 1000 valores y 12000 dígitos
  por muestra.
- Se conservan bloques completos, cola censurada, mínimo, máximo observado,
  media, mediana, media teórica y diferencia de medias.
- `Dmax` se evalúa en la malla común y permanece idéntico en las cuatro muestras.
- Los EAM de R30 columnas y R30 filas son exactamente iguales al baseline.
- No se modificó ni reemplazó ningún PNG. La prueba gráfica estricta reprodujo
  los ocho hashes del entorno de referencia.

## Validación ejecutada

La instalación editable local apuntaba a otro checkout; por ello, todas las
ejecuciones autoritativas fijaron `PYTHONPATH=src` para importar este worktree
exacto.

```bash
PYTHONPATH=src MPLBACKEND=Agg python3 -m unittest -v \
  tests.test_estadistica_coleccionista \
  tests.test_soportes_coleccionista \
  tests.test_baseline_coleccionista \
  tests.test_visualizacion_coleccionista \
  tests.test_cli_coleccionista

PYTHONPATH=src MPLBACKEND=Agg \
  python3 -m unittest discover -s tests -p 'test_*.py' -q

PYTHONPATH=src VERIFICAR_PNG_EXACTO=1 MPLBACKEND=Agg \
  python3 -m unittest -v \
  tests.test_baseline_coleccionista.BaselineGraficoEstrictoTest

PYTHONPATH=src python3 -m compileall -q \
  src tests/test_soportes_coleccionista.py

git diff --check
```

Resultados:

- pruebas específicas: 25 ejecutadas, 24 aprobadas y una comprobación PNG
  opcional omitida en esa primera ejecución;
- suite completa: 141 pruebas ejecutadas, 135 aprobadas y 6 comprobaciones PNG
  opcionales omitidas;
- comprobación PNG estricta: 1 aprobada;
- compilación de módulos: correcta;
- `git diff --check`: sin errores.

## Archivos de implementación

- `src/tesis_generacion/estadistica/coleccionista.py`;
- `src/tesis_generacion/experimentos/soportes_coleccionista.py`;
- `src/tesis_generacion/experimentos/__init__.py`;
- `src/tesis_generacion/visualizacion/coleccionista.py`;
- `tests/test_soportes_coleccionista.py`;
- `tests/test_visualizacion_coleccionista.py`;
- `docs/resultados_eam_coleccionista_malla_comun.md`.

No se modificó el repositorio de la tesis.
