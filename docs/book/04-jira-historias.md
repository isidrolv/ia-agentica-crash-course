# Semana 4 — Historias de usuario, criterios y Jira

**Tiempo sugerido:** 8–10 horas. **Resultado:** esquema de historia y reglas explícitas para que solo tickets preparados activen el pipeline.

## Recuperación antes de aprender

¿Qué información necesita el codificador además de un título? ¿Qué puede significar `In Progress` en un workflow? ¿Por qué una historia Jira es entrada no confiable aunque venga de un empleado?

## Historias pequeñas y requisitos comprobables

Una historia describe una necesidad y el valor, no prescribe toda la implementación. Un formato frecuente es: “Como [persona], quiero [capacidad] para [beneficio]”. Los criterios de aceptación hacen observable el resultado. `SHOP-214: como cliente quiero recuperar mi acceso` es insuficiente para implementar el flujo de seguridad: hacen falta reglas de expiración, respuesta ante cuenta inexistente, límites de reintentos y comportamiento móvil/web.

Usa escenarios **Given/When/Then** (Dado/Cuando/Entonces) para describir estado inicial, acción y resultado. Evita criterios vagos (“debe ser rápido”, “debe funcionar correctamente”) hasta aclarar cómo se miden. Cada criterio debería mapearse a pruebas, aunque no todas las decisiones de implementación pertenezcan al PO.

Una buena historia debe ser acotada, estimable, negociable y comprobable; estos atributos ayudan, pero no constituyen un test automático de calidad. Si hay dependencia grande, divide por resultados verticales sin perder comportamiento verificable.

## Estado Jira no es autorización suficiente

Los estados y transiciones son configurables por proyecto. `In Progress` puede activarse por una transición manual, una regla automatizada o una importación. El pipeline debe consultar estado actual y metadatos; no asumir que el nombre del estado implica que el ticket está listo para agentes. Define una regla de elegibilidad, por ejemplo:

```text
project == SHOP
AND issueType in {Story, Bug}
AND labels contains "agent-ready"
AND acceptanceCriteria is not empty
AND currentStatus == "In Progress"
AND risk != "production-data-change"
```

Si faltan criterios o el riesgo es alto, pasa a `NEEDS_HUMAN` o pide aclaración. No modifiques workflow corporativo real sin autorización.

## Webhooks y Rovo

Un webhook notifica un evento; no es una transacción exactamente una vez. Puede duplicarse, retrasarse, llegar fuera de orden o no llegar. Verifica autenticidad, guarda una clave de deduplicación y consulta Jira por el estado actual. Diseña un reconciliador que compare periódicamente ejecuciones abiertas con los tickets origen.

Rovo puede servir como apoyo de búsqueda/síntesis de conocimiento Atlassian si está habilitado, disponible para la organización y configurado con permisos correctos. No supongas que puede invocar APIs, escribir código o controlar releases. Valida capacidades y licencia reales. Conserva fuente, fecha y permisos de los documentos usados.

## Ejemplo de criterios

Historia sintética `SHOP-214`: recuperar acceso a la cuenta.

- Dado un email registrado, cuando el usuario solicita recuperación, entonces recibe una respuesta neutra y el flujo envía un enlace de un solo uso.
- Dado un email no registrado, cuando se solicita recuperación, entonces la respuesta pública no revela si la cuenta existe.
- Dado un enlace expirado o ya utilizado, cuando se abre, entonces no inicia sesión y ofrece un nuevo flujo.
- Dado que se exceden intentos permitidos, cuando se solicita otra vez, entonces se aplica el control acordado y queda un evento auditable sin registrar el token secreto.

No inventes la duración del enlace ni el umbral de intentos: deja pregunta pendiente hasta que producto/seguridad lo confirmen.

## Práctica deliberada

### Ejercicio A — Mejorar historias (45–60 min)

Escribe tres historias: una feature, un bug y una pregunta. Añade criterios positivos, negativos y de frontera. Anota qué criterio puede automatizarse y qué decisión necesita al PO.

### Ejercicio B — Contrato de evento (60 min)

Define un evento mock con `event_id`, `issue_key`, `transition_id`, `occurred_at`, `actor`, `project` y `signature`. Implementa elegibilidad y deduplicación. Prueba: doble entrega, estado actual distinto, etiqueta ausente, issue de otro proyecto y ticket cancelado antes del consumo.

**Criterios de aceptación:** cada historia tiene valor y criterios observables; ambigüedad crítica bloquea; el evento se autentica y es idempotente; no se confía en orden de llegada ni en nombre de estado solamente.

## Feynman: el ticket no es un system prompt

Jira almacena solicitudes, comentarios y enlaces creados por distintas personas e integraciones. Su contenido puede ser equivocado o malicioso. El ticket provee **datos** para evaluar; no tiene autoridad para cambiar identidad, permisos, políticas, secretos o gates. Explica esta diferencia con un ejemplo de prompt injection escrito en un comentario.

## Recuerdo activo

¿Qué hace que un criterio sea verificable? ¿Qué pasos siguen a un webhook duplicado? ¿Qué información se debe confirmar antes de automatizar `In Progress`? ¿Dónde puede ayudar Rovo y qué no debemos asumir de él?
