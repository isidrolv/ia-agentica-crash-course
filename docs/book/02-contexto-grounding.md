# Semana 2 — Prompting, contexto y grounding

**Tiempo sugerido:** 8–10 horas. **Resultado:** un paquete de contexto que resume una historia con fuentes, incertidumbres y rutas candidatas, sin permisos de escritura.

## Recuperación antes de aprender

Recuerda qué límites del clasificador de semana 1 no se resuelven con un prompt mejor. Anota dos formas en que un resumen puede parecer convincente y aun así estar equivocado.

## Prompting no sustituye contexto ni evidencia

Un prompt útil explicita rol, objetivo, límites, formato de salida y qué hacer ante ambigüedad. Sin embargo, una buena instrucción no vuelve actual un documento obsoleto ni convierte una inferencia en un hecho. La calidad depende de cuatro piezas distintas: **instrucciones**, **contexto recuperado**, **herramientas disponibles** y **validación de salida**.

Un orden práctico de confianza para el caso Shop:

1. Requisitos confirmados por el PO y criterios vigentes del issue.
2. Documentación versionada del proyecto y contratos de API.
3. Código y pruebas de la rama/commit objetivo.
4. Comentarios históricos, notas y conocimiento general del modelo.

No todos los entornos usarán este orden; haz explícita la política. Si una fuente contradice a otra, cita ambas y solicita decisión en lugar de escoger silenciosamente.

## Ventana de contexto y selección

La ventana de contexto limita tokens de entrada y salida. Introducir todos los archivos suele empeorar precisión, costo y privacidad. Selecciona contexto usando el issue, su componente, rutas relevantes, historial reciente y filtros de acceso. Resume solo cuando puedas conservar referencias verificables. Mantén fuera secretos, datos personales innecesarios y contenido no relacionado.

Una política de selección reproducible incluye:

- **Relevancia:** ¿qué evidencia responde a un criterio específico?
- **Actualidad:** ¿a qué commit, versión de API o fecha corresponde?
- **Autoridad:** ¿es una fuente aprobada o solo un comentario?
- **Acceso:** ¿el solicitante/agente tiene derecho a verla?
- **Tamaño:** ¿cuántos fragmentos son suficientes sin llenar el contexto?

## RAG y grounding

RAG (*retrieval-augmented generation*) combina recuperación y generación: convierte una consulta en búsqueda, recupera fragmentos, aplica filtros/reranking y entrega evidencia al modelo. La recuperación puede ser lexical, semántica o híbrida. El RAG no garantiza verdad: puede encontrar documentos irrelevantes, incompletos o desactualizados. Cada fragmento debería llevar origen, ruta/URL, versión o fecha, y permiso aplicable.

Mide el buscador por separado del texto generado: **precision@k** pregunta cuántos resultados entre los primeros k son pertinentes; **recall@k**, cuántos de los relevantes se recuperaron. Después evalúa fidelidad: ¿cada afirmación importante tiene evidencia? ¿El agente indica cuando no encontró una fuente? En producción, conserva enlaces/citas, no solo un resumen sin procedencia.

### Manejo de incertidumbre

Usa estados observables como `READY`, `NEEDS_CLARIFICATION`, `NO_SOURCE` y `CONFLICTING_SOURCES`. No conviertas falta de resultados en “no hay problema”. Una confianza numérica puede ayudar a ordenar revisiones, pero requiere calibración: en casos que el modelo marca 0.8, ¿acierta realmente cerca de 80%? Si no, trata esa cifra como señal ordinal y no como garantía.

## Ejemplo guiado: paquete de contexto `SHOP-214`

El issue solicita restablecer contraseña. La guía `docs/auth/reset-flow.md` describe el flujo viejo; el contrato OpenAPI en el commit actual muestra un endpoint diferente; una prueba del frontend todavía llama la ruta antigua. El agente debe producir algo como:

```json
{
  "issue_key": "SHOP-214",
  "requirements": [{"text": "...", "source": "Jira:criterion-1", "kind": "explicit"}],
  "candidate_paths": [{"path": "apps/mobile/auth/reset.ts", "reason": "...", "source": "commit:abc123"}],
  "conflicts": [{"sources": ["docs/auth/reset-flow.md", "openapi.yaml"], "question": "..."}],
  "open_questions": ["¿Qué flujo se considera vigente?"],
  "status": "NEEDS_CLARIFICATION"
}
```

La cita hace revisable el razonamiento. Una ruta candidata no es permiso para editar ese archivo. El agente de contexto sigue siendo de solo lectura.

## Práctica deliberada

### Ejercicio A — Recuperación controlada (60 min)

Prepara 10 documentos de prueba: tres relevantes actuales, dos obsoletos, dos distractores, uno con permiso restringido, uno contradictorio y uno ausente. Ejecuta la misma consulta con búsqueda lexical, semántica o mock. Registra documentos recuperados, precision@k y si el resumen distingue evidencia de inferencia.

### Ejercicio B — Paquete citable (45 min)

Vuelve a usar los 20 tickets de semana 1. Para cada uno, entrega requisitos explícitos, inferencias, fuentes, archivos candidatos, dudas y estado. Repite sobre una versión de entrada donde falte documentación o haya contradicción. Compara decisiones antes y después del contexto; no cuentes como mejora una respuesta más larga sin más evidencia.

**Criterios de aceptación:** las afirmaciones críticas tienen fuente y versión; material confidencial no aparece en salida; falta de contexto produce pregunta/pausa; conflictos se muestran; no existe operación de escritura.

## Errores frecuentes

- Considerar que embeddings implican acceso correcto: cada búsqueda debe respetar ACLs.
- Pegar resultados sin guardar URL, commit o fecha.
- Forzar una respuesta cuando las fuentes discrepan.
- Confundir “no recuperado” con “no existe”.

## Recuerdo activo y Feynman

Explica sin notas la diferencia entre prompt, contexto y grounding. ¿Qué métrica medirías para el retriever? ¿Qué información acompaña a una cita? ¿Qué salida debe producir el agente si dos fuentes confiables discrepan?

**Clave breve:** el prompt instruye; el contexto provee información; grounding conecta afirmaciones con evidencia. Mide precisión/recall de recuperación y fidelidad con casos etiquetados. Una cita necesita origen y versión. Conflicto debe ser explícito y puede requerir aclaración.
