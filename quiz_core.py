"""Shared loading, filtering, localization, and scoring helpers for the quizzes."""

import json
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BANK_PATH = ROOT / "docs" / "data" / "question_bank.json"
LANGS = {"es": "es", "en": "en"}
LEVELS = {
    "basic": "Básico", "básico": "Básico", "basico": "Básico", "basic-en": "Basic",
    "intermediate": "Intermedio", "intermedio": "Intermedio", "intermediate-en": "Intermediate",
    "advanced": "Avanzado", "avanzado": "Avanzado", "advanced-en": "Advanced",
}


def load_questions(path=BANK_PATH):
    with Path(path).open(encoding="utf-8") as stream:
        questions = json.load(stream)
    if not isinstance(questions, list) or not questions:
        raise ValueError("El banco debe ser una lista JSON no vacía.")
    return questions


def localized(question, field, lang):
    value = question[field]
    return value.get(lang, value.get("es", "")) if isinstance(value, dict) else value


def filter_questions(questions, level="all", category="all"):
    result = list(questions)
    if level and level.lower() not in {"all", "todos", "todas"}:
        key = LEVELS.get(level.lower(), level)
        result = [q for q in result if key.casefold() in {v.casefold() for v in q["level"].values()}]
    if category and category.lower() not in {"all", "todos", "todas"}:
        result = [q for q in result if category.casefold() in {v.casefold() for v in q["category"].values()}]
    return result


def categories(questions, lang):
    return sorted({localized(q, "category", lang) for q in questions})


def levels(questions, lang):
    return sorted({localized(q, "level", lang) for q in questions})


def choose_questions(questions, count=None, shuffle=True, seed=None):
    selected = list(questions)
    if seed is not None:
        random.Random(seed).shuffle(selected)
    elif shuffle:
        random.shuffle(selected)
    if count is not None:
        selected = selected[:max(0, min(count, len(selected)))]
    return selected


def score_summary(results):
    total = len(results)
    correct = sum(bool(item["recalled"]) for item in results)
    return {"total": total, "correct": correct, "review": total - correct,
            "percent": (100 * correct / total) if total else 0.0}


def print_summary(results, lang="es"):
    summary = score_summary(results)
    if lang == "en":
        print(f"\nResult: {summary['correct']}/{summary['total']} recalled ({summary['percent']:.1f}%).")
        print(f"Review cards: {summary['review']}.")
    else:
        print(f"\nResultado: {summary['correct']}/{summary['total']} recordadas ({summary['percent']:.1f}%).")
        print(f"Tarjetas para repasar: {summary['review']}.")
    return summary
