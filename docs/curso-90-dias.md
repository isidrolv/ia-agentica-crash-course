# Curso de IA Agéntica para ingeniería de software — 90 días

## Resultado demostrable

Construir un prototipo que tome una historia elegible de Jira, reúna contexto verificable, coordine agentes separados para planificación, código y pruebas, ejecute revisión independiente y permita que CI/CD avance solo tras cumplir puertas de calidad. El pipeline debe poder pausarse, reanudarse, auditarse y recuperarse ante fallos. Para producción, integrar aprobación humana según riesgo.

> **Expectativa realista:** 90 días de práctica enfocada pueden llevarte a un nivel avanzado y a un prototipo funcional; “1% superior” no es medible ni garantizable sin una población y una evaluación definidas. Aquí se aproxima mediante un examen acumulativo, una demo reproducible y una revisión de amenazas.

## Ritmo neuro-optimizado

Plan orientativo: **10–12 horas por semana**, seis días de práctica y uno ligero. Ajusta el tiempo si tus obligaciones lo requieren.

- **Recuerdo activo:** comienza cada sesión escribiendo o dibujando lo que recuerdas sin consultar notas; luego verifica y corrige.
- **Repetición espaciada:** repasa cada concepto al terminar, al día siguiente, a los 3, 7, 14 y 30 días. Usa `quiz_console_pro.py --review-only` o el modo de tarjetas.
- **Intercalación:** alterna diseño de agentes, integración, seguridad, pruebas y operación; evita estudiar una única herramienta durante semanas sin contexto.
- **Feynman:** explica cada semana un concepto en lenguaje simple, con diagrama, ejemplo y una limitación; si no puedes, identifica la laguna y vuelve a estudiarla.
- **Práctica deliberada:** entrega algo ejecutable o revisable cada semana. Usa fallos controlados, no solo lecturas.
- **Evaluación:** registra porcentaje recordado, latencia/costo del prototipo, defectos encontrados, falsos positivos/negativos y decisiones humanas.

### Rutina semanal sugerida

| Día | Sesión (60–120 min) |
|---|---|
| Lunes | Recuerdo activo de la semana anterior + concepto nuevo + notas Feynman. |
| Martes | Implementación guiada y pruebas pequeñas. |
| Miércoles | Tema intercalado (seguridad, calidad o sistemas distribuidos) aplicado al prototipo. |
| Jueves | Ejercicio sin apuntes; después consulta el material y corrige. |
| Viernes | Integración del entregable, test de regresión y revisión de decisiones. |
| Sábado | Demo de 5–10 minutos y retrospectiva: qué falló, qué automatizar y qué debe seguir con aprobación humana. |
| Domingo | Descanso o 15 minutos de tarjetas vencidas; no introduzcas contenido nuevo. |

## Programa de 13 semanas

### Semana 1 — Fundamentos de IA agéntica
- **Aprende:** LLM vs agente, herramientas, ciclo observar–decidir–actuar, estado, límites de autonomía y fallos no deterministas.
- **Practica:** crea un agente de solo lectura que clasifique historias ficticias en tipo, componente y riesgo; salida JSON validada.
- **Entregable:** contrato de entrada/salida y 20 ejemplos de evaluación, incluyendo ticket ambiguo y prompt injection.
- **Recuerdo/Feynman:** explica por qué un LLM no equivale a un workflow confiable.

### Semana 2 — Prompting, contexto y grounding
- **Aprende:** instrucciones, contexto, ventana de tokens, fuentes confiables, RAG, citas y gestión de incertidumbre.
- **Practica:** agente de contexto que resuma una historia y cite documentos/repositorio; no escribe en Jira ni Git.
- **Entregable:** paquete de contexto con requisitos, enlaces/fuentes, archivos candidatos, dudas y confianza.
- **Intercalación:** vuelve a evaluar las historias de semana 1 con contexto insuficiente o contradictorio.

### Semana 3 — Diseño de herramientas y permisos
- **Aprende:** schemas, validación, MCP, identidad, mínimo privilegio, credenciales efímeras y fronteras de confianza.
- **Practica:** mock de Jira y Git con operaciones distintas de lectura y escritura; valida argumentos y permisos fuera del prompt.
- **Entregable:** matriz de herramientas, permisos por agente y casos negativos de autorización.

### Semana 4 — Historias, criterios y Jira
- **Aprende:** historias pequeñas, criterios de aceptación, issue types, estados, webhooks/eventos, Rovo como posible buscador/contextualizador según disponibilidad y permisos.
- **Practica:** crear historias de ejemplo y transformarlas en un contexto verificable; simular la transición a `In Progress`.
- **Entregable:** esquema de historia listo para automatización y regla de elegibilidad (proyecto, etiqueta, criterios, riesgo).
- **Feynman:** explica por qué un ticket no es una instrucción de sistema confiable.

