# Metodología comparable para la prueba de brechas

## Estado

- **Fecha de decisión:** 2026-09-21.
- **Estado:** **IMPLEMENTADO** en el repositorio científico.
- **Rama base actualizada:** \`reestructuracion/repositorio\` en
  \`363bef1a8fc694e40ccab8e0625c166775f14c9c\`.
- **Rama de trabajo:** \`feat/brechas-comparables\`.
- **Commit científico principal:**
  \`3099b0630fb3eca42a18f7c5eaabe3874c4857b6\`.
- **Documento relacionado en la tesis:** AUT-065 en \`EduardoLinceGomez/tesis-generacion-numeros\`.
- **Alcance completado:** se reemplazó el uso activo de intervalos distintos por
  generador por un protocolo común y reproducible. El repositorio de la tesis no
  se modificó; su prosa y sus copias de figuras siguen pendientes de un handoff
  posterior.

## Registro de implementación

El protocolo final usa los intervalos abiertos
\(I_1=(0.1,0.3)\), \(I_2=(0.4,0.6)\) e \(I_3=(0.7,0.9)\), todos
con longitud y probabilidad teórica \(p=0.2\), y conserva la convención
\(W=G+1\). La constante pública se normaliza a \`0.2\` después de verificar
numéricamente \(\beta-\alpha\), para evitar serializar
\`0.19999999999999998\`; el cálculo matemático de brechas no se alteró.

Los archivos principales modificados fueron:

- \`src/tesis_generacion/experimentos/parametros.py\`;
- los experimentos y visualizaciones de \`reordenamiento\` y
  \`comparacion_generadores\`;
- las seis pruebas de experimento, visualización y CLI, además de la prueba
  estadística de terminología;
- los dos baselines JSON;
- los CSV y PNG reproducibles;
- las cuatro figuras canónicas FIG-054 a FIG-057 y su manifest.

### Estructura final materializada

El resumen de reordenamiento serializa los intervalos una sola vez en
\`parametros["intervalos_brechas_comunes"]\`. Cada muestra conserva la
dimensión explícita
\`muestras[nombre]["brechas"][intervalo_id]["original"/"reordenada"]\`.
El resumen comparativo usa los mismos parámetros globales y la dimensión
\`muestras[nombre]["brechas"][intervalo_id]\` sólo para la muestra original.

Las salidas versionadas son:

- \`graficas_auxiliares/reordenamiento/resumen_reordenamiento.csv\`, con las
  cuatro filas de métricas independientes del intervalo;
- \`graficas_auxiliares/reordenamiento/resumen_brechas_reordenamiento.csv\`,
  con 12 filas muestra por intervalo;
- \`graficas_auxiliares/comparacion_generadores/resumen_comparacion.csv\`, cuyo
  contenido científico previo se conserva;
- \`graficas_auxiliares/comparacion_generadores/resumen_brechas_comparacion.csv\`,
  con 15 filas generador por intervalo;
- cuatro PNG auxiliares y sus cuatro copias canónicas FIG-054 a FIG-057, cada
  uno con tres paneles, más \`brechas_comparacion_i1.png\`,
  \`brechas_comparacion_i2.png\` y \`brechas_comparacion_i3.png\`;
- \`tests/data/reordenamiento_baseline.json\` y
  \`tests/data/comparacion_generadores_baseline.json\`, regenerados desde el
  cálculo.

Se generaron 24 resúmenes de reordenamiento y 15 resúmenes de muestras
originales. Los CSV largos contienen respectivamente 12 y 15 filas. Las
figuras PG usan tres paneles verticales para mantener la legibilidad; las tres
figuras comparativas usan cinco paneles cada una. No se introdujo promedio,
puntuación ni clasificación global.

Los comandos de regeneración y validación ejecutados fueron:

\`\`\`bash
python3 scripts/regenerar_reordenamiento.py \
  --output-dir outputs/reordenamiento \
  --reference-dir graficas_auxiliares/reordenamiento
python3 scripts/regenerar_comparacion_generadores.py \
  --output-dir outputs/comparacion_generadores \
  --reference-dir graficas_auxiliares/comparacion_generadores
python3 -m unittest -v
python3 -m unittest discover -s tests -p 'test_*.py' -v
VERIFICAR_PNG_REORDENAMIENTO=1 VERIFICAR_PNG_COMPARACION=1 \
  MPLBACKEND=Agg python3 -m unittest -v \
  tests.test_visualizacion_reordenamiento \
  tests.test_visualizacion_comparacion_generadores
python3 scripts/verificar_figuras_tesis.py
git diff --check
\`\`\`

Resultados: 8/8 pruebas en la suite raíz; 129 pruebas descubiertas bajo
\`tests\`, de las cuales 123 pasaron y 6 verificaciones gráficas opcionales se
omitieron por defecto; 6/6 verificaciones PNG estrictas al activarlas; y 65
entradas válidas en el manifest. Una comparación exacta contra el baseline de
\`363bef1a8fc694e40ccab8e0625c166775f14c9c\` confirmó que fingerprints,
permutaciones, condiciones iniciales, semillas, ACF y las demás métricas de
comparación no cambiaron. Los PNG de ACF y \`permutacion_indices.png\`
permanecen sin cambios versionados.

La única desviación de disposición respecto de la preferencia inicial fue usar
tres paneles verticales en las figuras PG: la primera composición mostró
solapamientos de leyenda y fue corregida antes de aprobar visualmente y
actualizar los hashes. No hubo desviaciones científicas.

## 1. Problema metodológico

Antes de esta corrección, el bloque reproducible de reordenamiento usaba un
único intervalo de brechas distinto para cada muestra:

- logístico transformado: \((0.2,0.5)\), con \(p=0.3\);
- tienda: \((0.7,0.9)\), con \(p=0.2\);
- regla 30 por columnas: \((0.1,0.3)\), con \(p=0.2\);
- regla 30 por filas: \((0.7,1.0)\), con \(p=0.3\).

La comparación original frente a reordenada **dentro de una misma muestra**
sigue siendo válida porque ambas versiones usan el mismo intervalo. Sin
embargo, los resultados de brechas no constituyen un diagnóstico homogéneo
entre generadores, porque cambian simultáneamente:

1. la posición del intervalo;
2. en dos casos, su longitud;
3. la probabilidad teórica de éxito \(p=\beta-\alpha\);
4. la distribución geométrica de referencia.

La implementación histórica reconocía esta limitación en el capítulo de
Resultados y evitaba usar la prueba de brechas para una clasificación global.
La decisión aprobada fue corregir el diseño experimental en vez de conservar
esa restricción.

## 2. Metodología aprobada

Todos los generadores se evaluarán con los mismos tres intervalos abiertos:

\[
I_1=(0.1,0.3),\qquad
I_2=(0.4,0.6),\qquad
I_3=(0.7,0.9).
\]

Los tres tienen longitud

\[
|I_j|=0.2,
\]

por lo que bajo el modelo de referencia
\(U\sim\operatorname{Uniforme}(0,1)\),

\[
p=\mathbb P(U\in I_j)=0.2
\]

en los tres casos. Con la convención vigente \(W=G+1\), la misma ley teórica
se usa en todos los experimentos:

\[
\mathbb P(W=w)=0.2(0.8)^{w-1},
\qquad w=1,2,\dots,
\]

y

\[
F(w)=1-0.8^w.
\]

La elección de tres intervalos, en lugar de uno solo, reduce la dependencia de
las conclusiones respecto de una posición particular dentro de \([0,1]\). Los
intervalos exploran una región izquierda, una central y una derecha con la
misma probabilidad teórica.

### Convención que se conserva

Los intervalos continúan siendo **abiertos**. Un valor es éxito si

\[
\alpha < x_i < \beta.
\]

No cambiar esta convención durante la implementación.

## 3. Matriz experimental

### 3.1 Reordenamiento

Aplicar los tres intervalos a cada una de las cuatro muestras canónicas:

- logístico transformado;
- tienda;
- regla 30 por columnas;
- regla 30 por filas.

Para cada muestra se evalúan:

- la versión original;
- la versión reordenada;
- \(I_1\);
- \(I_2\);
- \(I_3\).

Por tanto, el bloque de brechas debe producir

\[
4\ \text{muestras}
\times
2\ \text{órdenes}
\times
3\ \text{intervalos}
=
24
\]

resúmenes de brechas.

La ACF, las permutaciones, las muestras y los fingerprints no cambian.

### 3.2 Comparación homogénea de generadores

El repositorio contiene además un bloque
\`comparacion_generadores\` con las cuatro muestras dinámicas y el benchmark
Park--Miller MINSTD.

Una vez adoptado el protocolo común, la prueba de brechas puede incorporarse
también a esta comparación homogénea. En ese bloque deben usarse las cinco
**muestras originales**:

- logístico transformado;
- tienda;
- R30 columnas;
- R30 filas;
- MINSTD.

Cada una se evalúa con \(I_1,I_2,I_3\), sin reordenar MINSTD. Esto produce

\[
5\times3=15
\]

resúmenes comparables adicionales.

El propósito de este bloque es comparar generadores originales bajo el mismo
protocolo. El análisis de reordenamiento sigue siendo un experimento separado.

## 4. Parámetros compartidos

La definición de los intervalos no debe permanecer dentro de
\`experimentos/reordenamiento.py\`, porque también será utilizada por
\`comparacion_generadores.py\`.

Centralizarla en:

\`src/tesis_generacion/experimentos/parametros.py\`.

La especificación recomendada es una estructura ordenada y con identificadores
estables, por ejemplo:

\`\`\`python
INTERVALOS_BRECHAS_COMUNES = {
    "i1": (0.1, 0.3),
    "i2": (0.4, 0.6),
    "i3": (0.7, 0.9),
}
\`\`\`

Los identificadores deben ser estables porque aparecerán en JSON, CSV,
baselines y nombres de archivos auxiliares si fuese necesario.

La implementación debe validar que:

- existen exactamente tres intervalos;
- cada intervalo satisface \(0\leq\alpha<\beta\leq1\);
- todos tienen la misma longitud;
- la longitud común es exactamente \(0.2\) dentro de la tolerancia numérica
  apropiada;
- la probabilidad teórica usada por \`resumen_brechas\` es \(p=0.2\).

No mantener simultáneamente un diccionario activo de intervalos históricos por
muestra. Los intervalos antiguos quedan preservados por el historial de Git y
por este documento, no como parámetros activos de la nueva metodología.

## 5. Cambios requeridos en el experimento de reordenamiento

Archivo principal:

\`src/tesis_generacion/experimentos/reordenamiento.py\`.

### 5.1 Eliminar el parámetro por muestra

Retirar el uso activo de:

\`\`\`python
INTERVALOS_BRECHAS = {
    "logistico": (0.2, 0.5),
    "tienda": (0.7, 0.9),
    "r30_columnas": (0.1, 0.3),
    "r30_filas": (0.7, 1.0),
}
\`\`\`

e importar \`INTERVALOS_BRECHAS_COMUNES\` desde
\`experimentos.parametros\`.

### 5.2 Estructura del resultado

No debe existir ya un único
\`intervalo_brechas\`, \`brechas_original\` y \`brechas_reordenada\` por
muestra.

Cada muestra debe contener una colección explícita, por ejemplo:

\`\`\`python
"brechas": {
    "i1": {
        "intervalo": [0.1, 0.3],
        "original": resumen_brechas(...),
        "reordenada": resumen_brechas(...),
    },
    "i2": {
        "intervalo": [0.4, 0.6],
        "original": resumen_brechas(...),
        "reordenada": resumen_brechas(...),
    },
    "i3": {
        "intervalo": [0.7, 0.9],
        "original": resumen_brechas(...),
        "reordenada": resumen_brechas(...),
    },
}
\`\`\`

El nombre concreto de las claves internas puede ajustarse al estilo del
repositorio, pero la estructura debe conservar inequívocamente las dimensiones
**muestra × intervalo × original/reordenada**.

### 5.3 Parámetros serializados

El resumen JSON debe reportar los intervalos una sola vez como parámetro común,
no como una asignación distinta por generador. Debe quedar explícito:

- los tres intervalos;
- su longitud común;
- \(p=0.2\);
- que se aplican a todas las muestras.

### 5.4 Invariantes que no deben cambiar

La implementación nueva no autoriza modificar:

- las cuatro muestras canónicas;
- sus fingerprints;
- \(n=1000\);
- las dos órbitas auxiliares del reordenamiento;
- sus condiciones iniciales;
- la semilla 2024;
- las permutaciones;
- los fingerprints de las permutaciones;
- la ACF en separaciones 1 a 20;
- la conservación del multiconjunto;
- la implementación matemática de \`resumen_brechas\`, salvo ajustes
  estrictamente necesarios para exponer mejor los resultados.

Los valores de ACF antes y después deben ser idénticos a los del baseline
vigente.

## 6. Estadística de brechas que debe conservarse

Para cada combinación muestra/orden/intervalo conservar como mínimo:

- \(\alpha\);
- \(\beta\);
- \(p=0.2\);
- número de tiempos de espera completos;
- longitud de la racha final incompleta;
- media de \(W\);
- máximo observado de \(W\);
- \(D_{\max}\), diferencia máxima entre CDF empírica y teórica;
- EAM de las diferencias de CDF.

La función de bajo nivel
\`src/tesis_generacion/estadistica/dependencia_serial.py\`
ya implementa la convención matemática necesaria. No reescribir el algoritmo
de \`tiempos_espera_brechas\` ni \`resumen_brechas\` sin una razón científica
independiente.

### Terminología pública

La tesis ya adoptó **racha final incompleta** en lugar de «cola censurada».

Aunque se conserve una clave interna histórica por compatibilidad, los CSV,
README, figuras y prosa nuevos deben usar la expresión:

\`racha_final_incompleta\`

o su equivalente legible en español, y no presentar la última racha como
censura estadística.

## 7. CSV del bloque de reordenamiento

Antes de la corrección, el archivo
\`graficas_auxiliares/reordenamiento/resumen_reordenamiento.csv\`
tenía una sola fila por muestra y mezclaba métricas de ACF con el único
intervalo histórico de brechas.

La nueva metodología necesita una dimensión adicional.

### Diseño recomendado

Mantener:

\`resumen_reordenamiento.csv\`

para las cantidades que no dependen del intervalo:

- muestra;
- \(n\);
- método de reordenamiento;
- fingerprints;
- métricas ACF original/reordenada.

Crear:

\`resumen_brechas_reordenamiento.csv\`

en formato largo, con **12 filas**:

\[
4\ \text{muestras}\times3\ \text{intervalos}.
\]

Campos mínimos:

- \`muestra\`;
- \`intervalo_id\`;
- \`alpha\`;
- \`beta\`;
- \`p\`;
- \`brechas_original\`;
- \`brechas_reordenada\`;
- \`racha_final_incompleta_original\`;
- \`racha_final_incompleta_reordenada\`;
- \`media_w_original\`;
- \`media_w_reordenada\`;
- \`max_w_original\`;
- \`max_w_reordenada\`;
- \`dmax_original\`;
- \`dmax_reordenada\`;
- \`mae_original\`;
- \`mae_reordenada\`.

Dentro de cada fila, el número de éxitos/tiempos completos de la muestra
original y de su permutación debe coincidir porque reordenar no altera qué
valores pertenecen al intervalo.

No calcular una puntuación agregada única a partir de los tres intervalos en
esta fase. Deben preservarse los resultados por intervalo para que no se
oculten diferencias regionales.

## 8. Figuras del bloque de reordenamiento

Archivo:

\`src/tesis_generacion/visualizacion/reordenamiento.py\`.

La implementación histórica generaba una figura de brechas por muestra y la
copiaba a los nombres usados por la tesis.

### Requisito

Conservar los cuatro nombres canónicos de la tesis:

- \`Log_PG.png\`;
- \`Tent_PG.png\`;
- \`R30_col_PG.png\`;
- \`R30_fila_PG.png\`.

Cada archivo debe pasar a mostrar **los tres intervalos comunes**. La solución
preferida es una figura compuesta con tres paneles, uno por intervalo.

Cada panel debe incluir:

- PMF empírica original;
- PMF empírica reordenada;
- PMF geométrica teórica con \(p=0.2\);
- identificación visible del intervalo correspondiente.

La misma referencia teórica debe aparecer en los tres paneles.

La disposición concreta puede ajustarse durante la inspección visual. Debe
priorizarse legibilidad cuando la figura se inserta en la tesis. Si un arreglo
horizontal resulta ilegible al ancho usado por LaTeX, usar tres paneles
verticales.

Los archivos auxiliares
\`brechas_antes_despues_<muestra>.png\`
pueden conservar sus nombres y convertirse también en las figuras compuestas,
de modo que no sea necesario multiplicar innecesariamente los PNG.

No cambiar las figuras ACF ni
\`permutacion_indices.png\`.

## 9. Comparación homogénea con MINSTD

Archivos:

- \`src/tesis_generacion/experimentos/comparacion_generadores.py\`;
- \`src/tesis_generacion/visualizacion/comparacion_generadores.py\`;
- \`graficas_auxiliares/comparacion_generadores/README.md\`;
- \`graficas_auxiliares/comparacion_generadores/resumen_comparacion.csv\`.

### 9.1 Experimento

Agregar a cada muestra original una colección \`brechas\` calculada con los
mismos \(I_1,I_2,I_3\).

Los parámetros del resumen deben registrar
\`intervalos_brechas_comunes\` y \(p=0.2\).

No usar muestras reordenadas en este bloque.

### 9.2 Salida tabular

Mantener \`resumen_comparacion.csv\` para las métricas que ya contiene.

Agregar un archivo separado:

\`resumen_brechas_comparacion.csv\`

con **15 filas**:

\[
5\ \text{generadores}\times3\ \text{intervalos}.
\]

Debe usar los mismos campos descriptivos de brechas que correspondan a una
sola muestra original.

### 9.3 Figuras comparativas

Generar tres figuras comparativas, una por intervalo:

- \`brechas_comparacion_i1.png\`;
- \`brechas_comparacion_i2.png\`;
- \`brechas_comparacion_i3.png\`.

Cada figura debe usar el mismo intervalo en sus cinco paneles, uno por
generador, y la misma geométrica teórica \(p=0.2\).

Esto permite inspeccionar visualmente una comparación realmente homogénea.

No producir una clasificación automática ni una puntuación total de
generadores.

## 10. Baselines y pruebas

### 10.1 \`tests/data/reordenamiento_baseline.json\`

Actualizar el baseline para representar los tres intervalos.

Deben permanecer exactamente iguales:

- fingerprints de muestras;
- fingerprints de permutaciones;
- estados iniciales y semillas;
- primeros y últimos índices de las permutaciones;
- métricas ACF.

Deben cambiar:

- parámetros de intervalos;
- métricas de brechas;
- hashes de las cuatro figuras de brechas;
- hashes de las copias canónicas de esas figuras.

La estructura de \`muestras\` debe almacenar las métricas de brechas por
intervalo, no un único vector por muestra.

### 10.2 \`tests/test_experimentos_reordenamiento.py\`

Añadir verificaciones de que:

1. los tres intervalos comunes son exactamente los aprobados;
2. los tres tienen longitud \(0.2\);
3. cada muestra posee resultados para exactamente \`i1\`, \`i2\`, \`i3\`;
4. cada resumen usa \(p=0.2\);
5. para cada muestra e intervalo, original y reordenada tienen el mismo número
   de tiempos completos;
6. las 24 combinaciones coinciden con el nuevo baseline;
7. ACF, fingerprints y permutaciones no cambian.

### 10.3 Pruebas visuales y CLI de reordenamiento

Actualizar:

- \`tests/test_visualizacion_reordenamiento.py\`;
- \`tests/test_cli_reordenamiento.py\`.

Deben comprobar:

- los CSV esperados;
- los parámetros comunes serializados;
- los archivos de salida;
- los nuevos hashes gráficos en el entorno baseline;
- que no reaparezca una asignación de intervalos distinta por generador.

### 10.4 Comparación de generadores

Actualizar:

- \`tests/data/comparacion_generadores_baseline.json\`;
- \`tests/test_experimentos_comparacion_generadores.py\`;
- \`tests/test_visualizacion_comparacion_generadores.py\`;
- \`tests/test_cli_comparacion_generadores.py\`.

El baseline debe incluir los 15 resúmenes de brechas originales.

Las métricas actualmente existentes de CDF, momentos, FGM, función
característica y ACF deben permanecer sin cambios.

## 11. Referencias gráficas canónicas de la tesis

Las figuras del bloque están registradas en
\`figuras_tesis/manifest_figuras.csv\`, en particular FIG-054 a FIG-057.

Después de regenerar y aprobar visualmente las nuevas figuras:

1. copiar explícitamente las cuatro nuevas figuras compuestas a
   \`figuras_tesis/cientificas/reordenamiento/\`;
2. actualizar sus SHA-256 en \`manifest_figuras.csv\`;
3. ejecutar
   \`python3 scripts/verificar_figuras_tesis.py\`;
4. copiar/verificar contra el repositorio de la tesis con
   \`python3 scripts/verificar_figuras_tesis.py --tesis-root "/ruta/a/Tesis UNAM"\`;
5. sólo después actualizar las copias que usa LaTeX.

No actualizar hashes antes de aprobar visualmente la nueva disposición.

## 12. Cambios posteriores necesarios en la tesis

La implementación científica ya se completó. La sustitución de cifras en la
prosa de la tesis sigue siendo una fase posterior y separada.

Una vez generados y validados los nuevos resultados, el repositorio de la tesis
deberá actualizar al menos:

### Diseño de los experimentos

Reemplazar la asignación histórica de un intervalo diferente a cada muestra por
la metodología común:

\[
(0.1,0.3),\quad(0.4,0.6),\quad(0.7,0.9),
\]

todos con \(p=0.2\).

### Resultados locales

Recalcular y sustituir las cifras de brechas en:

- regla 30;
- mapeo tienda;
- mapeo logístico.

No conservar números obtenidos con los intervalos históricos.

### Tabla de reordenamiento

La tabla actual que contiene un solo intervalo por muestra debe rediseñarse
para mostrar los tres intervalos. Puede usarse una fila por muestra e intervalo
o tres bloques de cuatro filas.

No promediar los tres intervalos como única cifra principal.

### Comparación de generadores

Eliminar la justificación vigente de que la prueba de brechas se excluye de la
comparación porque los intervalos son distintos.

La nueva comparación puede incorporar las métricas de brechas bajo el protocolo
común. Si se presenta MINSTD en esa sección, debe utilizar los mismos tres
intervalos.

### Figuras y pies

Actualizar los pies de \`fig:PG_log\`, \`fig:PG_tent\` y las figuras de R30
para describir los tres paneles y la referencia geométrica común con \(p=0.2\).

## 13. Trazabilidad de los resultados históricos

Los valores actualmente publicados en
\`graficas_auxiliares/reordenamiento/resumen_reordenamiento.csv\`
corresponden al diseño histórico de intervalos distintos.

No deben mezclarse con los nuevos resultados.

El commit anterior permanece como trazabilidad histórica. La nueva
implementación quedó identificada por el commit científico
\`3099b0630fb3eca42a18f7c5eaabe3874c4857b6\` y los baselines y referencias se
regeneraron desde el cálculo bajo la metodología aprobada.

No modificar manualmente cifras del CSV o del JSON para hacer pasar pruebas.

## 14. Orden ejecutado de implementación

1. Centralizar \`INTERVALOS_BRECHAS_COMUNES\`.
2. Adaptar \`construir_experimentos_reordenamiento\`.
3. Ejecutar pruebas numéricas preliminares y revisar los 24 resúmenes.
4. Adaptar CSV y figuras de reordenamiento.
5. Actualizar baseline y pruebas del bloque de reordenamiento.
6. Integrar los intervalos comunes en \`comparacion_generadores\`, incluyendo
   MINSTD sólo como muestra original.
7. Generar CSV y figuras comparativas de brechas.
8. Actualizar baseline y pruebas del bloque comparativo.
9. Ejecutar toda la suite.
10. Regenerar referencias auxiliares.
11. Inspeccionar visualmente los cuatro PNG canónicos de reordenamiento y las
    tres figuras comparativas.
12. Actualizar \`figuras_tesis/manifest_figuras.csv\` y verificar hashes.
13. Dejar pendiente, fuera de este repositorio, la copia de figuras a la tesis.
14. Dejar pendiente la actualización de números, tablas, pies y prosa.
15. Dejar pendiente la compilación y revisión visual de la tesis.

## 15. Comandos de validación ejecutados

La implementación terminó con:

\`\`\`bash
python3 -m unittest -v
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/regenerar_reordenamiento.py \
  --output-dir outputs/reordenamiento \
  --reference-dir graficas_auxiliares/reordenamiento
python3 scripts/regenerar_comparacion_generadores.py \
  --output-dir outputs/comparacion_generadores \
  --reference-dir graficas_auxiliares/comparacion_generadores
python3 scripts/verificar_figuras_tesis.py
\`\`\`

En el entorno gráfico baseline deben ejecutarse además las verificaciones
estrictas de PNG que ya tenga configuradas cada bloque.

## 16. Criterios de aceptación científicos

La implementación científica quedó completa porque:

- [x] los cuatro generadores dinámicos usan exactamente los mismos tres
      intervalos en el bloque de reordenamiento;
- [x] las versiones original y reordenada usan el mismo intervalo en cada
      comparación;
- [x] los tres intervalos tienen \(p=0.2\);
- [x] existen 24 resúmenes reproducibles de brechas para reordenamiento;
- [x] ACF, muestras, fingerprints y permutaciones permanecen inalterados;
- [x] el CSV de brechas de reordenamiento contiene 12 filas;
- [x] las cuatro figuras PG canónicas muestran los tres intervalos;
- [x] la comparación homogénea original incluye los mismos tres intervalos para
      las cinco muestras, incluido MINSTD;
- [x] existen 15 resúmenes de brechas para la comparación original;
- [x] no se produce una puntuación agregada ni una clasificación automática;
- [x] los baselines se regeneraron a partir del cálculo, no mediante edición
      manual de cifras;
- [x] la suite completa pasa;
- [x] las nuevas figuras se revisaron visualmente antes de actualizar hashes;
- [ ] la tesis deja de presentar cifras derivadas de intervalos históricos
      distintos.

## 17. No objetivos

Esta corrección no autoriza:

- cambiar las muestras canónicas;
- cambiar \(n=1000\);
- modificar las permutaciones;
- modificar la ACF;
- elegir intervalos diferentes según el generador;
- seleccionar a posteriori el intervalo que favorezca a cada método;
- agregar una puntuación global de calidad;
- interpretar una buena prueba de brechas como demostración de independencia.

La finalidad es hacer **comparable** el diagnóstico, no convertirlo en una
prueba exhaustiva de independencia.
