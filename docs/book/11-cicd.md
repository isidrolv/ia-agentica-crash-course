# Semana 11 — CI/CD y despliegue seguro

**Tiempo sugerido:** 9–11 horas. **Resultado:** pipeline mock de build, validaciones, promoción a staging y rollback, protegido por gates versionados.

## Recuperación antes de aprender

¿Qué diferencia un build fallido de un deploy fallido? ¿Por qué construir el mismo commit de nuevo para staging y producción puede producir artefactos distintos?

## CI, entrega continua y despliegue continuo

**Integración continua (CI)** integra cambios con compilación, pruebas y análisis automáticos. **Entrega continua** conserva una versión validada lista para liberar, normalmente con aprobación. **Despliegue continuo** promueve automáticamente los cambios que cumplen política. Son prácticas relacionadas, pero el nivel de autonomía y riesgo de liberación es diferente.

Una puerta (quality gate) es una condición evaluable: build reproducible, pruebas obligatorias, no hay hallazgos críticos abiertos, revisión independiente, escaneo de secretos limpio y artefacto identificado. El controlador determinista comprueba esas condiciones; el LLM puede resumir resultados, pero no declarar un gate verde por interpretación.

## Artefacto inmutable y procedencia

Construye una sola vez desde commit identificado. Publica un artefacto inmutable por digest (hash), junto con procedencia: repo, commit, pipeline, dependencias, configuración de build y resultados. Promueve ese mismo artefacto entre staging y producción. Si cambia el código, es otro candidato y requiere nuevas pruebas/revisión.

Mantén separación de identidades: el agente de código no puede obtener credenciales de producción. El release controller accede solo al entorno autorizado y usa credenciales efímeras. El merge a rama protegida también debe exigir gates, no solo el estado de Jira.

## Canary, salud y rollback

Un canary entrega a una fracción de tráfico o usuarios. Observa señales como tasa de error, latencia y resultados de negocio comparados con umbrales antes de ampliar. Rollback no es “volver a desplegar” si una migración irreversible ya cambió datos. Diseña migraciones compatibles hacia atrás, backups, forward fixes y un plan de recuperación antes del release.

El rollback debe estar ensayado y su disparador debe ser claro. Por ejemplo: detener promoción si la tasa de error supera el presupuesto durante una ventana. Registra artefacto anterior, decisión, actor, tiempo y validación posterior.

## Ejemplo de política de promoción

```text
CI pasa si: build + unitarias + integración + funcionales + escaneos requeridos.
Merge pasa si: CI pasa + review independiente PASS + cero findings BLOCK.
Staging pasa si: smoke tests OK + SLI dentro de umbral.
Producción pasa si: staging válido + aprobación exigida + canary saludable.
```

No interpretes `review PASS` como deploy. Si una vulnerabilidad crítica falla, el pipeline se detiene aunque todos los tests funcionales estén verdes.

## Práctica deliberada: pipeline de laboratorio

1. Define estados `BUILD`, `TEST`, `SCAN`, `REVIEW`, `STAGING`, `APPROVAL`, `PRODUCTION`, `ROLLBACK`.
2. Escribe una política declarativa y evalúala sobre JSON de resultados mock.
3. Crea escenarios: unit test rojo, integración pendiente, reviewer BLOCK, scan crítico, staging sano, staging degradado y aprobación denegada.
4. Simula creación de artefacto con digest y promueve exactamente el mismo digest a staging.
5. Inyecta fallo en canary; comprueba detención/rollback y genera evidencia de run.

**Criterios de aceptación:** gates evaluados de manera determinista; no se salta una etapa obligatoria; artefacto se identifica por digest; promoción está auditada; producción solicita aprobación según política; rollback fue probado.

## Errores frecuentes

- Confundir CI exitoso con autorización para producción.
- Reconstruir un artefacto distinto por ambiente sin preservar procedencia.
- Permitir que un agente con permiso de PR también administre secrets del deploy.
- Probar rollback solo en documentación y no con una simulación.

## Recuerdo activo y Feynman

Explica CI, entrega continua y despliegue continuo. ¿Qué es un artefacto inmutable? ¿Cómo decides detener un canary? ¿Qué limita un rollback si hay cambios de esquema? Dibuja gates desde commit a producción.
