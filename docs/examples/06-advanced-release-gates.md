# Ejercicio 6 — Review no equivale a despliegue (Avanzado)

## Problema / escenario de ejecución

El reviewer del PR `INV-303` devuelve PASS. Sin embargo, las pruebas de integración están pendientes y el análisis de dependencias detecta una vulnerabilidad crítica. El release agent recibió instrucciones del coder para desplegar inmediatamente.

## Inputs

- Veredicto review `PASS`.
- CI: pruebas de integración pendientes; dependencia crítica.
- Artefacto construido con digest conocido.
- Política: no desplegar si hay gate crítico fallido; producción requiere aprobación humana.

## Outputs esperados

Transición bloqueada, reporte accionable, sin despliegue; reanudación solo sobre candidato actualizado y validado.

## Tu solución propuesta (incompleta)

Completa la política de decisión:

```text
Si review == PASS y ... entonces ...
Si gate crítico falla ...
Después de corregir ...
Para producción ...
```

## Respuesta correcta esperada

Review PASS es una condición necesaria pero no suficiente. El controlador determinista espera que todas las puertas requeridas terminen y pasen; vulnerabilidad crítica bloquea y crea un hallazgo/escala. El coder corrige en una nueva revisión, se regeneran artefacto y evidencias, y los gates se repiten vinculados al digest final. Solo se promueve el mismo artefacto validado; producción exige aprobación según política y despliegue progresivo con health checks y rollback. Un prompt del coder nunca cambia estas reglas.
