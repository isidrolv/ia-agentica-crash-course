# Semana 13 — Capstone: integración y evaluación final

**Tiempo sugerido:** 10–14 horas. **Resultado:** demo segura, reproducible y explicable de extremo a extremo, con operación y límites documentados.

## Propósito

El capstone demuestra criterio de sistemas, no cantidad de agentes ni uso de un framework específico. Debe enseñar cómo una historia pasa por el pipeline, qué artefactos se crean, qué controles autorizan cada acción y cómo se recupera la ejecución cuando algo falla.

## Arquitectura mínima

Incluye:

1. **Jira mock o sandbox:** historia sintética con criterios y transición elegible.
2. **Intake/contexto:** valida issue, busca fuentes y produce paquete trazable; Rovo puede ser opcional si está permitido.
3. **Planificador:** descompone tareas, contratos, dependencias y riesgos.
4. **Codificador:** cambia una rama/worktree efímero con permisos limitados.
5. **Autor/ejecutor de pruebas:** genera tests desde criterios en espacio separado; ejecuta snapshots y una suite final integrada.
6. **Reviewer/seguridad:** lectura independiente, hallazgos con evidencia y severidad.
7. **Orquestador durable:** estado, checkpoints, idempotencia, retry, cancelación, audit trail.
8. **CI/CD mock:** build, test, scan, staging, gate de aprobación y rollback.
9. **Observabilidad:** una traza por `run_id`, métricas y reporte de fallos.

No se requiere conectar credenciales reales ni desplegar a producción. Una simulación reproducible es preferible a una integración insegura.

## Historia para la demostración

Usa `SHOP-214`: “Como cliente quiero restablecer mi contraseña desde móvil”. Define criterios confirmados y un elemento ambiguo (por ejemplo, expiración del enlace) que debe producir `NEEDS_HUMAN`. Demuestra dos recorridos:

- **Camino aprobado:** criterios completos → contexto con fuentes → plan → código/tests paralelos → integración y tests verdes → review PASS → CI mock → staging.
- **Camino bloqueado:** introduce un criterio insuficiente, prompt injection en comentario, test fallido o scan crítico; el pipeline se detiene y no despliega.

Luego simula evento duplicado y reinicio del worker. Debe reanudar la misma ejecución, no crear un segundo PR/branch. Añade cancelación y explica qué efectos pueden compensarse y cuáles requieren intervención.

## Secuencia de trabajo

### Día 1: contrato y escenarios

Versiona historia, criterios, schemas, estados y matriz de permisos. Define 10–20 casos de evaluación, con ambigüedad y adversarios.

### Día 2: orquestación y agentes

Construye el camino feliz con identidad mock. Persistencia y transiciones funcionan aunque la salida del LLM sea inválida. Implementa pausa humana.

### Día 3: pruebas y revisión

Agrega test author paralelo, integración por hashes, reviewer independiente y evaluación de defectos sembrados.

### Día 4: CI/CD y seguridad

Añade gates deterministas, artefacto identificable, aprobación de staging/producción simulada y rollback. Verifica secreto/prompt injection.

### Día 5: fallo, trazas y presentación

Inyecta duplicado, timeout, cancelación y proveedor caído. Practica demo y explica tradeoffs sin notas.

## Rubrica de evaluación

| Dimensión | Evidencia de dominio |
|---|---|
| Funcionalidad | Demo del camino feliz y camino bloqueado; contratos validados. |
| Trazabilidad | Cada criterio crítico se vincula con prueba y resultado del commit candidato. |
| Autorización | Matriz por agente; intentos fuera de permiso denegados por runtime. |
| Seguridad | No hay secretos en contexto/logs; ejecución aislada; prompt injection no cambia política. |
| Confiabilidad | Duplicados idempotentes; reinicio reanuda; retries limitados; cancelación y DLQ simuladas. |
| Calidad | Tests apropiados, review independiente, defectos críticos bloquean. |
| Entrega | CI gates reproducibles; artefacto versionado; aprobación y rollback demostrados. |
| Observabilidad | Trace conectada por run, logs redactados y métricas útiles. |
| Comunicación | Explicación Feynman clara, límites y decisiones documentados. |

Mínimos recomendados: **80% o más en cada nivel** del banco, cobertura trazable del 100% de criterios críticos, cero secretos expuestos, cero efectos duplicados en pruebas de deduplicación, todo defecto crítico bloquea y rollback ensayado. Los porcentajes de recuerdo no compensan una falla de seguridad.

## Examen Feynman de 10 minutos

Sin slides ni notas, explica:

1. ¿Qué es agente y qué es workflow? ¿Cuál decide transiciones?
2. ¿Qué recibe el coder y cómo se verifica la procedencia del contexto?
3. ¿Cómo puede el test author trabajar mientras codifica sin pisar archivos?
4. ¿Qué ocurre si la prueba pasa en un hash antiguo y falla en el actual?
5. ¿Qué impide que un ticket ordene revelar secretos o desplegar?
6. ¿Quién habilita CI/CD y qué gates se vuelven a validar?
7. ¿Cómo reanudas tras timeout o evento duplicado?
8. ¿Qué debe permanecer con una aprobación humana y por qué?

Graba la explicación, detecta huecos y reintenta dos días después con preguntas en orden distinto.

## Retrospectiva y continuidad

Documenta decisiones arquitectónicas, supuestos pendientes, fallos más costosos, métricas, falso positivo/negativo del reviewer y próximos riesgos. Selecciona dos debilidades para el siguiente ciclo de cuatro semanas. No aumentes autonomía hasta contar con evidencia: entorno de prueba, controles externos, evals, auditoría y ruta de recuperación.
