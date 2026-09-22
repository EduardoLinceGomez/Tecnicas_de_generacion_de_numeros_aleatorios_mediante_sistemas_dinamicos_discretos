# AUT-097: normalización de figuras de resultados

## Trazabilidad

- Repositorio científico: `Tecnicas_de_generacion_de_numeros_aleatorios_mediante_sistemas_dinamicos_discretos`.
- Rama base: `reestructuracion/repositorio`.
- Commit base aprobado: `de052fa68eb6ebb94fd09a7d087fdc4c813555b8`.
- Rama de trabajo: `feat/aut-097-figuras-resultados`.
- HEAD técnico validado, antes del commit exclusivamente documental de este informe: `68d1b3a3327d995f2fc2136e552b83790ac6ac82`.
- Repositorio de tesis usado sólo como vista previa local: rama `correcciones/MCF`, HEAD inicial y conservado `cd27945c0698aaf0e1f6ccce48532f46dce930be`.

El SHA del commit que contiene este propio informe no se incluye dentro del
archivo para evitar una referencia circular; el HEAD final de entrega queda
registrado en la rama y en el pull request.

## Entorno de referencia

- macOS 26.6.2 (build 25G83).
- Python 3.14.5.
- NumPy 2.4.6.
- SciPy 1.18.0.
- Matplotlib 3.10.9, backend `Agg` en los generadores.
- Pillow 12.2.0.
- latexmk 4.88.
- pdfTeX 1.40.29 (TeX Live 2026).

## Archivos fuente modificados

- `src/tesis_generacion/visualizacion/reordenamiento.py`.
- `src/tesis_generacion/visualizacion/transformadas.py`.
- `tests/test_visualizacion_reordenamiento.py`.
- `tests/test_visualizacion_transformadas.py`.
- `tests/data/reordenamiento_baseline.json`.
- `figuras_tesis/manifest_figuras.csv`.
- Ocho PNG canónicos bajo `figuras_tesis/cientificas/`.

En la vista previa local de la tesis se sustituyeron esos ocho PNG y se aplicó
una única modificación a `capitulos/resultados.tex`: `\raisebox{-2mm}` en el
panel derecho de la Figura 3.13. No se creó ningún commit en la tesis.

## Tipografía y geometría

Las cuatro figuras de brechas dejaron de usar tamaños locales pequeños y ahora
consumen `PERFIL_MEDIO` mediante `PerfilTipografico`:

| Elemento | Antes | Después |
|---|---:|---:|
| Título general | 16 pt | 22 pt (`perfil.titulo`) |
| Título de panel | 13 pt | 14 pt (`perfil.anotacion`) |
| Etiquetas de ejes | 12 pt | 19 pt (`perfil.ejes`) |
| Ticks | 9 pt | 16 pt (`perfil.ticks`) |
| Leyenda | 10 pt | 14 pt (`perfil.leyenda`) |
| Lienzo | 7.4 x 10.4 in | 8.6 x 9.8 in |

La leyenda compartida permanece fuera de los ejes y por encima de los tres
paneles. Se ajustaron los márgenes y la separación vertical para mantener
legibles los títulos de panel sin desperdiciar altura.

Para las parejas de función característica de tienda y logística, tanto la
trayectoria compleja como el error usan un lienzo nominal de 8.2 x 7.0 in. El
alcance fue deliberadamente local: las figuras FGM, las FC de R30 y las figuras
diagnósticas históricas conservan su geometría y sus hashes previos. La
trayectoria compleja conserva `aspect="equal"`.

## PNG canónicos antes y después

| Figura canónica | Antes: píxeles; SHA-256 | Después: píxeles; SHA-256 |
|---|---|---|
| `reordenamiento/Log_PG.png` | 1452 x 2018; `eae19f4f9db85e2988f79414cdb88048cd030eeb1f2b7df2503c411b0083c3da` | 1700 x 1913; `e50fd4e8a2d37845e9b50be2ccd625aea1757350a4336a3ff900d50a42306eef` |
| `reordenamiento/Tent_PG.png` | 1452 x 2018; `a390cf9f1cb936a1caf9d53c03da37985b4f7a1e389783844e72ab99c050aef7` | 1700 x 1913; `72e038ae81959b2757f7d2025942dd5b26f73b7ec2ab69cdb4ecc224512fb6e6` |
| `reordenamiento/R30_col_PG.png` | 1452 x 2018; `907bfeb31c734da532ad660c77dd3de28a054d34f275f45da83bfbdfca0d0080` | 1704 x 1913; `5cbc28c95f9aa301c5fde979d08f69b38e6171ffe601ade616e77e40a48b2e42` |
| `reordenamiento/R30_fila_PG.png` | 1452 x 2018; `208d239d96803c655c9c3a9ff6caf5c028ece0c1d7a6ef06c9b4d92fbe592d78` | 1700 x 1913; `b141e3c14b99c2a0d08e89bab357bdffb33126e381abffb372781983bff3bffe` |
| `transformadas/tienda_fc.png` | 1309 x 1070; `ef4af195001caa4105f9ae2b7029fc4b65032a3365b0d0bdfdb2483fd648e6c5` | 1655 x 1346; `0a9a83cca25ad86818ebd724342b57694ae4cce7e2be63e6bd1cc658b3f24af6` |
| `transformadas/tienda_error_fc.png` | 1567 x 921; `a0b529bae2e93f532b42ef18dc6e58f273e1ab95e2e9b4116f23204fe26f0266` | 1681 x 1420; `6a213e862f5229ab87da0c5f4e77b15b14e05266443f4b24863a171e641f18c8` |
| `transformadas/logistico_fc.png` | 1644 x 1075; `0c16984bea15b4cf511cafe3ab1fcccd63faf5c9cde79feb87036094a3b4e0cf` | 1655 x 1421; `62e3eb9122300891a0a452b7b164b17ffadbc43521f193532ed1540a2d6f99b1` |
| `transformadas/logistico_error_fc.png` | 1972 x 921; `56fc44f20a1b2d760dd81d8243bc8ffb791e3143049ec608660ad5e3feba2ce2` | 1655 x 1424; `57d5c579ece97a118a4e652e749274d61d1e0adfb9f010c19eeb4bee27a4a2fa` |

