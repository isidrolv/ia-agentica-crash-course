import unittest

from quiz_theme import THEMES, THEME_LABELS, theme_key_from_label


class QuizThemeTests(unittest.TestCase):
    def test_all_dropdown_labels_map_to_their_theme(self):
        for theme_key, label in THEME_LABELS.items():
            self.assertEqual(theme_key_from_label(label), theme_key)

    def test_unknown_label_falls_back_to_dark(self):
        self.assertEqual(theme_key_from_label("unknown"), "dark")

    def test_each_theme_has_required_color_roles(self):
        required = {"background", "surface", "input", "foreground", "muted", "accent", "accent_text"}
        for palette in THEMES.values():
            self.assertTrue(required.issubset(palette))
            for color in palette.values():
                self.assertRegex(color, r"^#[0-9a-fA-F]{6}$")


if __name__ == "__main__":
    unittest.main()
