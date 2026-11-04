# Semana 5 — Orquestación durable

**Tiempo sugerido:** 9–11 horas. **Resultado:** workflow persistente que consume eventos, avanza por estados válidos y se recupera sin repetir efectos.

## Recuperación antes de aprender

¿Qué diferencia hay entre reintentar una función pura y volver a crear un PR? Dibuja qué queda guardado si el proceso cae después de iniciar CI, pero antes de registrar su respuesta.

## Workflow frente a agente

Un **workflow** determina el orden y las condiciones de ejecución. Un **agente** propone decisiones dentro de una etapa. La máquina de estados conserva el control:

```text
RECEIVED → CONTEXT_READY → PLANNED → IMPLEMENTING → VERIFYING → REVIEW → CI → DONE
     ↘ BLOCKED / NEEDS_HUMAN / CANCELLED / FAILED_RETRYABLE / FAILED_FINAL
```

Cada transición debe tener precondición, comando permitido, evidencia de entrada, estado de salida y política de error. Por ejemplo, `VERIFYING → REVIEW` requiere commit candidato, pruebas obligatorias exitosas y resultados asociados al mismo hash. El LLM no puede saltar directamente de `IMPLEMENTING` a `DONE`.

## Durabilidad y checkpoints

Un proceso en memoria desaparece al cerrarse. Guarda estado en un almacén durable antes/después de efectos importantes: `run_id`, issue, versión de entrada, estado, intento, commit, artefactos, aprobaciones, errores y marcas de tiempo. Un **checkpoint** permite continuar desde una frontera segura. Si ya se creó una rama, reanudar debe consultar si existe y asociarla a la ejecución, no crear otra a ciegas.

El estado es un registro operativo; conviene versionar su esquema y preservar historial de transiciones. Evita guardar prompts completos, secretos o datos sensibles innecesarios. Un identificador de ejecución correlaciona eventos, agentes, herramientas y CI.

## Entrega de eventos, idempotencia y reintentos

Los sistemas de cola/webhook suelen ofrecer entrega al menos una vez: el mismo evento puede procesarse varias veces. “Exactamente una vez” entre Jira, Git y CI es una promesa difícil porque no comparten una transacción. Diseña cada efecto externo para ser **idempotente** o reconciliable.

Clave de deduplicación: `(issue_key, transition_id, workflow_version)`. Regístrala con restricción única antes de iniciar el trabajo. Si una fila ya existe, devuelve la ejecución existente. Para crear recursos, usa identificadores deterministas o consulta por etiqueta `run_id` antes de crear.

Usa timeout y reintentos acotados con backoff exponencial y jitter ante errores transitorios (por ejemplo, 503 o timeout). No reintentes indiscriminadamente errores permanentes como `FORBIDDEN` o argumentos inválidos. Después de agotar reintentos, manda el evento a una cola de fallos (DLQ) y alerta a una persona.

## Fallo parcial, cancelación y compensación

Si Jira se actualiza pero Git falla, queda un estado parcial. El orquestador debe reconciliar, reanudar o ejecutar una compensación que no cause un daño mayor. Este encadenamiento de transacciones locales se puede modelar como una **saga**. No siempre es posible “deshacer” un comentario público o un despliegue; en esos casos registra la incidencia y aplica un forward fix.

La cancelación es cooperativa: detener admisión de tareas nuevas, señalizar agentes, impedir nuevos efectos, terminar procesos o sandbox y marcar artefactos parciales. Un timeout tampoco garantiza que el sistema remoto haya cancelado; consulta el estado remoto antes de reintentar.

## Ejemplo: caída tras crear rama

1. El worker registra `run_id=run-51`, reclama lease para `SHOP-214` y persiste `IMPLEMENTING`.
2. Crea `agent/SHOP-214/run-51` y guarda su identificador.
3. El proceso cae antes de confirmar al usuario.
4. El worker reiniciado lee el checkpoint, confirma que el ticket sigue elegible y verifica la rama por `run_id`.
5. Reanuda el workspace existente y registra `RESUMED`, sin duplicar la rama.

Si el ticket ya fue cancelado, detiene el trabajo y pasa a `CANCELLED`; la reanudación no ignora el estado actual de Jira.

## Práctica deliberada

### Ejercicio A — Máquina de estados (60 min)

Modela los estados y transiciones del pipeline en una tabla: origen, destino, precondición, actor, evidencia, timeout y recuperación. Escribe una función de transición que rechaza saltos como `RECEIVED → CI`.

### Ejercicio B — Fallos inyectados (60–90 min)

Usa un almacenamiento local/mock y simula caída antes y después de: insertar idempotency key, crear rama, iniciar pruebas y recibir resultado CI. Reentrega el evento, reinicia el worker y cancela el ticket en medio de la ejecución. Cuenta efectos duplicados y verifica que sean cero.

**Criterios de aceptación:** reanuda desde checkpoint; duplicados retornan mismo `run_id`; estados ilegales se rechazan; transitorios usan backoff limitado; errores permanentes llegan a `BLOCKED`/DLQ; efectos parciales se reconcilian.

## Errores frecuentes

- Guardar el resultado del agente pero no el estado del workflow.
- Tratar un timeout como prueba de que el servidor remoto no ejecutó nada.
- Repetir `create PR` sin consultar si el PR ya existe.
- Llamar “rollback” a una acción que no puede restaurar efectos irreversibles.

## Recuerdo activo y Feynman

Explica la diferencia entre checkpoint y log; por qué no hay exactly-once global; qué error reintentarías y cuál no; cómo se atiende una ejecución huérfana. Dibuja el punto de recuperación tras iniciar un build.
