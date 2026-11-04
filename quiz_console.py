"""Simple bilingual flashcard quiz for the Agentic AI course."""

from quiz_core import choose_questions, filter_questions, load_questions, localized, print_summary


def main():
    questions = load_questions()
    lang = "en" if input("Idioma / Language [es/en, default es]: ").strip().lower() == "en" else "es"
    level = input("Nivel / Level [todos, básico, intermedio, avanzado]: ").strip() or "all"
    selected = filter_questions(questions, level)
    if not selected:
        print("No hay preguntas para ese nivel / No questions for that level.")
        return
    raw_count = input(f"Número de tarjetas [1-{len(selected)}, Enter=todas]: ").strip()
    count = int(raw_count) if raw_count.isdigit() and int(raw_count) > 0 else None
    selected = choose_questions(selected, count)
    results = []
    for index, question in enumerate(selected, 1):
        level_text = localized(question, "level", lang)
        category = localized(question, "category", lang)
        print(f"\n{index}/{len(selected)} · {level_text} · {category} · {question['id']}")
        print(localized(question, "question", lang))
        input("Enter para revelar la respuesta / Press Enter to reveal...")
        print("\n" + localized(question, "answer", lang))
        rating_prompt = "Did you recall it without help? [y/n]: " if lang == "en" else "¿La recordaste sin ayuda? [s/n]: "
        if input(rating_prompt).strip().lower() in {"s", "si", "sí", "y", "yes"}:
            recalled = True
        else:
            recalled = False
        results.append({"id": question["id"], "recalled": recalled})
        if not recalled:
            print(localized(question, "explanation", lang))
    print_summary(results, lang)


if __name__ == "__main__":
    main()
