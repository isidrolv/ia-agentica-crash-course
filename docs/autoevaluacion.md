# Autoevaluación y banco de reactivos

El [banco de preguntas bilingüe](data/question_bank.json) contiene 100 tarjetas de recuerdo activo:

- 20 de nivel básico, 39 intermedio y 41 avanzado.
- Preguntas, respuestas, explicaciones, categorías y niveles en español e inglés.
- Temas: agentes, herramientas, RAG, Jira, orquestación, seguridad, pruebas paralelas, revisión, confiabilidad y CI/CD.

## Cuatro maneras de practicar

Ejecuta los comandos desde la raíz del proyecto. Los programas de consola usan la biblioteca estándar de Python. Los GUI necesitan `tkinter`.

| Programa | Comando | Enfoque |
|---|---|---|
| Consola | `python quiz_console.py` | Sesión simple filtrada por idioma y nivel. |
| Consola avanzada | `python quiz_console_pro.py --lang es --level advanced --count 15 --save historial.json` | Filtros, semilla reproducible, exportación y repaso de falladas. |
| GUI de examen | `python quiz_gui.py` | Cuestionario gráfico con puntuación, repaso y temas oscuro, claro u océano. |
| GUI de estudio | `python quiz_gui_study.py` | Tarjetas navegables, revelar, autoevaluar y cambiar tema. |

La puntuación es deliberadamente autoevaluada: intenta recordar y explicar la respuesta antes de revelarla. No es una calificación automatizada de texto libre. Para fortalecer la retención, vuelve a las falladas al día siguiente y a los 3, 7, 14 y 30 días.

## Validar y reconstruir

```powershell
python -m unittest discover -s tests -v
python tools/build_question_bank.py
python -m mkdocs build --strict
```
