"""Tkinter study cards with navigation and self-rating, inspired by the reference study mode."""

import tkinter as tk
from tkinter import messagebox, ttk

from quiz_core import filter_questions, load_questions, localized
from quiz_theme import THEME_LABELS, apply_theme, theme_key_from_label


class StudyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IA Agéntica · Modo estudio")
        self.geometry("950x700")
        self.minsize(740, 520)
        self.theme_key = "dark"
        apply_theme(self, self.theme_key)
        self.bank = load_questions()
        self.lang = "es"
        self.cards = []
        self.index = 0
        self.ratings = {}
        self.setup()

    def clear(self):
        for child in self.winfo_children():
            child.destroy()

    def setup(self):
        self.clear()
        frame = ttk.Frame(self, padding=30)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="MODO ESTUDIO · ACTIVE RECALL", font=("Segoe UI", 22, "bold")).pack(pady=20)
        ttk.Label(frame, text="Intenta explicar cada tarjeta antes de revelar la respuesta. Marca si la recordaste.", wraplength=760).pack(pady=10)
        self.language = tk.StringVar(value="Español")
        ttk.Combobox(frame, textvariable=self.language, values=["Español", "English"], state="readonly", width=30).pack(pady=8)
        self.level = tk.StringVar(value="Todos / All")
        ttk.Combobox(frame, textvariable=self.level,
                     values=["Todos / All", "Básico / Basic", "Intermedio / Intermediate", "Avanzado / Advanced"],
                     state="readonly", width=30).pack(pady=8)
        ttk.Label(frame, text="Tema UI / UI theme").pack(pady=(12, 2))
        self.theme_var = tk.StringVar(value=THEME_LABELS[self.theme_key])
        theme_box = ttk.Combobox(frame, textvariable=self.theme_var,
                                 values=list(THEME_LABELS.values()), state="readonly", width=30)
        theme_box.pack(pady=8)
        theme_box.bind("<<ComboboxSelected>>", self._on_theme_changed)
        ttk.Button(frame, text="Estudiar / Study", command=self.start).pack(pady=20)

    def _on_theme_changed(self, _event=None):
        self.theme_key = theme_key_from_label(self.theme_var.get())
        apply_theme(self, self.theme_key)

    def start(self):
        self.lang = "en" if self.language.get() == "English" else "es"
        level = {"Todos / All": "all", "Básico / Basic": "basic", "Intermedio / Intermediate": "intermediate", "Avanzado / Advanced": "advanced"}[self.level.get()]
        self.cards = filter_questions(self.bank, level)
        if not self.cards:
            messagebox.showinfo("Sin tarjetas", "No hay tarjetas para ese nivel.")
            return
        self.index = 0
        self.ratings = {}
        self.card()

    def card(self):
        self.clear()
        q = self.cards[self.index]
        root = ttk.Frame(self, padding=28)
        root.pack(fill="both", expand=True)
        ttk.Label(root, text=f"Tarjeta {self.index + 1}/{len(self.cards)}  ·  {localized(q, 'level', self.lang)}  ·  {localized(q, 'category', self.lang)}",
                  font=("Segoe UI", 11, "bold")).pack(anchor="w")
        ttk.Progressbar(root, maximum=len(self.cards), value=self.index + 1).pack(fill="x", pady=10)
        ttk.Label(root, text=localized(q, "question", self.lang), wraplength=820,
                  font=("Segoe UI", 18), justify="left").pack(fill="x", pady=(34, 18))
        self.back = ttk.Label(root, text="", wraplength=820, font=("Segoe UI", 13), justify="left")
        self.back.pack(fill="x", pady=15)
        self.reveal_button = ttk.Button(root, text="Revelar / Reveal", command=self.reveal)
        self.reveal_button.pack(pady=8)
        rate = ttk.Frame(root)
        self.knew_button = ttk.Button(rate, text="Lo sabía / Knew it", command=lambda: self.rate(True), state="disabled")
        self.knew_button.pack(side="left", padx=6)
        self.review_button = ttk.Button(rate, text="A repasar / Review", command=lambda: self.rate(False), state="disabled")
        self.review_button.pack(side="left", padx=6)
        rate.pack(pady=8)
        nav = ttk.Frame(root)
        ttk.Button(nav, text="◀ Anterior / Previous", command=self.previous, state="normal" if self.index else "disabled").pack(side="left", padx=6)
        ttk.Button(nav, text="Siguiente / Next ▶", command=self.next, state="normal" if self.index < len(self.cards) - 1 else "disabled").pack(side="left", padx=6)
        ttk.Button(nav, text="Finalizar / Finish", command=self.finish).pack(side="left", padx=6)
        nav.pack(side="bottom", pady=12)

    def reveal(self):
        q = self.cards[self.index]
        self.back.configure(text=f"{localized(q, 'answer', self.lang)}\n\n{localized(q, 'explanation', self.lang)}")
        self.knew_button.configure(state="normal")
        self.review_button.configure(state="normal")

    def rate(self, knew):
        self.ratings[self.cards[self.index]["id"]] = knew
        self.next()

    def next(self):
        if self.index < len(self.cards) - 1:
            self.index += 1
            self.card()
        else:
            self.finish()

    def previous(self):
        if self.index > 0:
            self.index -= 1
            self.card()

    def finish(self):
        self.clear()
        total_rated = len(self.ratings)
        knew = sum(self.ratings.values())
        panel = ttk.Frame(self, padding=30)
        panel.pack(fill="both", expand=True)
        ttk.Label(panel, text="Resumen de estudio / Study summary", font=("Segoe UI", 22, "bold")).pack(pady=22)
        ttk.Label(panel, text=f"Recordadas / Recalled: {knew}/{total_rated}   ·   Pendientes / Unrated: {len(self.cards) - total_rated}",
                  font=("Segoe UI", 15)).pack(pady=10)
        missed = [qid for qid, value in self.ratings.items() if not value]
        ttk.Label(panel, text="Para repasar / Review: " + (", ".join(missed) if missed else "—"), wraplength=800).pack(pady=12)
        ttk.Button(panel, text="Volver / Home", command=self.setup).pack(pady=18)


if __name__ == "__main__":
    StudyApp().mainloop()
