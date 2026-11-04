# Semana 6 — Sistemas multiagente y contratos

**Tiempo sugerido:** 8–10 horas. **Resultado:** un planificador que divide una historia en tareas y contratos versionados para los handoffs del pipeline.

## Recuperación antes de aprender

¿Cuándo aumenta calidad una arquitectura multiagente y cuándo solo añade latencia? ¿Qué ocurre si la salida del agente de contexto cambia de forma y el codificador sigue esperando el esquema anterior?

## Una responsabilidad por agente, no un agente por cada idea

Separa agentes si tienen objetivos, contexto, herramientas, evaluación o límites de confianza distintos. Por ejemplo, un coder con permiso de escribir no debería ser el único reviewer. No dividas cada subpaso en un nuevo agente automáticamente: coordinación, llamadas, contexto repetido y fallos de integración tienen costo.

El **orquestador** conserva el estado y asigna trabajo. En orquestación centralizada, el coordinador ordena etapas y recoge resultados; en coreografía, los componentes reaccionan a eventos. La primera suele ser más fácil de auditar para un pipeline de ingeniería; la segunda puede reducir dependencia central, pero complica observar y depurar el flujo. Ambas requieren contratos y políticas explícitas.

## Handoffs: contratos, evidencia y versión

Un contrato de handoff es una API entre agentes. Especifica campos, tipos, versión, restricciones, errores y qué evidencia debe acompañar a cada conclusión. Valida la salida antes de entregarla al agente siguiente. Si el contrato se rompe, pausa con error explícito; no intentes “adivinar” campos.

Un planificador para `SHOP-214` puede devolver:

```json
{
  "schema_version": "1.0",
  "status": "READY",
  "tasks": [
    {"id": "T1", "owner": "backend", "depends_on": [], "contract": "POST /reset"},
    {"id": "T2", "owner": "mobile", "depends_on": ["T1"], "contract": "consume reset response"},
    {"id": "T3", "owner": "tests", "depends_on": [], "contract": "acceptance criteria AC-1..AC-4"}
  ],
  "shared_interfaces": ["ResetRequest", "ResetResult"],
  "risks": [{"id": "R1", "severity": "high", "question": "..."}],
  "needs_human": false
}
```

Los ejemplos no dan autoridad al agente para decidir temas de negocio. Si la expiración de token no está definida, la salida correcta puede ser `NEEDS_HUMAN`, no inventar un valor.

## Paralelismo y consistencia

Dos tareas pueden correr en paralelo si sus dependencias se han resuelto y no editan los mismos recursos. Marca `depends_on`, propiedad de archivos, commit base y contrato compartido. Cuando tareas convergen, el integrador valida que los cambios funcionen juntos; no asumir que dos resultados individualmente válidos son compatibles.

Paralelismo aumenta throughput hasta que contención, tasa de errores o costo supera el beneficio. Define límites por ticket, proyecto y proveedor. Aísla resultados; los agentes consumen artefactos inmutables, no carpetas compartidas modificadas concurrentemente.

## Ejemplo de secuencia

1. Contexto produce requisitos y preguntas.
2. Especificación confirma ambigüedad crítica con PO.
3. Planificador crea T1 backend, T2 móvil depende de T1, T3 tests se prepara en paralelo desde contratos.
4. Coders trabajan en worktrees separados. El test author no toca los archivos de implementación.
5. Integrador reúne hashes y ejecuta suites sobre un snapshot combinado.

Si el contrato del API cambia en T1, T2 y tests quedan marcados como afectados y se revalidan.

## Práctica deliberada

### Ejercicio A — Descomposición (60 min)

Toma una historia mediana. Divide en 3–5 tareas con owner, dependencia, interfaz, archivos permitidos, pruebas y riesgo. Etiqueta tareas paralelizables y justifica por qué.

### Ejercicio B — Contrato versionado (60 min)

Escribe schemas para `ContextPackage`, `Plan`, `CodeResult`, `TestReport` y `ReviewFinding`. Agrega `schema_version`, estado (`READY`, `BLOCKED`, `NEEDS_HUMAN`) y referencias de evidencia. Crea una prueba de compatibilidad donde falta un campo, cambia enum o versión y verifica que se detenga el pipeline.

**Criterios de aceptación:** cada tarea tiene dueño y salida verificable; no hay ciclo de dependencias; conflictos de archivos son explícitos; cambios de contrato invalidan dependientes; el plan puede terminar en aclaración humana.

## Errores frecuentes

- Crear muchos agentes sin definir quién mantiene la verdad del estado.
- Compartir el mismo checkout mutable entre escritor y tester.
- Hacer que el coder diseñe un contrato y que ningún consumidor lo valide.
- Aumentar paralelismo para reducir latencia sin medir contención.

## Intercalación y Feynman

Repite casos previos con evento duplicado, retrasado y una tool call malformada. Explica por qué contratos entre agentes se parecen a APIs y qué debe hacer el sistema cuando la versión recibida no es compatible.
