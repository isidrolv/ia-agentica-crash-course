# Semana 12 — Evaluación, observabilidad y resiliencia

**Tiempo sugerido:** 9–12 horas. **Resultado:** evaluación reproducible y una traza de pipeline que permite diagnosticar fallos, costo y recuperación.

## Recuperación antes de aprender

¿Por qué un test unitario convencional no mide por completo la calidad de un agente? ¿Qué identificador permite conectar el webhook con el resultado del deploy? ¿Qué diferencia hay entre timeout y error permanente?

## Evaluaciones para sistemas probabilísticos

Una **prueba de software** verifica comportamiento esperado de componentes; una **eval** mide desempeño del sistema modelo sobre un conjunto de casos y una rúbrica. Usa casos versionados, entradas realistas, etiquetas, límites aceptables y revisión de errores. Cambios de prompt, modelo, retrieval, schema o herramienta pueden alterar comportamiento y requieren regresión.

Evalúa por dimensiones: clasificación y routing, cobertura de fuentes, fidelidad de resumen, validez de salida, seguridad, tasa de intervención humana, costo y latencia. No reduzcas calidad a una sola puntuación agregada que oculte fallos críticos. Los jueces LLM pueden ayudar a puntuar tono o relevancia, pero también se equivocan; valida muestras humanas y nunca sustituyas tests deterministas de permisos.

Separa casos de desarrollo de los de evaluación final para reducir sobreajuste. Incluye casos comunes, límites, entradas adversariales, ambigüedad y situaciones no vistas. Registra versiones exactas de modelo, prompt, retrieval, tools, dataset y criterios.

## Trazas, métricas y SLO

Un trace con `run_id` enlaza spans de recepción del webhook, recuperación, llamadas de modelo, tool calls, cambios de código, test runs, review y deploy. Cada span incluye hora, estado, versión y duración. Redacta secretos antes de exportar. Una métrica agregada no reemplaza la traza por ticket.

Métricas útiles: éxito por etapa, duración p50/p95, retrabajo, retries, tasa de escalamiento humano, defectos bloqueados/escapados, calidad de retrieval, costo/token y fallos de proveedor. Define SLI observable y SLO con población y ventana, por ejemplo “95% de los tickets elegibles con datos completos terminan contexto dentro del presupuesto de tiempo”; excluye deliberadamente tickets bloqueados por humanos según se defina.

## Resiliencia: límites y recuperación

- **Timeout:** no dejar llamadas colgadas; consultar estado remoto antes de repetir efecto.
- **Rate limit:** leer `Retry-After` si existe, limitar concurrencia y usar backoff con jitter.
- **Circuit breaker:** dejar de llamar temporalmente a servicio persistentemente fallido y probar recuperación controladamente.
- **Backpressure:** reducir admisión cuando una etapa posterior se satura; mantener colas acotadas.
- **DLQ:** aislar eventos que agotaron reintentos para revisión y reproceso seguro.
- **Reconciliación:** comparar estado durable con Jira/Git/CI para corregir eventos perdidos o estados parciales.
- **Cancelación:** no iniciar nuevos efectos, parar workers de manera cooperativa y comprobar remotos.

## Ejemplo: proveedor de modelo degradado

El servicio de modelos devuelve timeout en `CONTEXT_READY`. El orquestador mantiene el checkpoint, aplica timeout y un retry con jitter. Tras N intentos abre el circuit breaker, guarda `FAILED_RETRYABLE`, emite alerta y deja ticket sin cambios. Al recuperarse, reanuda desde el mismo `run_id`. No crea un segundo branch ni cambia ticket a `DONE`. Si hay fallback model, ya debe haber pasado eval de compatibilidad y la traza registra que fue usado.

## Práctica deliberada

### Ejercicio A — Instrumentación (60 min)

Define eventos y spans por etapa con `run_id`, `issue_key` pseudonimizado si corresponde, agente, versión, duración, outcome, costo y referencia al artefacto. Redacta prompt con secreto sintético y verifica que no aparece en logs.

### Ejercicio B — Chaos tabletop (90 min)

Simula Jira caído, webhook duplicado, entrega fuera de orden, modelo lento, rate limit, test runner sin recursos, CI fallido, cancelación durante ejecución y estado remoto cambiado manualmente. Para cada escenario documenta detección, estado durable, retry/stop, efecto duplicado, alerta y operador responsable.

**Criterios de aceptación:** cualquier run se traza extremo a extremo; los logs no contienen secretos; los retries son limitados; backpressure previene cola ilimitada; la recuperación evita efectos duplicados; dashboard distingue bloqueos de defectos.

## Errores frecuentes

- Reintentar en cascada en todos los niveles sin presupuesto común.
- Capturar todos los prompts y outputs “por observabilidad” sin política de datos.
- Promediar éxito de agentes y esconder un gate crítico con baja tasa.
- Hacer fallback de modelo sin registrar/evaluar diferencias.

## Recuerdo activo y Feynman

¿Qué dimensiones evalúas? ¿Qué campos mínimos unen spans? ¿Cuándo abrirías circuit breaker? ¿Qué debe ocurrir al agotar reintentos? Explica a otra persona por qué una buena demo necesita también métricas y una estrategia de recuperación.
