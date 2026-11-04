# Ejercicio 2 — Convertir una historia en criterios comprobables (Básico)

## Problema / escenario de ejecución

Historia: “Como usuario quiero que la página de pedidos cargue rápido”. El agente de especificación debe preparar preguntas y una propuesta sin inventar el SLA.

## Inputs

- Objetivo de negocio: reducir abandono.
- No se especifica dispositivo, tamaño de datos, percentil ni límite de latencia.

## Outputs esperados

Lista de criterios Given/When/Then, preguntas para el PO y estado listo/bloqueado.

## Tu solución propuesta (incompleta)

Completa al menos dos escenarios y anota qué métrica no se puede asumir:

```text
Given ...
When ...
Then ...

Preguntas abiertas: ...
Estado: ...
```

## Respuesta correcta esperada

No fijes arbitrariamente un SLA como “menos de 1 s”. Pide confirmar población, dispositivo/red, volumen de pedidos, métrica (p. ej. p95), ventana de medición y umbral. Sí pueden proponerse criterios funcionales verificables como mostrar pedidos autorizados, estado vacío y error de carga/reintento; marca la historia `NEEDS_CLARIFICATION` para el requisito cuantitativo y deja trazabilidad al PO.
