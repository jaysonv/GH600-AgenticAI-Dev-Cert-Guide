#!/usr/bin/env python3
"""Generate the Anki import file and the web app's data.js from the JSON sources."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import gh600  # noqa: E402


def main():
    cards, qs = gh600.load_cards(), gh600.load_questions()
    anki = ROOT / "flashcards" / "anki" / "gh600-flashcards.tsv"
    anki.parent.mkdir(parents=True, exist_ok=True)
    lines = ["#separator:tab", "#html:false", "#tags column:3"]
    for c in cards:
        front, back = c["front"].replace("\t", " "), c["back"].replace("\t", " ")
        lines.append(f"{front}\t{back}\tGH600 domain-{c['d']}")
    anki.write_text("\n".join(lines) + "\n", encoding="utf-8")
    data = {
        "domains": {str(k): v for k, v in gh600.DOMAINS.items()},
        "weights": {str(k): v for k, v in gh600.WEIGHTS.items()},
        "cards": cards,
        "questions": qs,
    }
    out = ROOT / "web" / "data.js"
    out.write_text("window.GH600 = " + json.dumps(data, ensure_ascii=False) + ";\n", encoding="utf-8")
    print(f"wrote {anki.relative_to(ROOT)} and {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
