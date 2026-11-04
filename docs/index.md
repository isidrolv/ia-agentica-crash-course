# IA Agéntica para ingeniería de software

Aprende a diseñar un flujo de ingeniería donde varios agentes colaboran para llevar una historia desde Jira hasta un cambio revisado y validado por CI/CD.

## Ruta de aprendizaje

1. [Sigue el plan de 90 días](curso-90-dias.md), con práctica semanal y repasos espaciados.
2. [Lee el libro de 13 capítulos](book/README.md) para desarrollar cada tema con ejemplos y prácticas.
3. [Estudia la arquitectura objetivo](PIPELINE_OBJETIVO.md): roles, estados, seguridad y gates.
4. [Practica con escenarios](examples/README.md), desde preparar contexto hasta bloquear un despliegue inseguro.
5. [Evalúa tu progreso](autoevaluacion.md) con el banco bilingüe y los cuatro cuestionarios.

## El pipeline en una vista

**Historia elegible en Jira → contexto verificable → plan → agente de código + agente de pruebas en paralelo → integración → code review independiente → CI/CD con gates y aprobación por riesgo.**

El agente de pruebas puede preparar casos mientras se programa, pero la suite final debe correr sobre el candidato integrado y quedar vinculada a su commit. El review habilita el pipeline; no despliega por sí solo a producción.

## Ejecutar localmente

Desde la raíz del proyecto:

```powershell
python quiz_console.py
python quiz_console_pro.py --lang es --level intermediate --count 12
```

Para abrir el sitio mientras editas:

```powershell
python -m pip install -r requirements-mkdocs.txt
python -m mkdocs serve
```
