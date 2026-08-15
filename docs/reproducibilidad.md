# Reproducibilidad y baseline científico

## Punto de control

El commit científico de origen es
`d837e4fc1e3c773b129a7036a36c91a975d185d7`. El baseline registra el
comportamiento que los commits posteriores de movimiento y refactorización
deben conservar. No introduce ni valida correcciones científicas nuevas.

Los parámetros protegidos son:

- `PRECISION_DECIMAL = 12`;
- `SEED = 2024` en los experimentos que ya fijan semilla;
- cuatro muestras de 1000 valores y 12000 dígitos cada una.

## Métricas de referencia

| Muestra | Bloques | Cola | Mín. | Máx. | Media | Mediana | CDF máx. | MAE CDF |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Logístico | 435 | 13 | 10 | 67 | 27.55632183908046 | 26 | 0.06239741904102747 | 0.0285822127624915 |
| Tienda | 415 | 0 | 12 | 86 | 28.91566265060241 | 27 | 0.030273814306883917 | 0.007884894696680737 |
| R30 columnas | 423 | 16 | 12 | 91 | 28.33096926713948 | 27 | 0.05969646946652962 | 0.012624459072199258 |
| R30 filas | 413 | 35 | 11 | 91 | 28.97094430992736 | 26 | 0.04695242695186852 | 0.005696878167701897 |

La media teórica es `29.289682539682538`. Los valores completos están en
`tests/data/coleccionista_baseline.json`; los tests usan tolerancias explícitas
y no redondean resultados para forzar coincidencias.

## Fingerprints de las muestras

Cada muestra se convierte a un array contiguo con `dtype="<f8"` (float64,
little-endian) y se calcula SHA-256 sobre sus 8000 bytes en orden C.

| Muestra | Elementos | SHA-256 |
|---|---:|---|
| Logístico | 1000 | `7b088ec20314081394523a732c4270c531dbf4219c521e146abf87ef59e51491` |
| Tienda | 1000 | `0726a1fb5a0e886bb09ea70fbd2595631d95c9c3592648a905ebdf49dc2223a3` |
| R30 columnas | 1000 | `b81d0a7733d126c104bc778d8a6cc8efcfaab5098291dbc4e517f796744250bb` |
| R30 filas | 1000 | `989b081363d4eb6d6b4a2b3fc9630a03b5c380b3b36075dcb24e19824b16b4c4` |

Los fingerprints detectan cualquier cambio en los valores, su orden o su
representación binaria sin copiar la implementación científica al test.

## Reproducibilidad científica y PNG binario

Las muestras, las métricas, la CDF/PMF y las propiedades de MCF-036 son el
baseline científico obligatorio. Los SHA-256 de los PNG son un control
secundario y estricto.

El entorno usado para fijar los hashes gráficos fue:

- Python 3.14.5;
- NumPy 2.5.2;
- SciPy 1.18.0;
- Matplotlib 3.11.1;
- Pillow 12.3.0;
- backend `Agg`.

Versiones distintas pueden producir PNG byte-distintos por cambios de
compresión. La auditoría comprobó que esos archivos pueden conservar píxeles,
dimensiones y metadatos idénticos aunque cambie su SHA-256. Por ello, las
métricas y los fingerprints tienen prioridad científica.

## Ejecución de pruebas

Desde la raíz del repositorio:

```bash
python3 -m unittest -v
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

La verificación PNG exacta se activa solamente en el entorno de referencia:

```bash
VERIFICAR_PNG_EXACTO=1 \
MPLBACKEND=Agg \
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Conviene establecer `PYTHONPYCACHEPREFIX` y `MPLCONFIGDIR` en directorios
temporales durante validaciones automatizadas.

## Inconsistencias conocidas que NO se corrigen en la reestructuración

- muestra logística sin uniformizar en momentos, MGF y función característica;
- diferencia de 1001 frente a 1000 valores logísticos;
- parámetro del mapeo tienda `1.999` frente a la teoría con `2`;
- distribución triangular con moda `0.3` frente a `0.5`;
- reordenamiento logístico sin semilla;
- codificación de filas y columnas de R30 ambigua;
- inconsistencias entre los bloques de la prueba de brechas;
- outputs obsoletos embebidos en el notebook;
- afirmaciones sobre reordenamiento en el coleccionista sin pipeline actual.

Estas cuestiones requieren commits científicos independientes.
