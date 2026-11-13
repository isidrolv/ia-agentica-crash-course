"""Tkinter self-test: bilingual quiz, filters, reveal, and score screen."""

import random
import tkinter as tk
from tkinter import messagebox, ttk

from quiz_core import filter_questions, load_questions, localized
from quiz_theme import THEME_LABELS, apply_theme, theme_key_from_label


class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IA Agéntica · Autoevaluación")
        self.geometry("900x650")
        self.minsize(720, 500)
        self.theme_key = "dark"
        apply_theme(self, self.theme_key)
        self.bank = load_questions()
        self.lang = "es"
        self.questions = []
        self.index = 0
        self.results = []
        self._setup()

    def _setup(self):
        self._clear()
        panel = ttk.Frame(self, padding=28)
        panel.pack(fill="both", expand=True)
        ttk.Label(panel, text="IA AGÉNTICA · QUIZ", font=("Segoe UI", 22, "bold")).pack(pady=(16, 8))
        ttk.Label(panel, text=f"{len(self.bank)} tarjetas bilingües | Responde de memoria y evalúate con honestidad").pack(pady=(0, 28))

        form = ttk.Frame(panel, padding=18)
        form.pack()
        ttk.Label(form, text="Idioma / Language").grid(row=0, column=0, sticky="w", padx=8, pady=8)
        self.lang_var = tk.StringVar(value="Español")
        ttk.Combobox(form, textvariable=self.lang_var, values=["Español", "English"], state="readonly", width=22).grid(row=0, column=1, padx=8)
        ttk.Label(form, text="Nivel / Level").grid(row=1, column=0, sticky="w", padx=8, pady=8)
        self.level_var = tk.StringVar(value="Todos / All")
        ttk.Combobox(form, textvariable=self.level_var,
                     values=["Todos / All", "Básico / Basic", "Intermedio / Intermediate", "Avanzado / Advanced"],
                     state="readonly", width=22).grid(row=1, column=1, padx=8)
        ttk.Label(form, text="Tema UI / UI theme").grid(row=2, column=0, sticky="w", padx=8, pady=8)
        self.theme_var = tk.StringVar(value=THEME_LABELS[self.theme_key])
        theme_box = ttk.Combobox(form, textvariable=self.theme_var,
                                 values=list(THEME_LABELS.values()), state="readonly", width=22)
        theme_box.grid(row=2, column=1, padx=8)
        theme_box.bind("<<ComboboxSelected>>", self._on_theme_changed)
        ttk.Label(form, text="Cantidad (0 = todas)").grid(row=3, column=0, sticky="w", padx=8, pady=8)
        self.count_var = tk.StringVar(value="10")
        ttk.Entry(form, textvariable=self.count_var, width=25).grid(row=3, column=1, padx=8)
        ttk.Button(panel, text="Comenzar / Start", command=self._start).pack(pady=24)

    def _on_theme_changed(self, _event=None):
        self.theme_key = theme_key_from_label(self.theme_var.get())
        apply_theme(self, self.theme_key)

    def _clear(self):
        for child in self.winfo_children():
            child.destroy()

    def _start(self):
        self.lang = "en" if self.lang_var.get() == "English" else "es"
        level = {"Todos / All": "all", "Básico / Basic": "basic", "Intermedio / Intermediate": "intermediate", "Avanzado / Advanced": "advanced"}[self.level_var.get()]
        self.questions = filter_questions(self.bank, level)
        try:
            count = int(self.count_var.get())
            if count < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Cantidad inválida", "Usa un entero mayor o igual a cero.")
            return
        random.shuffle(self.questions)
        if count:
            self.questions = self.questions[:count]
        if not self.questions:
            messagebox.showinfo("Sin preguntas", "No hay preguntas para ese filtro.")
            return
        self.index = 0
        self.results = []
        self._question()

    def _question(self):
        self._clear()
        q = self.questions[self.index]
        outer = ttk.Frame(self, padding=28)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text=f"{self.index + 1} / {len(self.questions)}     {localized(q, 'level', self.lang)} · {localized(q, 'category', self.lang)}",
                  font=("Segoe UI", 11, "bold")).pack(anchor="w")
        ttk.Progressbar(outer, maximum=len(self.questions), value=self.index + 1).pack(fill="x", pady=10)
        ttk.Label(outer, text=localized(q, "question", self.lang), wraplength=800,
                  font=("Segoe UI", 18), justify="left").pack(fill="x", pady=(28, 18))
        self.answer = ttk.Label(outer, text="", wraplength=800, font=("Segoe UI", 13), justify="left")
        self.answer.pack(fill="x", pady=12)
        self.reveal_btn = ttk.Button(outer, text="Revelar respuesta / Reveal answer", command=self._reveal)
        self.reveal_btn.pack(pady=15)
        self.grade_row = ttk.Frame(outer)
        ttk.Button(self.grade_row, text="La recordé / Recalled", command=lambda: self._grade(True)).pack(side="left", padx=8)
        ttk.Button(self.grade_row, text="A repasar / Review", command=lambda: self._grade(False)).pack(side="left", padx=8)
        ttk.Button(outer, text="Salir al inicio / Home", command=self._setup).pack(side="bottom", pady=10)

    def _reveal(self):
        q = self.questions[self.index]
        self.answer.configure(text=f"{localized(q, 'answer', self.lang)}\n\n{localized(q, 'explanation', self.lang)}")
        self.reveal_btn.pack_forget()
        self.grade_row.pack(pady=16)

    def _grade(self, recalled):
        self.results.append({"id": self.questions[self.index]["id"], "recalled": recalled})
        self.index += 1
        if self.index == len(self.questions):
            self._results()
        else:
            self._question()

    def _results(self):
        self._clear()
        total = len(self.results)
        correct = sum(r["recalled"] for r in self.results)
        panel = ttk.Frame(self, padding=30)
        panel.pack(fill="both", expand=True)
        title = "Final score" if self.lang == "en" else "Resultado final"
        ttk.Label(panel, text=title, font=("Segoe UI", 23, "bold")).pack(pady=20)
        ttk.Label(panel, text=f"{correct} / {total}  ·  {100 * correct / total:.1f}%",
                  font=("Segoe UI", 20)).pack(pady=10)
        missed = [r["id"] for r in self.results if not r["recalled"]]
        review_label = "Cards to review: " if self.lang == "en" else "Tarjetas para repasar: "
        ttk.Label(panel, text=review_label + (", ".join(missed) if missed else "ninguna / none"), wraplength=800).pack(pady=12)
        ttk.Button(panel, text="Otra sesión / New session", command=self._setup).pack(pady=20)


if __name__ == "__main__":
    QuizApp().mainloop()
