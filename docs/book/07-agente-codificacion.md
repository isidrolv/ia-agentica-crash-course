# Semana 7 — Agente de codificación

**Tiempo sugerido:** 9–12 horas. **Resultado:** cambio pequeño en rama aislada, trazable a criterios y sin capacidad de merge o despliegue.

## Recuperación antes de aprender

¿Qué evidencia necesita el coder para empezar? ¿Qué debería hacer si la ruta propuesta por contexto no existe? ¿Por qué un sandbox debe limitar también la red y no solo el filesystem?

## Del plan aprobado al diff

El coder recibe una historia estructurada, paquete de contexto con fuentes, criterios, plan, contratos y restricciones. Antes de editar, inspecciona estructura, convenciones y pruebas existentes. Debe confirmar que archivos objetivo están dentro del alcance y proponer un plan pequeño. Si requisito e implementación actual discrepan, no los “resuelve” inventando una regla: pausa y escala.

Limita tamaño del cambio. Cada paso debe ser verificable: implementar un comportamiento, ejecutar tests relevantes, revisar diff y guardar commit. Un cambio incremental permite asociar fallos a una edición concreta y simplifica rollback. El agente debe reportar comandos, resultados, archivos modificados, criterios cubiertos, supuestos y pendientes.

## Aislamiento: branch, worktree y sandbox

- **Branch/worktree por run:** evita conflictos con trabajo humano y otras tareas; registra commit base y branch asignado.
- **Sandbox efímero:** ejecuta código sin secretos, con filesystem acotado, CPU/memoria/tiempo limitados y red denegada o allowlisted.
- **Permisos:** puede escribir en su espacio, pero no hacer push a ramas protegidas, aprobar PR ni desplegar.
- **Validación del diff:** bloquea rutas sensibles no autorizadas, archivos de configuración de seguridad o cambios fuera del plan.

Un worktree organiza cambios; no es un límite de seguridad por sí solo. El proceso que ejecuta código y sus credenciales deben estar aislados también.

## Rutina recomendada del coder

1. Verificar que el plan y los criterios tengan estado `READY`.
2. Leer solo rutas autorizadas y localizar pruebas relevantes.
3. Proponer plan concreto y contratos que va a preservar.
4. Cambiar código en pasos pequeños; ejecutar unitarias rápidas.
5. Inspeccionar `git diff` y comprobar que no haya secretos ni archivos ajenos.
6. Entregar commit/hash, tests ejecutados, criterios cubiertos y riesgos.
7. Esperar integración/review; no autoaprobar ni desplegar.

## Ejemplo: corregir endpoint

`SHOP-214` ya tiene endpoint acordado `POST /password-reset`. El plan señala `services/auth/reset_handler.py`, el contrato y los casos. El coder implementa validación de token y respuesta neutra para evitar enumeración de cuentas. No debe decidir la expiración si no existe en requisitos. El test author puede descubrir que la respuesta revela si el correo está registrado: reporta fallo AC-2 con request/response sintético; el coder corrige y vuelve a correr suite en commit nuevo.

## Práctica deliberada

### Ejercicio A — Cambio aislado (90 min)

En un repositorio de laboratorio crea rama o worktree, copia criterios y plan. Implementa un cambio pequeño y agrega tests unitarios. Guarda hash base y final; adjunta lista de archivos y relación `criterio → cambio → prueba`.

### Ejercicio B — Límites de alcance (45 min)

Prueba un cambio malicioso o accidental fuera del alcance: modificación de `.github/workflows`, lectura de `.env`, acceso a `../`, intento de push a `main` o invocación de red. Demuestra que runtime/sandbox lo bloquean sin depender de un prompt admonitorio.

**Criterios de aceptación:** diff acotado; origen y resultado reproducibles; pruebas pasan; cero accesos a secretos; branch protegida intacta; cambios fuera de allowlist bloqueados; resumen menciona limitaciones.

## Errores frecuentes

- Pedir al coder “termina la historia” sin plan ni criterios.
- Permitir shell y red irrestrictos para que solucione dependencias.
- Evaluar solo por “compila en mi máquina”.
- Dejar que el agente actualice documentación, dependencias y workflows sin que sean parte del alcance.

## Recuerdo activo y Feynman

Describe el paquete mínimo de entrada. ¿Qué limita un worktree y qué no? ¿Qué datos debe contener el reporte de cambio? Explica por qué producir un diff no significa que el ticket esté terminado.
