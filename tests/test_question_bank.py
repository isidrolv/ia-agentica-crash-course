import unittest

from quiz_core import filter_questions, load_questions, localized, score_summary


class QuestionBankTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.questions = load_questions()

    def test_bank_has_at_least_80_unique_bilingual_questions(self):
        self.assertGreaterEqual(len(self.questions), 80)
        ids = [question["id"] for question in self.questions]
        self.assertEqual(len(ids), len(set(ids)))
        for question in self.questions:
            for field in ("level", "category", "question", "answer", "explanation"):
                self.assertTrue(question[field]["es"].strip(), (question["id"], field, "es"))
                self.assertTrue(question[field]["en"].strip(), (question["id"], field, "en"))

    def test_levels_are_populated_and_filterable(self):
        for level in ("basic", "intermediate", "advanced"):
            self.assertTrue(filter_questions(self.questions, level))
        self.assertGreaterEqual(len(filter_questions(self.questions, "basic")), 15)
        self.assertGreaterEqual(len(filter_questions(self.questions, "intermediate")), 15)
        self.assertGreaterEqual(len(filter_questions(self.questions, "advanced")), 15)

    def test_english_level_filter(self):
        filtered = filter_questions(self.questions, "intermediate")
        self.assertTrue(all("Intermediate" in question["level"]["en"] for question in filtered))

    def test_localization_and_scoring(self):
        self.assertTrue(localized(self.questions[0], "question", "es"))
        self.assertTrue(localized(self.questions[0], "question", "en"))
        result = score_summary([{"recalled": True}, {"recalled": False}])
        self.assertEqual((result["correct"], result["review"], result["percent"]), (1, 1, 50.0))


if __name__ == "__main__":
    unittest.main()
