"""Configurable console self-test with category/level filters and review export."""

import argparse
import json
import random
from pathlib import Path

from quiz_core import categories, choose_questions, filter_questions, load_questions, localized, print_summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lang", choices=["es", "en"], default="es")
    parser.add_argument("--level", default="all", help="all/basic/intermediate/advanced or nivel en español")
    parser.add_argument("--category", default="all", help="Categoría en español o inglés")
    parser.add_argument("--count", type=int, help="Máximo de tarjetas (por defecto, todas)")
    parser.add_argument("--seed", type=int, help="Semilla para una sesión reproducible")
    parser.add_argument("--review-only", action="store_true", help="Solo tarjetas falladas en sesiones anteriores")
    parser.add_argument("--history", type=Path, default=Path("quiz_history.json"))
    parser.add_argument("--save", type=Path, help="Guardar resultado JSON de esta sesión")
    parser.add_argument("--no-shuffle", action="store_true")
    args = parser.parse_args()
    if args.count is not None and args.count < 1:
        parser.error("--count debe ser un entero mayor que cero")

    questions = load_questions()
    if args.review_only:
        if not args.history.exists():
            print(f"No se encontró historial para repasar: {args.history}")
            return
        history = json.loads(args.history.read_text(encoding="utf-8"))
        sessions = history if isinstance(history, list) else [history]
        last_result = {}
        for session in sessions:
            for entry in session.get("results", []):
                last_result[entry["id"]] = bool(entry.get("recalled"))
        missed = {question_id for question_id, recalled in last_result.items() if not recalled}
        questions = [q for q in questions if q["id"] in missed]
    questions = filter_questions(questions, args.level, args.category)
    if not questions:
        print("No hay tarjetas que coincidan con los filtros.")
        print("Categorías disponibles:", ", ".join(categories(load_questions(), args.lang)))
        return

    chosen = choose_questions(questions, args.count, not args.no_shuffle, args.seed)
    results = []
    lang = args.lang
    print(f"Agentic AI · {len(chosen)} tarjetas · {args.level} · {args.category}")
    for index, question in enumerate(chosen, 1):
        print(f"\n[{index}/{len(chosen)}] {localized(question, 'level', lang)} / {localized(question, 'category', lang)} · {question['id']}")
        print(localized(question, "question", lang))
        input("Enter para revelar / Press Enter to reveal...")
        print("\n" + localized(question, "answer", lang))
        rating_prompt = "Did you recall it without help? [y/n]: " if lang == "en" else "¿La recordaste sin ayuda? [s/n]: "
        recalled = input(rating_prompt).strip().lower() in {"s", "si", "sí", "y", "yes"}
        results.append({"id": question["id"], "recalled": recalled})
        if not recalled:
            print("→ " + localized(question, "explanation", lang))

    summary = print_summary(results, lang)
    if args.save:
        session = {"lang": lang, "level": args.level, "category": args.category,
                   "summary": summary, "results": results}
        previous = []
        if args.save.exists():
            loaded = json.loads(args.save.read_text(encoding="utf-8"))
            previous = loaded if isinstance(loaded, list) else [loaded]
        previous.append(session)
        args.save.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Sesión guardada en {args.save}")


if __name__ == "__main__":
    main()