### Semana 5 — Orquestación durable
- **Aprende:** workflow vs agente, máquinas de estado, colas, checkpointing, idempotencia, retries, backoff y cancelación.
- **Practica:** workflow de estados `RECEIVED → CONTEXT_READY → PLANNED → IMPLEMENTING → VERIFYING → REVIEW → CI → DONE/BLOCKED`.
- **Entregable:** diagrama de secuencia, registro durable de ejecución, deduplicación por issue/transición y cola de fallos.

### Semana 6 — Multiagente y contratos
- **Aprende:** descomposición, handoffs, agentes especializados, coordinación, límites de paralelismo y consistencia.
- **Practica:** agrega agente de planificación/arquitectura que entregue tareas, interfaces, archivos candidatos y riesgos.
- **Entregable:** contratos versionados para contexto, plan, cambio de código, pruebas y revisión.
- **Intercalación:** repetir tests de semanas 1–5 sobre entradas duplicadas, evento atrasado y tool call malformada.

### Semana 7 — Agente de codificación
- **Aprende:** contexto de repositorio, convenciones, ejecución en sandbox, ramas/worktrees, cambios pequeños y resumen de diff.
- **Practica:** codificador que modifica una rama aislada a partir de plan aprobado y criterios; no puede hacer merge ni desplegar.
- **Entregable:** un cambio pequeño con diff, pruebas locales y trazabilidad a criterios.

### Semana 8 — Agente de pruebas en paralelo
- **Aprende:** unitarias, integración, funcionales, contratos, fixtures, oráculos, tests de regresión y trabajo paralelo sin colisiones.
- **Practica:** el agente de pruebas comienza desde criterios/contratos en una rama separada mientras el codificador implementa. Corre pruebas rápidas sobre snapshots identificados; comunica fallos reproducibles y vuelve a probar cambios nuevos.
- **Entregable:** matriz criterio→caso de prueba y demostración de ciclo fallido-corregido. La suite completa corre una vez que el candidato está integrado/estable.

### Semana 9 — Seguridad de aplicaciones y agentes
- **Aprende:** prompt injection directa/indirecta, OWASP para aplicaciones LLM, secretos, SSRF, exfiltración, cadena de suministro y sandbox.
- **Practica:** ataque controlado desde un comentario de Jira o archivo README; demuestra que el texto no cambia permisos ni omite puertas.
- **Entregable:** threat model, controles, logs redactados y reporte de escenarios de abuso.

### Semana 10 — Code review y calidad
- **Aprende:** revisión independiente, riesgos de falsos positivos, análisis estático, dependencias, cobertura útil y puertas de calidad.
- **Practica:** agente reviewer separado del coder; hallazgos deben referenciar archivo/línea, criterio, severidad y evidencia. No aprueba su propio diff.
- **Entregable:** flujo de hallazgos `BLOCK / FIX / RECHECK / PASS` y evaluación sobre PRs sembrados con defectos.

### Semana 11 — CI/CD y despliegue seguro
- **Aprende:** CI vs entrega/despliegue continuo, artefactos inmutables, promoción entre entornos, canary, rollback y aprobaciones.
- **Practica:** pipeline local/mock que solo avanza si pruebas, revisión y escaneos requeridos pasan. Simula deploy de staging y rollback.
- **Entregable:** reglas CI/CD versionadas; producción con gate humano hasta demostrar control y cumplir gobernanza organizacional.

### Semana 12 — Evaluación, observabilidad y resiliencia
- **Aprende:** evals probabilísticos, trazas distribuidas, métricas, costo/token, SLO, rate limit, backpressure, circuit breaker y reconciliación.
- **Practica:** introduce caídas de Jira/modelo/CI, evento duplicado, timeout y cancelación; comprueba recuperación sin duplicar cambios.
- **Entregable:** dashboard/trazas de una corrida, reporte de fallas y playbook de operación.

### Semana 13 — Integración final y evaluación
- **Aprende:** repaso intercalado y toma de decisiones basada en evidencia.
- **Construye:** demo de extremo a extremo con historia de prueba, contexto trazable, plan, PR simulado, tests, code review, CI y estados de Jira sincronizados.
- **Evalúa:** 80%+ de recuerdo en cada nivel del banco; 100% de criterios críticos trazables; ningún secreto en contexto/logs; eventos duplicados no duplican efectos; fallos críticos bloquean entrega; rollback ensayado.
- **Examen Feynman:** graba una explicación de 10 minutos y responde: qué hace cada agente, quién tiene permisos, cómo se reanuda el pipeline y qué impide producción insegura.

## Hitos de 30/60/90 días

- **Día 30:** agente de contexto de solo lectura, criterios buenos y evaluación reproducible.
- **Día 60:** orquestación durable, agente de código aislado y pruebas generadas en paralelo con sincronización segura.
- **Día 90:** pipeline integrado, revisión independiente, CI/CD protegido, trazabilidad, recuperación y demo documentada.

## Registro de aprendizaje

Después de cada sesión registra: fecha, preguntas recordadas sin ayuda, errores y causa, concepto explicado con Feynman, próximo repaso (1/3/7/14/30 días), cambio del prototipo, riesgos/decisiones y siguiente experimento. Mide calidad además de velocidad: una automatización rápida que introduce defectos no es progreso.
