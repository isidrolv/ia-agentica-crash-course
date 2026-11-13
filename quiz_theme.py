"""Shared color themes for the Tkinter quiz interfaces."""

from tkinter import ttk


THEMES = {
    "dark": {
        "background": "#101827",
        "surface": "#1b2940",
        "input": "#142137",
        "foreground": "#edf3ff",
        "muted": "#aab8ce",
        "accent": "#5eead4",
        "accent_text": "#062a2b",
        "border": "#35445e",
        "hover": "#2b3d59",
        "trough": "#263650",
    },
    "light": {
        "background": "#f3f6fb",
        "surface": "#ffffff",
        "input": "#ffffff",
        "foreground": "#17243a",
        "muted": "#52627a",
        "accent": "#087f8c",
        "accent_text": "#ffffff",
        "border": "#cbd5e1",
        "hover": "#dce8f2",
        "trough": "#dbe4ee",
    },
    "ocean": {
        "background": "#082f49",
        "surface": "#0d4564",
        "input": "#0a3a56",
        "foreground": "#e0f2fe",
        "muted": "#b8d9ed",
        "accent": "#2dd4bf",
        "accent_text": "#073b43",
        "border": "#25617e",
        "hover": "#176080",
        "trough": "#164e6c",
    },
}

THEME_LABELS = {
    "dark": "Oscuro / Dark",
    "light": "Claro / Light",
    "ocean": "Océano / Ocean",
}


def theme_key_from_label(label):
    for key, display_name in THEME_LABELS.items():
        if label == display_name:
            return key
    return "dark"


def apply_theme(root, theme_key):
    """Apply a named palette to the root window and its ttk widgets."""
    colors = THEMES.get(theme_key, THEMES["dark"])
    style = ttk.Style(root)
    # clam reliably honors palette colors across Windows and other Tk platforms.
    if "clam" in style.theme_names():
        style.theme_use("clam")

    root.configure(background=colors["background"])
    style.configure(".", background=colors["background"], foreground=colors["foreground"])
    style.configure("TFrame", background=colors["background"])
    style.configure("TLabel", background=colors["background"], foreground=colors["foreground"])
    style.configure("Muted.TLabel", background=colors["background"], foreground=colors["muted"])
    style.configure("Title.TLabel", background=colors["background"], foreground=colors["foreground"])
    style.configure("Card.TFrame", background=colors["surface"])
    style.configure("Card.TLabel", background=colors["surface"], foreground=colors["foreground"])
    style.configure("TButton", background=colors["surface"], foreground=colors["foreground"],
                    bordercolor=colors["border"], focuscolor=colors["accent"], padding=(12, 8))
    style.map("TButton",
              background=[("pressed", colors["border"]), ("active", colors["hover"])],
              foreground=[("disabled", colors["muted"]), ("active", colors["foreground"])])
    style.configure("Accent.TButton", background=colors["accent"], foreground=colors["accent_text"],
                    bordercolor=colors["accent"], padding=(14, 9))
    style.map("Accent.TButton",
              background=[("pressed", colors["hover"]), ("active", colors["hover"])],
              foreground=[("active", colors["foreground"])])
    style.configure("TEntry", fieldbackground=colors["input"], foreground=colors["foreground"],
                    insertcolor=colors["foreground"], bordercolor=colors["border"])
    style.configure("TCombobox", fieldbackground=colors["input"], background=colors["surface"],
                    foreground=colors["foreground"], arrowcolor=colors["foreground"],
                    bordercolor=colors["border"])
    style.map("TCombobox",
              fieldbackground=[("readonly", colors["input"])],
              foreground=[("readonly", colors["foreground"])],
              selectbackground=[("readonly", colors["input"])],
              selectforeground=[("readonly", colors["foreground"])])
    style.configure("Horizontal.TProgressbar", background=colors["accent"],
                    troughcolor=colors["trough"], bordercolor=colors["trough"])
    return colors
