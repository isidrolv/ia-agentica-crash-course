# Arquitectura objetivo: Jira → agentes → revisión → CI/CD

## Principios

1. **Workflow determinista para el control; LLM para tareas cognitivas.** El modelo puede clasificar, resumir, proponer o revisar; el servicio de orquestación valida permisos, estados y efectos externos.
2. **El ticket y los documentos recuperados son datos no confiables.** Ningún texto dentro de ellos puede ampliar permisos, revelar secretos o saltarse gates.
3. **Cada etapa deja artefactos verificables.** Contexto con fuentes, plan, commit, tests, revisión, resultados de CI y aprobaciones.
4. **Menor privilegio, aislamiento y aprobación por riesgo.** Los agentes no comparten credenciales de escritura globales.
5. **Reintentos seguros.** Webhooks se duplican y entregan fuera de orden: deduplicar, consultar Jira y hacer transiciones condicionadas.

## Secuencia propuesta

```mermaid
sequenceDiagram
    actor PO as Product Owner
    participant J as Jira
    participant O as Orquestador durable
    participant C as Contexto (Rovo opcional)
    participant P as Planificador/Arquitecto
    participant D as Agente de código
    participant T as Agente de pruebas
    participant I as Integrador determinista
    participant R as Reviewer/Seguridad
    participant CI as CI/CD
    actor H as Aprobador humano

    PO->>J: Crea historia con criterios de aceptación
    J-->>O: Evento de transición a In Progress
    O->>O: Verifica firma, elegibilidad, deduplicación y estado actual
    O->>C: Recuperar contexto con permiso de solo lectura
    C-->>O: Resumen, fuentes, archivos candidatos, dudas
    O->>P: Criterios + contexto versionado
    P-->>O: Plan, contratos, tareas y riesgos
    O->>D: Implementar en rama/worktree aislado
    par Preparación de pruebas mientras se codifica
        O->>T: Crear pruebas desde criterios/contratos en rama aislada
        T-->>O: Tests y resultados sobre snapshots identificados
    and Implementación
        D-->>O: Commits/diffs incrementales y estado
    end
    O->>I: Integrar candidato y tests; ejecutar suite completa
    I-->>O: Artefacto/commit y resultados reproducibles
    O->>R: Diff integrado + requisitos + evidencias de CI
    R-->>O: Hallazgos accionables o PASS
    O->>CI: Iniciar pipeline si se cumplen las puertas
    CI-->>O: Resultado de build, seguridad y despliegue permitido
    opt Producción o acción de alto impacto
        O->>H: Solicita aprobación con evidencias
        H-->>O: Aprobar o rechazar
    end
    O-->>J: Actualiza estado y añade resumen de ejecución
```

## Roles de agentes y servicios

| Rol | Responsabilidad | Permisos recomendados | Salida comprobable |
|---|---|---|---|
| **Triage/Intake** | Determinar elegibilidad, tipo, componente y riesgo del issue. | Lectura de issue y metadatos; sin escrituras autónomas al comienzo. | JSON validado, razón de enrutamiento, `needs_clarification` si aplica. |
| **Contexto/Research** | Buscar repositorio, documentación y conocimiento Atlassian. Rovo puede ocupar este rol si está habilitado y se valida el acceso disponible. | Lectura acotada y filtrada por permisos; no secrets ni deploy. | Resumen con fuentes/enlaces, fecha/versión, dudas y archivos candidatos. |
| **Especificación** | Convertir petición en criterios concretos, casos límite y preguntas. | Proponer; el PO confirma ambigüedades de negocio. | Criterios Given/When/Then y mapa de trazabilidad. |
| **Planificador/Arquitecto** | Descomponer trabajo, definir interfaces, dependencias, riesgos y secuencia. | Lectura; propuesta revisable antes de cambios. | Plan estructurado con límites de archivos/contratos y riesgos. |
| **Codificador** | Implementar una tarea asignada y corregir fallos reportados. | Escritura limitada a rama/worktree temporal; sin aprobar PR, cambiar permisos ni desplegar. | Commits pequeños, diff, pruebas ejecutadas y resumen. |
| **Autor de pruebas** | Derivar pruebas unitarias, integración y funcionales desde criterios/contratos. | Rama/worktree separado; no escribe archivos propiedad del coder. | Tests, matriz criterio→test y comandos/resultados. |
| **Ejecutor de pruebas** | Ejecutar suites en snapshots/candidato integrado y reportar fallos. | Sandbox efímero; acceso a código y datos sintéticos. | Logs redactados, commit probado, clasificación de fallos. |
| **Code reviewer** | Evaluar el diff de forma independiente contra requisitos, calidad y seguridad. | Solo lectura; no puede aprobar su propio cambio ni editar y aprobar en la misma identidad. | PASS o hallazgos con severidad, archivo/línea y evidencia. |
| **Seguridad/Dependencias** | Revisar secretos, dependencias, políticas y amenazas. Puede ser etapa determinista más análisis asistido. | Solo lectura más reporte; bloquear ante riesgo crítico. | SBOM/escaneos o hallazgos accionables. |
| **Release/CI controller** | Aplicar gates, construir y promover artefactos; registrar y, cuando proceda, revertir. | Identidad de servicio separada y credenciales efímeras por entorno. | Artefacto por digest, resultados, aprobaciones y estado de release. |
| **Evaluación/Observabilidad** | Medir calidad del pipeline, costo, latencia, fallos y comportamiento de agentes. | Lectura de telemetría redactada. | Trazas, métricas, alertas y regresión de evaluaciones. |

