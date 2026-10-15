#!/usr/bin/env python3
"""Validate flashcards and question bank. Exit 1 on any problem."""
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import gh600  # noqa: E402

TYPES = {"single", "multi", "order"}


def validate():
    errors = []
    cards, qs = gh600.load_cards(), gh600.load_questions()
    seen = set()
    for c in cards:
        for k in ("id", "d", "front", "back"):
            if not c.get(k):
                errors.append(f"card {c.get('id')}: missing {k}")
        if c.get("d") not in gh600.DOMAINS:
            errors.append(f"card {c.get('id')}: bad domain")
        if not str(c.get("id", "")).startswith(f"D{c.get('d')}-C"):
            errors.append(f"card {c.get('id')}: id prefix must be D{c.get('d')}-C")
        if c.get("id") in seen:
            errors.append(f"duplicate id {c.get('id')}")
        seen.add(c.get("id"))
    for q in qs:
        i = q.get("id")
        for k in ("id", "d", "type", "q", "o", "a", "e"):
            if q.get(k) in (None, "", []):
                errors.append(f"question {i}: missing {k}")
        if i in seen:
            errors.append(f"duplicate id {i}")
        seen.add(i)
        if q.get("d") not in gh600.DOMAINS or not str(i).startswith(f"D{q.get('d')}-Q"):
            errors.append(f"question {i}: bad domain or id prefix")
        if q.get("type") not in TYPES:
            errors.append(f"question {i}: bad type")
            continue
        n = len(q["o"])
        if not 2 <= n <= 8:
            errors.append(f"question {i}: needs 2-8 options")
        if any(not isinstance(x, int) or not 0 <= x < n for x in q["a"]):
            errors.append(f"question {i}: answer index out of range")
        if q["type"] == "single" and len(q["a"]) != 1:
            errors.append(f"question {i}: single needs exactly 1 answer")
        if q["type"] == "multi" and len(set(q["a"])) < 2:
            errors.append(f"question {i}: multi needs 2+ answers")
        if q["type"] == "order" and sorted(q["a"]) != list(range(n)):
            errors.append(f"question {i}: order answer must be a permutation")
        if len(set(q["o"])) != n:
            errors.append(f"question {i}: duplicate options")
    return errors, cards, qs


if __name__ == "__main__":
    errs, cards, qs = validate()
    print(f"{len(cards)} flashcards, {len(qs)} questions")
    cc, qc = Counter(c["d"] for c in cards), Counter(q["d"] for q in qs)
    for d, name in gh600.DOMAINS.items():
        print(f"  D{d}: {cc[d]:>3} cards  {qc[d]:>3} questions  {name}")
    for e in errs:
        print("ERROR:", e)
    sys.exit(1 if errs else 0)
