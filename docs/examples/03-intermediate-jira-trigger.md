# Ejercicio 3 — Disparador de Jira idempotente (Intermedio)

## Problema / escenario de ejecución

Jira envía dos webhooks iguales cuando `PAY-88` pasa a `In Progress`. Un worker ve el primer evento tarde y el segundo antes. No se debe abrir dos PRs ni ejecutar dos pipelines completos.

## Inputs

- Eventos con `issueKey`, `transitionId`, timestamp y firma.
- Consulta de estado actual de Jira.
- Registro durable de ejecuciones y PR existentes.

## Outputs esperados

Un `runId` único o una decisión `DUPLICATE/NOT_ELIGIBLE`; auditoría del evento y un único pipeline activo.

## Tu solución propuesta (incompleta)

Completa la clave idempotente y el orden de validaciones:

```text
1. Validar ...
2. Construir clave: ...
3. Consultar ...
4. Si ya ... entonces ...
5. Crear ...
```

## Respuesta correcta esperada

Valida firma/autenticidad, issue/proyecto elegible y transición; consulta el estado actual de Jira porque el evento puede estar atrasado; usa clave durable como `(issueKey, transitionId, workflowVersion)` con restricción única/lock; reclama un lease y crea o reanuda una sola ejecución. Reintentos deben ser idempotentes. Si el ticket ya salió de `In Progress`, no iniciar trabajo nuevo; registrar y reconciliar.
