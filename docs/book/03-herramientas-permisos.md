# Semana 3 — Diseño de herramientas y permisos

**Tiempo sugerido:** 8–10 horas. **Resultado:** una maqueta de Jira/Git con herramientas explícitas, validación en el runtime y permisos por identidad/rol.

## Recuperación antes de aprender

¿Quién debe impedir una llamada `create_branch` si el prompt indica que el agente solo puede leer? ¿Por qué una herramienta `jira_api(url, method, body)` es más difícil de proteger que `read_issue(issue_key)`?

## Diseñar interfaces que limiten daños

Una herramienta es una operación acotada, no una sesión ilimitada del sistema operativo. Favorece nombres y argumentos específicos: `read_issue(key)`, `list_files(path_prefix)`, `get_file(path, revision)`. Evita exponer capacidades genéricas como shell irrestricto, HTTP arbitrario o SQL libre. Las herramientas de lectura y escritura deben ser distintas y sujetas a políticas diferentes.

Un contrato de herramienta define:

- nombre, propósito y clase de efecto (lectura/escritura);
- schema de argumentos, campos requeridos, límites y tipos;
- identidad/permisos necesarios;
- validación semántica y efecto esperado;
- errores tipados, timeout y límites de recursos;
- auditoría sin datos secretos.

La validación ocurre antes del efecto. Un argumento válido como texto puede seguir siendo peligroso: `path="../../.env"` debe rechazarse por resolver rutas fuera del workspace. El runtime verifica pertenencia del recurso, autorización y estado actual, no solo sintaxis.

## Identidad, autorización y mínimo privilegio

**Autenticación** responde quién llama; **autorización**, qué puede hacer en este recurso. Un mismo proceso orquestador puede usar identidades diferentes para leer Jira, crear una rama o iniciar CI. Evita tokens compartidos entre todos los agentes. Prefiere credenciales de corta duración, alcance mínimo y emisión justo antes de una etapa.

Una matriz inicial de permisos:

| Agente | Jira | Repositorio | CI/CD |
|---|---|---|---|
| Contexto | Leer issue elegible | Leer commit permitido | Ninguno |
| Codificador | Leer issue | Escribir rama/worktree asignado | Ejecutar validaciones locales/mock |
| Pruebas | Leer requisitos | Escribir solo rama de tests | Ejecutar suites en sandbox |
| Reviewer | Leer issue/PR | Solo lectura del diff | Leer resultados |
| Release controller | Actualizar estados permitidos | Leer artefacto firmado | Promover dentro de política |

Las políticas deben verificar operación, recurso, actor, proyecto, estado, duración y riesgo. El texto del ticket nunca concede permisos.

## MCP: protocolo, no política de seguridad

MCP normaliza cómo un cliente descubre y usa herramientas o recursos ofrecidos por un servidor. No garantiza que un servidor sea confiable ni decide automáticamente qué puede hacer el agente. Trata cada servidor como una frontera de confianza: identifica propietario, herramientas expuestas, autenticación, datos transmitidos, límites y logs. Expón solo las capacidades necesarias; un servidor MCP para Jira de solo lectura no debe reutilizar una credencial de administrador.

## Ejemplo: mock mínimo seguro

En vez de pasar al modelo `run_shell(command)`, ofrece `get_issue(key)` y `list_repository_files(prefix)`. El runtime acepta únicamente claves con formato `SHOP-123`, confirma que el proyecto esté en una allowlist, filtra campos sensibles y registra el `run_id`. Para la semana 3, `create_branch` siempre responde `DENIED`: todavía no hay agente que requiera ese efecto.

Errores tipados: `INVALID_ARGUMENT`, `NOT_FOUND`, `FORBIDDEN`, `RATE_LIMITED`, `TIMEOUT`. El modelo puede adaptar su respuesta a `NOT_FOUND`, pero no debe reinterpretar `FORBIDDEN` como permiso para probar otra ruta.

## Práctica deliberada

### Ejercicio A — Catálogo de herramientas (45 min)

Especifica tres herramientas de lectura y dos de escritura futuras. Para cada una, crea schema, ejemplos válidos e inválidos, efecto, permiso, timeout y log esperado. En la primera iteración, deja las dos de escritura deshabilitadas.

### Ejercicio B — Pruebas negativas (60 min)

Mock de Jira y Git: intenta issue de otro proyecto, clave malformada, ruta traversal, archivo fuera del workspace, llamada de escritura del agente de contexto, token expirado y respuesta duplicada. Comprueba denegación en código y en pruebas; no basta que el agente diga “no puedo”.

**Criterios de aceptación:** todas las operaciones tienen contratos estrechos; políticas funcionan aunque se elimine el prompt; identidad es separada por rol; denegaciones dejan razón auditable y no filtran secretos.

## Errores frecuentes

- Dar al agente acceso shell total porque una tarea “podría necesitarlo”.
- Poner secretos en variables visibles para el modelo o en argumentos/logs.
- Creer que usar MCP sustituye allowlists, autenticación y autorización.
- Reintentar automáticamente un `FORBIDDEN` como si fuera un timeout.

## Recuerdo activo y Feynman

Dibuja el camino de una tool call desde propuesta hasta efecto. ¿Dónde validas schema? ¿Dónde autorización? ¿Por qué no se debe confiar en el prompt para permisos? Explica MCP como un conector de capacidades, no como una certificación de seguridad.

**Clave breve:** el LLM propone; el cliente/runtime valida sintaxis y política; la herramienta ejecuta con identidad acotada; el resultado queda auditado. Autorización es control externo. MCP estandariza interacción, no confiabilidad.
