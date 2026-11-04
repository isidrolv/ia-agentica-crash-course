# Semana 10 — Code review y calidad

**Tiempo sugerido:** 8–10 horas. **Resultado:** reviewer de solo lectura, hallazgos accionables y gate evaluado con cambios sembrados con defectos.

## Recuperación antes de aprender

¿Qué identidad debería aprobar el trabajo del coder? ¿Qué información hace que un hallazgo sea corregible? ¿Por qué un reviewer LLM no sustituye pruebas y análisis estático?

## Independencia y alcance de la revisión

El reviewer compara el diff integrado contra criterios aprobados, contratos, convenciones, riesgos y resultados de pruebas. Recibe el commit base y commit candidato; revisa cambios, no solo el resumen del coder. Tiene permiso de lectura, no edita ni autoaprueba su propio cambio. Una identidad independiente reduce conflicto de interés, aunque no garantiza una revisión correcta.

Revisa por prioridad:

1. ¿Cumple criterios y conserva compatibilidad de contratos?
2. ¿Introduce errores de lógica, autorización o manejo de estados límite?
3. ¿Se filtran datos, tokens, PII o información de infraestructura?
4. ¿Maneja errores, concurrencia y reintentos de forma segura?
5. ¿Pruebas representan casos positivos, negativos y límites?
6. ¿Cambios son mantenibles y están dentro del alcance?

Estilo y formato pueden automatizarse con linters. No dejes que comentarios de estilo oculten un bug crítico.

## Hallazgos estructurados

Un hallazgo debería incluir `id`, `severity`, `file`, `line_range`, `criterion_id`, `description`, `evidence`, `impact`, `suggested_fix` y `confidence`. `confidence` no sustituye evidencia. Exige ubicación exacta y comportamiento reproducible o explicación verificable. Clasifica como `BLOCK`, `FIX`, `RECHECK`, `PASS` o `NEEDS_HUMAN`; el estado final se calcula con política determinista.

Ejemplo: el diff agrega `POST /password-reset` y devuelve `404` solo si el correo no existe. Reviewer informa `BLOCK`, `services/auth/reset.py:42-48`, `AC-2`: el status code permite enumerar cuentas. Adjunta dos requests sintéticos que devuelven respuestas distintas. Sugerencia: respuesta pública neutra y prueba de regresión. El integrador no acepta `PASS` si existen hallazgos bloqueantes sin resolver.

## Falsos positivos y evaluación del reviewer

Un modelo puede reportar problemas inexistentes o pasar por alto defectos. Construye un conjunto etiquetado de PRs: algunos con vulnerabilidades/breakages intencionales y otros seguros. Mide **recall de bloqueos críticos** (¿detectó los defectos graves?), **precision** (¿cuántos hallazgos eran válidos?), y tiempo/revisión humana. Para defectos críticos, una falsa negativa suele ser más costosa; calibra umbrales por tipo de riesgo y exige escáneres deterministas cuando están disponibles.

Un hallazgo LLM no debe bloquear para siempre sin ruta de apelación. Define quién decide falsos positivos y cómo se corrige la regla. No dejes que el coder escriba “ignora este finding” y el workflow lo cierre sin evidencia.

## Práctica deliberada

### Ejercicio A — PRs sembrados (60–90 min)

Crea cinco diffs en repositorio de laboratorio: exposición de email, autorización faltante, error de frontera, cambio de contrato incompatible y refactor seguro. Ejecuta reviewer y escáneres. Etiqueta hallazgos manualmente; calcula precision/recall básicos y registra omisiones.

### Ejercicio B — Workflow de hallazgos (45 min)

Define transición `REVIEW → FIX → RECHECK → PASS`. Rechaza un PASS que omita el commit revisado, tenga bloqueantes abiertos, o se refiera a tests de otra versión. Asegúrate de que el mismo agente no codifica y firma aprobación independiente.

**Criterios de aceptación:** hallazgo vinculado a archivo, línea, criterio y evidencia; severity aplicada por política; defectos críticos bloquean; false positives son revisables; nueva versión invalida review anterior.

## Errores frecuentes

- Aceptar “se ve bien” o “no encontré problemas” sin versión y alcance revisados.
- Tratar una explicación segura del modelo como evidencia de corrección.
- Hacer que reviewer escriba cambios y apruebe el mismo diff sin nueva revisión.
- Permitir que PASS omita pruebas fallidas o escáneres críticos.

## Recuerdo activo y Feynman

¿Qué diferencia a un hallazgo de una recomendación vaga? ¿Qué es un falso negativo? ¿Qué condiciones hacen obsoleta una aprobación? Explica por qué code review puede habilitar CI pero no debería desplegar directamente.
