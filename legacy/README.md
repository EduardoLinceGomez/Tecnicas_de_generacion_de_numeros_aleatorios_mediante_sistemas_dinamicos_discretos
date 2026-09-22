# Material histórico

Este directorio conserva archivos de la implementación temprana para mantener
la trazabilidad de la tesis. No es el punto de entrada público del proyecto.

- `notebooks/` contiene el notebook de exploración original y una libreta de
  Mathematica sobre operadores de transferencia.
- `compat/` conserva adaptadores de la prueba del coleccionista. Delegan en la
  implementación canónica de `src/tesis_generacion/` y no se instalan como API.
- `tests/` conserva la primera suite específica del coleccionista.

Para trabajo nuevo deben usarse `src/`, `scripts/` y `tests/`. Los comandos
actuales están documentados en el README de la raíz.
