# IA Agéntica: curso intensivo de 90 días

Curso práctico para diseñar y construir un pipeline de ingeniería de software orquestado por agentes, desde una historia de Jira hasta revisión y CI/CD con controles humanos.

## Objetivo final

Al terminar, podrás diseñar, instrumentar y explicar un flujo durable y seguro donde un ticket elegible activa agentes con roles específicos: contexto, especificación, planificación, codificación, pruebas en paralelo, revisión y entrega. La automatización propone y ejecuta cambios dentro de permisos explícitos; las puertas de calidad y las aprobaciones necesarias no dependen de que un modelo “se porte bien”.

La aspiración de estar en el 1% superior es un objetivo de desempeño, no una garantía. Se medirá con entregables demostrables, evaluaciones repetibles, seguridad y capacidad de operar el pipeline bajo fallos.

## Contenido

- [`docs/curso-90-dias.md`](docs/curso-90-dias.md): calendario semanal, práctica diaria, repetición espaciada y proyecto final.
- [`docs/PIPELINE_OBJETIVO.md`](docs/PIPELINE_OBJETIVO.md): arquitectura de referencia, agentes, estados, paralelismo, seguridad y CI/CD.
- [`docs/data/question_bank.json`](docs/data/question_bank.json): 100 reactivos en español e inglés.
- [`docs/examples/`](docs/examples/README.md): seis ejercicios guiados básicos, intermedios y avanzados.
- [`tools/build_question_bank.py`](tools/build_question_bank.py): fuente reproducible del banco JSON.

## Cuatro modalidades de autoevaluación

Inspiradas en las cuatro variantes del proyecto de referencia `ArchitecturalInterviewQuestionsAndAswers`, pero implementadas para este curso y su propio esquema de reactivos. No se modificó ni se copió código del repositorio de referencia.

| Programa | Uso |
|---|---|
| `quiz_console.py` | Sesión sencilla en terminal, español/inglés, por nivel y cantidad. |
| `quiz_console_pro.py` | Filtros, semilla reproducible, repaso de falladas y exportación de sesión. |
| `quiz_gui.py` | Examen gráfico con puntuación y lista de tarjetas a repasar. |
| `quiz_gui_study.py` | Tarjetas gráficas con navegación, recuerdo activo y autoevaluación. |

Las tarjetas usan recuperación activa: intenta responder antes de revelar y marca honestamente si lo recordaste. La puntuación es autoevaluada, no una calificación automática de texto libre.

El banco contiene 20 reactivos básicos, 39 intermedios y 41 avanzados. Cada uno tiene pregunta, respuesta, explicación, nivel y categoría tanto en español como en inglés.

## Requisitos y ejecución

Python 3.10 o posterior. Los cuestionarios de consola solo usan la biblioteca estándar. Los GUI requieren que la distribución de Python incluya `tkinter`.

```powershell
python quiz_console.py
python quiz_console_pro.py --lang es --level intermediate --count 12 --save sesion.json
python quiz_console_pro.py --lang en --review-only
python quiz_gui.py
python quiz_gui_study.py
```

Regenerar el banco tras modificar su fuente:

```powershell
python tools/build_question_bank.py
```

## Validación rápida

```powershell
python -m unittest discover -s tests -v
python -m py_compile quiz_core.py quiz_console.py quiz_console_pro.py quiz_gui.py quiz_gui_study.py
```

## Sitio MkDocs

```powershell
python -m pip install -r requirements-mkdocs.txt
python -m mkdocs serve
python -m mkdocs build --strict
```

El contenido publicado vive bajo `docs/`; el sitio generado queda en `site/` y no se versiona.

## Decisión importante del diseño

El agente de pruebas puede trabajar mientras el agente de código implementa, pero en una rama/espacio de trabajo aislado y a partir de criterios y contratos estables. Un integrador determinista ejecuta pruebas en snapshots identificables y corre la suite completa sobre el candidato integrado. Evita que dos agentes sobrescriban los mismos archivos o que un test intermedio e incompleto habilite una entrega.
