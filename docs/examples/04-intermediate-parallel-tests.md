# Ejercicio 4 — Tests mientras el coder sigue trabajando (Intermedio)

## Problema / escenario de ejecución

`API-51` agrega un endpoint `GET /reports/{id}`. El coder implementa el endpoint. El agente de pruebas quiere empezar ahora y generar unitarias, integración y funcionales. Ambos agentes comparten el mismo checkout en el diseño inicial.

## Inputs

- Criterios de aceptación y contrato OpenAPI acordado.
- Commit base `abc123`.
- Dos agentes independientes y CI de pruebas.

## Outputs esperados

Tests construidos en paralelo, resultados etiquetados por commit/snapshot, feedback al coder y suite completa sobre candidato integrado.

## Tu solución propuesta (incompleta)

Completa dónde trabaja cada agente y qué evento invalida resultados anteriores:

```text
Coder: ...
Tester: ...
Integración: ...
Repetir tests cuando: ...
```

## Respuesta correcta esperada

El coder escribe implementación en su rama/worktree. El test author crea pruebas desde criterios/contrato en una rama/worktree distinta y no edita archivos del coder. El integrador ejecuta suites sobre un snapshot identificable que combina ambas ramas; los resultados quedan vinculados al hash. Los fallos reproducibles vuelven al coder. Al cambiar el candidato, se invalidan y repiten tests afectados; después de `CODE_COMPLETE`, integrar todo y correr la suite completa. No permitir despliegue a partir de una ejecución parcial/intermedia.
