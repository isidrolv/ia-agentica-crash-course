# Semana 8 — Agente de pruebas en paralelo

**Tiempo sugerido:** 9–12 horas. **Resultado:** pruebas trazables a criterios, escritas en paralelo sin conflictos y ejecutadas sobre snapshots identificables.

## Recuperación antes de aprender

¿Quién define el oráculo esperado: el test o la implementación? ¿Por qué un resultado verde del commit N no prueba que el commit N+1 sea correcto?

## Tipos de prueba y qué riesgo cubren

- **Unitaria:** verifica una función/clase aislada con dependencias controladas. Rápida y precisa para reglas de negocio.
- **Integración:** verifica colaboración real entre módulos, base de datos, colas o servicios. Detecta incompatibilidades de contrato/configuración.
- **Funcional/aceptación:** comprueba comportamiento visible frente a los criterios; puede atravesar API/UI con entorno representativo.
- **Contrato:** confirma que productor y consumidor acuerdan schema y semántica.
- **Regresión:** protege comportamientos ya corregidos frente a cambios futuros.

No persigas solo cobertura de líneas. Una línea cubierta sin una aserción significativa no demuestra el resultado esperado.

## Oráculo y trazabilidad

Para cada criterio, define entradas, precondiciones, acción y resultado esperado. Deriva el esperado del requisito aprobado, no de observar qué hace el código. Incluye casos positivos, negativos, fronteras, estados y autorización. Una matriz sencilla:

| Criterio | Nivel | Caso | Resultado esperado |
|---|---|---|---|
| AC-1 enlace válido | Funcional | token vigente y no usado | flujo de reset aceptado |
| AC-2 no enumeración | Integración | email existe/no existe | misma respuesta pública |
| AC-3 enlace vencido | Unitaria/funcional | token expirado | no autentica; ofrece reinicio |

## Paralelizar con un coder

El test author puede iniciar al aprobar contratos y criterios. Trabaja en branch/worktree propio desde el mismo commit base, sin editar los archivos del coder. Puede escribir pruebas que inicialmente fallen o incluso no compilen; debe etiquetar supuestos, interfaces pendientes y snapshot probado.

Cada resultado debe incluir hash del código, hash/versión de tests, ambiente, comando, salida y clasificación. Al cambiar el código, las pruebas afectadas quedan **stale** hasta ejecutarse nuevamente. Un integrador determinista combina ramas y corre la suite final tras `CODE_COMPLETE`. No habilites merge/deploy por un conjunto parcial ejecutado en un árbol inestable.

El ciclo de feedback puede ser continuo:

```text
Contrato/criterio → test draft ─┐
                               ├→ snapshot integrado → resultado → coder
Implementación → commit ───────┘
```

Una falla intermedia es información, no veredicto final. Mantén un caso reproducible y evita crear loops sin límite: usa máximo de iteraciones y escala si criterio/implementación están en conflicto.

## Flakiness, fixtures y mutación

Una prueba flaky pasa/falla sin cambio relevante, por carreras, reloj, red o datos compartidos. Registra frecuencia y cuarentena con fecha/propietario; no la marques como aprobada por reintentar hasta obtener verde. Usa datos sintéticos y fixtures aislados. **Mutation testing** introduce cambios deliberadamente incorrectos para medir si assertions los detectan; mutantes sobrevivientes señalan huecos posibles, no automáticamente mala calidad.

## Práctica deliberada

### Ejercicio A — Matriz de pruebas (60 min)

Usa los criterios `SHOP-214`. Añade pruebas unitarias de token, integración con almacenamiento mock, funcionales de respuesta neutra y contrato de API. Incluye límites, token usado, token expirado y solicitud repetida. Vincula cada prueba con criterio e id.

### Ejercicio B — Simulación paralela (90 min)

1. Crea commit base `B` y branch `agent-code`/`agent-tests`.
2. El test author escribe casos desde contrato; el coder implementa en su branch.
3. Corre tests sobre snapshot `B + tests`, guarda resultado `FAIL` con hash.
4. Integra implementación en snapshot `C + tests`; corre pruebas.
5. Modifica coder a `C2`; demuestra que el resultado anterior no se presenta como vigente.

**Criterios de aceptación:** trazabilidad total de criterios críticos; las pruebas no comparten archivos de escritura; resultados tienen hash; error reproducible vuelve al coder; suite final usa candidato integrado y actualizado.

## Errores frecuentes

- Escribir aserciones copiando la lógica del código y compartir el mismo bug.
- Mezclar branch mutable de coder con tests en ejecución.
- Ocultar tests flaky para obtener un gate verde.
- Ejecutar pruebas finales contra commit distinto del que se revisa.

## Recuerdo activo

Sin notas, da un ejemplo que necesita cada tipo de prueba. ¿Qué evidencia invalida un resultado anterior? ¿Cómo evitas la colisión de archivos? ¿Qué significa `stale`? Explica por qué test author puede arrancar antes, pero el gate final espera candidato estable.