El **orquestador** es un servicio/workflow durable, no necesariamente otro LLM. Mantiene estado, transiciones, deduplicación, límites, cancelaciones y trazabilidad. n8n puede servir para una prueba de concepto basada en eventos; para tareas largas, paralelismo, checkpoints y recuperación, elige un motor durable o una implementación equivalente. Rovo no debe asumirse como agente que escribe código o despliega: valida las capacidades reales, APIs/licencias y permisos del entorno Atlassian.

## Estado y política de transiciones

Flujo sugerido (los nombres concretos deben mapearse a los estados de tu Jira):

`BACKLOG → READY_FOR_AGENT → IN_PROGRESS → CONTEXT_READY → PLAN_READY → IMPLEMENTING → VERIFYING → REVIEW → CI → READY_FOR_RELEASE → DONE`

Estados de salida: `BLOCKED`, `NEEDS_HUMAN`, `CANCELLED`, `FAILED_RETRYABLE`, `FAILED_FINAL`.

- No todo `In Progress` debe activar automatización: exigir proyecto/issue type elegibles, etiqueta o campo opt-in, criterios suficientes y presupuesto.
- Usa clave idempotente como `issueKey + transitionId + workflowVersion` y consulta Jira para validar estado actual antes de actuar.
- Registra estado durable, versiones de entrada, commit base, artefactos, agente/modelo/prompt, intentos y timestamps.
- Cada transición tiene precondiciones, timeout, salida de error y propietario humano/servicio.
- La acción de agente no debe cerrar el ticket si todavía falta aprobación o promoción correspondiente.

## Pruebas paralelas mientras codifica

Es viable y útil **preparar casos y escribir pruebas en paralelo** si criterios y contratos de interfaz son estables. Implementación recomendada:

1. Al aprobar el plan, crea una rama/worktree de coder y otra de test author desde el mismo commit base. Asigna propiedad de archivos para no editar simultáneamente el mismo archivo.
2. El test author construye tests primero desde criterios y contratos, incluso si no compilan todavía; marca dependencias y supuestos. El coder implementa componentes.
3. Cuando hay snapshot/commit nuevo, el integrador monta una ejecución aislada con ese commit y la rama de tests; ejecuta solo el subconjunto que tiene sentido y etiqueta resultados con hashes exactos.
4. Los fallos reproducibles regresan como feedback al coder. Al llegar a `CODE_COMPLETE`, congela el candidato, integra tests y código, corre unitarias, integración, funcionales, lint, seguridad y compilación requeridas.
5. Si el coder cambia código, invalida los resultados afectados y repite las pruebas sobre el nuevo commit. No uses un “test verde” de una revisión anterior para aprobar el último cambio.
6. Reviewer inspecciona el diff y evidencias del candidato integrado. Solo entonces CI/CD avanza según política.

No hagas que un agente escriba en el checkout mutable de otro ni que tests temporales verdes disparen despliegues. Separa el **feedback continuo** del **gate final**.

## Puertas CI/CD y promoción

1. **Pre-merge:** formato/lint, compilación, unitarias, contratos, análisis estático y secretos.
2. **Candidato integrado:** integración, funcionales relevantes, regresión, dependencias/imagen y firma/procedencia del artefacto.
3. **Review:** aprobación independiente y sin hallazgos bloqueantes.
4. **Staging:** despliegue del mismo artefacto inmutable, smoke tests y observación de SLI.
5. **Producción:** aprobación humana inicialmente; despliegue progresivo/canary, criterios automáticos de salud y rollback documentado.

Code review **no debe disparar directamente producción**. Un resultado PASS puede habilitar el workflow de CI/CD; el pipeline determinista vuelve a validar todos los gates. Entrega continua puede dejar listo para aprobación; despliegue continuo requiere políticas, evaluación y gobierno adecuados.

## Seguridad y operación

- Verifica autenticidad de webhooks; evita guardar tokens en prompts, issues o logs.
- Credenciales por agente/etapa, solo lectura por defecto, alcance mínimo, expiración corta y rotación.
- Sanitiza contenido externo y defiende contra prompt injection con aislamiento de datos y validación de acciones; no dependas de una frase del system prompt.
- Ejecuta código generado en sandbox efímero, sin secretos, con red, CPU, memoria y tiempo limitados.
- Logs y trazas con correlación por `issueKey`/`runId`, redacción de datos sensibles y evidencia reproducible.
- Retries limitados con backoff/jitter; dead-letter queue, cancelación cooperativa, reconciliación y alertas.
- Antes de producción: evaluación de seguridad, privacidad, licencias y políticas de la organización.

## Decisiones a validar al implementar

El curso es vendor-neutral. El prototipo debe elegir un proveedor/modelo, un orquestador durable, la integración Jira disponible, el sistema Git/CI, identidad/secrets manager y sandbox. Confirma soporte, costos, residencia de datos, APIs/licencia de Rovo y políticas internas antes de fijar la arquitectura. Comienza con Jira y repositorio de prueba, datos sintéticos y deploy de staging.
