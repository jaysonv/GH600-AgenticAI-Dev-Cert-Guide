import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import gh600  # noqa: E402
import validate  # noqa: E402


class ContentTests(unittest.TestCase):
    def test_content_valid(self):
        errors, _, _ = validate.validate()
        self.assertEqual(errors, [])

    def test_weights_sum_to_one(self):
        self.assertAlmostEqual(sum(gh600.WEIGHTS.values()), 1.0)

    def test_every_domain_has_enough_content(self):
        for d in gh600.DOMAINS:
            self.assertGreaterEqual(sum(c["d"] == d for c in gh600.load_cards()), 15)
            self.assertGreaterEqual(sum(q["d"] == d for q in gh600.load_questions()), 10)

    def test_exam_selection_follows_weights(self):
        random.seed(1)
        qs = gh600.load_questions()
        picked = gh600.pick_exam(qs, 60)
        self.assertEqual(len(picked), 60)
        self.assertEqual(len({q["id"] for q in picked}), 60)
        for d in gh600.DOMAINS:
            share = sum(q["d"] == d for q in picked) / 60
            self.assertLess(abs(share - gh600.WEIGHTS[d]), 0.1)

    def test_grading(self):
        single = {"type": "single", "a": [1]}
        multi = {"type": "multi", "a": [0, 2]}
        order = {"type": "order", "a": [2, 0, 1]}
        self.assertTrue(gh600.grade(single, [1]))
        self.assertFalse(gh600.grade(single, [0]))
        self.assertTrue(gh600.grade(multi, [2, 0]))
        self.assertFalse(gh600.grade(multi, [0]))
        self.assertTrue(gh600.grade(order, [2, 0, 1]))
        self.assertFalse(gh600.grade(order, [0, 1, 2]))

    def test_parse_answer(self):
        q = {"type": "multi", "o": ["a", "b", "c", "d"]}
        self.assertEqual(gh600.parse_answer(q, "a, c"), [0, 2])
        self.assertIsNone(gh600.parse_answer(q, "z"))
        o = {"type": "order", "o": ["a", "b", "c"]}
        self.assertEqual(gh600.parse_answer(o, "3 1 2"), [2, 0, 1])
        self.assertIsNone(gh600.parse_answer(o, "1 1 2"))


class SimulatorFlowTests(unittest.TestCase):
    def _run(self, skip_first):
        import contextlib
        import io
        import tempfile
        calls = set()

        def fake_ask(q, n, total, allow_skip=False):
            if skip_first and allow_skip and q["id"] not in calls:
                calls.add(q["id"])
                return "skip"
            return list(q["a"])

        old = (gh600.ask_question, gh600.ask_input, gh600.STATE)
        gh600.ask_question = fake_ask
        gh600.ask_input = lambda msg: ""
        gh600.STATE = Path(tempfile.mkdtemp())
        try:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                gh600.main(["--seed", "7", "exam", "-n", "12"])
            return buf.getvalue()
        finally:
            gh600.ask_question, gh600.ask_input, gh600.STATE = old

    def test_perfect_exam(self):
        self.assertIn("Result: 12/12", self._run(False))

    def test_skipped_questions_are_revisited(self):
        self.assertIn("Result: 12/12", self._run(True))


if __name__ == "__main__":
    unittest.main()
