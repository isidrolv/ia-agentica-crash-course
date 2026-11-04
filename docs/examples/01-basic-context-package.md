# Ejercicio 1 — Paquete de contexto para una historia (Básico)

## Problema / escenario de ejecución

Un PO crea `SHOP-214`: “Como cliente quiero restablecer mi contraseña”. El agente de contexto debe ayudar al coder a localizar requisitos y puntos de extensión, pero no debe inventar decisiones ni modificar archivos.

## Inputs

- Jira: título, descripción, criterios incompletos, proyecto `SHOP`.
- Base de conocimiento: guía de autenticación y carpetas del frontend/backend.
- Permisos: Jira y repositorio de solo lectura.

## Outputs esperados

Un JSON que contenga `issue_key`, `summary`, `sources[]`, `candidate_paths[]`, `known_requirements[]`, `open_questions[]` y `status` (`READY` o `NEEDS_CLARIFICATION`).

## Tu solución propuesta (incompleta)

```json
{
  "issue_key": "SHOP-214",
  "summary": "...",
  "sources": [],
  "candidate_paths": [],
  "known_requirements": [],
  "open_questions": [],
  "status": "..."
}
```

¿Qué campos faltan para distinguir hechos de inferencias? ¿Qué haces si no encuentras documentación?

<details>
<summary>Respuesta correcta esperada</summary>

Devuelve fuentes con identificador/enlace y fecha, separa requisitos explícitos de inferencias, lista rutas candidatas con razón, y añade preguntas abiertas. Como los criterios están incompletos, responde `NEEDS_CLARIFICATION`; no convierte una inferencia en requisito. Permisos de solo lectura se aplican en la capa de herramientas, no solo en el prompt.

</details>