## Solución de las Figuras 3.13 y 3.20

### Figura 3.13: mapeo tienda

- Los títulos conservan exactamente su redacción y una sola línea:
  `Función característica: mapeo tienda` y
  `Error de la función característica: mapeo tienda`.
- Ambos PNG usan el lienzo 8.2 x 7.0 in.
- El panel complejo conserva aspecto igual.
- La vista previa usa `\raisebox{-2mm}` en el panel derecho para alinear los
  bordes superiores a `width=0.49\textwidth`.

### Figura 3.20: mapeo logístico uniformizado

- Los títulos contienen exactamente un salto de línea:
  `Función característica:\nmapeo logístico uniformizado` y
  `Error de la función característica:\nmapeo logístico uniformizado`.
- Ambos PNG usan el lienzo 8.2 x 7.0 in.
- El panel complejo conserva aspecto igual.
- La geometría Matplotlib fue suficiente; el ajuste LaTeX es 0 mm y no se
  añadió `\raisebox`.

## Control de cambios colaterales

La regeneración de reordenamiento también cambia, como duplicados byte a byte,
`brechas_antes_despues_logistico.png`,
`brechas_antes_despues_tienda.png`,
`brechas_antes_despues_r30_columnas.png` y
`brechas_antes_despues_r30_filas.png` dentro de `outputs/reordenamiento/`. Sus
hashes estrictos se actualizaron junto con los cuatro alias de tesis en el
baseline. No se promovieron como canónicos adicionales.

No cambió ningún otro PNG canónico de transformadas: las cuatro FGM, las cuatro
figuras de R30 y las dos figuras diagnósticas históricas permanecieron
idénticas. `tests/data/transformadas_baseline.json` no necesitó modificación.

## Invariancia científica

Antes de promover los PNG se comparó la regeneración contra una instantánea
externa tomada en el commit base. Los resultados fueron:

- `resumen_reordenamiento.csv`: idéntico byte a byte.
- `resumen_brechas_reordenamiento.csv`: idéntico byte a byte.
- `resumen_transformadas.csv`: idéntico byte a byte.
- 67 comprobaciones estructuradas de parámetros, fingerprints, ACF, soportes y
  métricas de brechas: 67 coincidentes.
- 7 comprobaciones estructuradas de mallas, muestras, fingerprints y métricas
  de transformadas: 7 coincidentes.
- Intervalos, `p=0.2`, PMF, soportes, datos, `D_max`, EAM, colores y marcadores
  no cambiaron.

## Pruebas y regeneración

- Pruebas focalizadas estrictas con
  `VERIFICAR_PNG_REORDENAMIENTO=1 VERIFICAR_PNG_EXACTO=1`: 9/9.
- `python3 -m unittest -v`: 8/8.
- `python3 -m unittest discover -s tests -p 'test_*.py' -v`: 138/138,
  con 6 omisiones esperadas de baselines gráficos ajenos al alcance.
- `python3 scripts/regenerar_reordenamiento.py --output-dir outputs/reordenamiento`: correcto.
- `python3 scripts/regenerar_transformadas.py --output-dir outputs/transformadas`: correcto.
- `python3 scripts/verificar_figuras_tesis.py`: 65 entradas, 0 errores.
- `git diff --check`: correcto.

Las pruebas nuevas verifican el perfil tipográfico compartido, la leyenda fuera
de los ejes, márgenes sin recorte, generación de los cuatro PNG de brechas,
títulos exactos, un único salto de línea logístico, ausencia de salto en tienda
y conservación de `aspect="equal"`.

## Vista previa de la tesis

La tesis se compiló con:

```text
latexmk -pdf -interaction=nonstopmode -file-line-error Main.tex
```

Resultado:

- `Main.pdf`: 112 páginas, tamaño carta, SHA-256
  `268482c5b4d62790fddb0148affa5b31ab8ae36c559a4940e3c0b5bad3d3261b`.
- Sin referencias ni citas indefinidas.
- Los dos avisos `Overfull` existentes corresponden a texto de
  `marco_teorico.tex` y a un párrafo previo de `resultados.tex`; no se originan
  en las figuras AUT-097.
- Inspección renderizada a 180 dpi de las páginas físicas 88, 93, 94, 98 y 100,
  correspondientes a las Figuras 3.8, 3.13, 3.15, 3.20 y 3.22.
- No se observaron recortes, solapamientos ni etiquetas ilegibles. Los paneles
  de 3.13 y 3.20 quedan alineados a tamaño normal de página.

La revisión visual descrita es técnica. La aprobación visual humana final sigue
correspondiendo al autor. Los ocho PNG candidatos, la línea de `resultados.tex`
y el `Main.pdf` ignorado quedan localmente en la tesis para esa revisión; no se
creó commit, push ni pull request en ese repositorio.
