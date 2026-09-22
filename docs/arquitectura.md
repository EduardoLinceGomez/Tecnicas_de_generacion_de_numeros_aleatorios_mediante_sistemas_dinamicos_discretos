# Arquitectura del repositorio

El pipeline separa cálculo, presentación y promoción canónica:

```text
generadores
    ↓
transformaciones
    ↓
experimentos ──→ estadística
    ↓               ↓
visualización ──────┘
    ↓
scripts → outputs/ → revisión → figuras_tesis/
```

## Capas

### Generadores

`src/tesis_generacion/generadores/` implementa el mapeo logístico, el mapeo
tienda, regla 30 y Park–Miller MINSTD. Son funciones pequeñas sin salida gráfica.

### Transformaciones

`src/tesis_generacion/transformaciones/` contiene uniformización beta,
codificación decimal, codificación binaria y reordenamiento. No fija rutas ni
escribe resultados.

### Experimentos

`src/tesis_generacion/experimentos/` construye las muestras canónicas y combina
los generadores con parámetros versionados. `parametros.py` es la referencia
central para semillas, tamaños e intervalos.

### Estadística

`src/tesis_generacion/estadistica/` calcula momentos, transformadas,
autocorrelación, brechas, invariancia y coleccionista. Esta capa devuelve datos
y métricas; no decide cómo dibujarlos.

### Visualización

`src/tesis_generacion/visualizacion/` transforma resultados en figuras, CSV y
reportes. Los módulos aceptan un directorio de salida y sólo copian referencias
cuando el llamador solicita explícitamente esa operación.

### Scripts y orquestación

Cada `scripts/regenerar_*.py` es un adaptador CLI del módulo correspondiente.
`scripts/reproducir_tesis.py` compone esos comandos sin duplicar lógica
científica. `scripts/verificar_figuras_tesis.py` valida el manifiesto y,
opcionalmente, el repositorio privado del manuscrito.

## Directorios de resultados

- `outputs/`: resultados locales regenerados, ignorados por Git y reemplazables;
- `graficas_auxiliares/`: diagnósticos científicos versionados, no
  necesariamente usados en la tesis;
- `figuras_tesis/`: copias canónicas aprobadas y su manifiesto;
- `tests/data/`: contratos numéricos y gráficos usados por la suite.

La transición `outputs/ → figuras_tesis/` nunca es automática. Requiere
validación científica, revisión visual y una acción explícita de promoción.

## Compatibilidad histórica

`legacy/` conserva notebooks, adaptadores y pruebas tempranas. Esos archivos
sirven para trazabilidad y para demostrar equivalencia con la implementación
modular, pero no son entrypoints públicos ni se instalan como parte del paquete.
