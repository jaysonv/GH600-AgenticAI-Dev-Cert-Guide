#!/usr/bin/env python3
"""GH-600 study CLI (Python 3.9+, standard library only).

  python gh600.py cards [-d N] [--limit 20] [--all]   Leitner flashcards (spaced repetition)
  python gh600.py practice [-d N] [--limit 10] [--missed]   Practice with instant feedback
  python gh600.py exam [-n 60] [--minutes 120]        Timed, blueprint-weighted simulation
  python gh600.py stats                               Progress and weak domains

Progress is stored in ./.state (git-ignored).
"""
import argparse
import datetime as dt
import glob
import json
import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATE = ROOT / ".state"
DOMAINS = {
    1: "Prepare agent architecture and SDLC processes",
    2: "Implement tool use and environment interaction",
    3: "Manage memory, state, and execution",
    4: "Perform evaluation, error analysis, and tuning",
    5: "Orchestrate multi-agent coordination",
    6: "Implement guardrails and accountability",
}
# Midpoints of the published ranges (15-20, 20-25, 10-15, 15-20, 15-20, 10-15).
WEIGHTS = {1: 0.175, 2: 0.225, 3: 0.125, 4: 0.175, 5: 0.175, 6: 0.125}
INTERVALS = {1: 0, 2: 1, 3: 3, 4: 7, 5: 14}  # Leitner box -> days until due
LETTERS = "ABCDEFGH"


# ---------- data ----------
def _load(pattern):
    items = []
    for p in sorted(glob.glob(str(ROOT / pattern))):
        items += json.loads(Path(p).read_text(encoding="utf-8"))
    return items


def load_cards():
    return _load("flashcards/domain-*.json")


def load_questions():
    return _load("simulator/questions/domain-*.json")


def _state(name, default):
    f = STATE / name
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else default


def _save(name, data):
    STATE.mkdir(exist_ok=True)
    (STATE / name).write_text(json.dumps(data, indent=1), encoding="utf-8")


def ask_input(msg):
    try:
        return input(msg)
    except (EOFError, KeyboardInterrupt):
        print()
        return "q"


# ---------- questions ----------
def grade(q, ans):
    """ans is a list of 0-based option indices (ordered for 'order' questions)."""
    if q["type"] == "order":
        return list(ans) == list(q["a"])
    return sorted(set(ans)) == sorted(q["a"])


def parse_answer(q, raw):
    raw = raw.strip().upper()
    n = len(q["o"])
    try:
        if q["type"] == "order":
            ans = [int(x) - 1 for x in raw.replace(",", " ").split()]
            ok = sorted(ans) == list(range(n))
        else:
            ans = [LETTERS.index(c) for c in raw.replace(",", "").replace(" ", "")]
            ok = bool(ans) and all(0 <= i < n for i in ans)
            ok = ok and (len(set(ans)) == 1 if q["type"] == "single" else len(set(ans)) >= 1)
    except ValueError:
        return None
    return ans if ok else None


def label(q, i):
    return str(i + 1) if q["type"] == "order" else LETTERS[i]


def show_question(q, n, total):
    print(f"\nQ{n}/{total}  [Domain {q['d']}]\n{q['q']}")
    if q["type"] == "multi":
        print("  (select all that apply, e.g. A,C)")
    if q["type"] == "order":
        print("  (type the correct sequence of numbers, e.g. 3 1 2 4)")
    for i, o in enumerate(q["o"]):
        print(f"  {label(q, i)}. {o}")


def ask_question(q, n, total, allow_skip=False):
    """Return list of indices, 'skip' or 'quit'."""
    show_question(q, n, total)
    hint = "answer" + (", s=skip" if allow_skip else "") + ", q=quit"
    while True:
        raw = ask_input(f"> ({hint}) ").strip()
        if raw.lower() == "q":
            return "quit"
        if allow_skip and raw.lower() == "s":
            return "skip"
        ans = parse_answer(q, raw)
        if ans is not None:
            return ans
        print("  Invalid input, try again.")


def correct_text(q):
    return ", ".join(label(q, i) for i in q["a"])


def feedback(q, ok):
    print("  Correct." if ok else f"  Incorrect. Correct answer: {correct_text(q)}")
    print(f"  Why: {q['e']}")
    if q.get("ref"):
        print(f"  Ref: {q['ref']}")


def record(mode, per_domain):
    hist = _state("results.json", [])
    hist.append({"when": dt.datetime.now().isoformat(timespec="seconds"), "mode": mode, "domains": per_domain})
    _save("results.json", hist)


def update_missed(wrong_ids, right_ids):
    missed = set(_state("missed.json", []))
    missed |= set(wrong_ids)
    missed -= set(right_ids)
    _save("missed.json", sorted(missed))


# ---------- commands ----------
def cmd_practice(args):
    qs = load_questions()
    if args.domain:
        qs = [q for q in qs if q["d"] == args.domain]
    if args.missed:
        ids = set(_state("missed.json", []))
        qs = [q for q in qs if q["id"] in ids]
    if not qs:
        print("No questions match.")
        return 1
    random.shuffle(qs)
    qs = qs[: args.limit]
    per, wrong, right = {}, [], []
    for n, q in enumerate(qs, 1):
        ans = ask_question(q, n, len(qs))
        if ans == "quit":
            break
        ok = grade(q, ans)
        feedback(q, ok)
        c, t = per.get(str(q["d"]), [0, 0])
        per[str(q["d"])] = [c + ok, t + 1]
        (right if ok else wrong).append(q["id"])
    if per:
        record("practice", per)
        update_missed(wrong, right)
        tot = sum(v[1] for v in per.values())
        print(f"\nScore: {sum(v[0] for v in per.values())}/{tot}")
    return 0


def pick_exam(qs, n):
    """Choose n questions with domain quotas that follow the blueprint weights."""
    by = {d: [q for q in qs if q["d"] == d] for d in DOMAINS}
    quota = {d: WEIGHTS[d] * n for d in DOMAINS}
    base = {d: min(int(quota[d]), len(by[d])) for d in DOMAINS}
    rem = n - sum(base.values())
    order = sorted(DOMAINS, key=lambda d: quota[d] - int(quota[d]), reverse=True)
    while rem > 0:
        moved = False
        for d in order:
            if rem > 0 and base[d] < len(by[d]):
                base[d] += 1
                rem -= 1
                moved = True
        if not moved:
            break
    picked = []
    for d in DOMAINS:
        picked += random.sample(by[d], base[d])
    random.shuffle(picked)
    return picked


def cmd_exam(args):
    bank = load_questions()
    n = min(args.questions, len(bank))
    minutes = args.minutes if args.minutes else round(120 * n / 60)
    qs = pick_exam(bank, n)
    print(f"GH-600 simulation: {len(qs)} questions, {minutes} minutes. No feedback until the end.")
    print("Weighted by the published domain ranges. Questions are original practice items.")
    ask_input("Press Enter to start... ")
    deadline = time.time() + minutes * 60
    answers, skipped = {}, []
    queue = list(enumerate(qs, 1))
    quit_early = False
    for phase in (0, 1):  # phase 1 revisits skipped items
        for n_i, q in queue:
            if time.time() > deadline:
                print("\nTime is up.")
                quit_early = True
                break
            left = int((deadline - time.time()) / 60)
            print(f"\n[{left} min left]", end="")
            ans = ask_question(q, n_i, len(qs), allow_skip=(phase == 0))
            if ans == "quit":
                quit_early = True
                break
            if ans == "skip":
                skipped.append((n_i, q))
                continue
            answers[q["id"]] = ans
        if quit_early or not skipped:
            break
        queue, skipped = skipped, []
        print("\nReturning to skipped questions...")
    per, wrong, right = {}, [], []
    for q in qs:
        ans = answers.get(q["id"])
        ok = ans is not None and grade(q, ans)
        c, t = per.get(str(q["d"]), [0, 0])
        per[str(q["d"])] = [c + ok, t + 1]
        (right if ok else wrong).append(q["id"])
    record("exam", per)
    update_missed(wrong, right)
    total_c = sum(v[0] for v in per.values())
    pct = 100 * total_c / len(qs)
    print(f"\n=== Result: {total_c}/{len(qs)} ({pct:.0f}%) ===")
    for d in DOMAINS:
        c, t = per.get(str(d), [0, 0])
        if t:
            print(f"  D{d} {DOMAINS[d][:48]:<48} {c}/{t} ({100*c/t:.0f}%)")
    print("The real exam uses scaled scoring (pass = 700 of 1000), so this percentage is only a guide.")
    print("Aim for 80%+ here and 70%+ in every domain. Review misses with: python gh600.py practice --missed")
    return 0


def cmd_cards(args):
    cards = load_cards()
    if args.domain:
        cards = [c for c in cards if c["d"] == args.domain]
    st = _state("cards.json", {})
    today = dt.date.today()
    due = [c for c in cards if args.all or st.get(c["id"], {}).get("due", "0000-00-00") <= today.isoformat()]
    if not due:
        print("Nothing due. Nice. Use --all to review anyway.")
        return 0
    random.shuffle(due)
    due = due[: args.limit]
    known = 0
    for n, c in enumerate(due, 1):
        print(f"\nCard {n}/{len(due)}  [Domain {c['d']}]\n  {c['front']}")
        if ask_input("  (Enter to reveal, q to quit) ").strip().lower() == "q":
            break
        print(f"  -> {c['back']}")
        r = ask_input("  Did you know it? [y/n/q] ").strip().lower()
        if r == "q":
            break
        box = st.get(c["id"], {}).get("box", 1)
        box = min(5, box + 1) if r.startswith("y") else 1
        known += r.startswith("y")
        st[c["id"]] = {"box": box, "due": (today + dt.timedelta(days=INTERVALS[box])).isoformat()}
        _save("cards.json", st)
    print(f"\nKnew {known} cards this session.")
    return 0


def cmd_stats(_args):
    qs, cards = load_questions(), load_cards()
    print(f"Content: {len(cards)} flashcards, {len(qs)} questions")
    hist = _state("results.json", [])
    if not hist:
        print("No attempts yet. Try: python gh600.py practice")
    else:
        agg = {}
        for h in hist:
            for d, (c, t) in h["domains"].items():
                a = agg.setdefault(d, [0, 0])
                a[0] += c
                a[1] += t
        print(f"Attempts: {len(hist)}\n\nAccuracy by domain (all attempts):")
        for d in DOMAINS:
            c, t = agg.get(str(d), [0, 0])
            if t:
                pct = 100 * c / t
                flag = "  <- study more" if pct < 70 else ""
                print(f"  D{d} {DOMAINS[d]:<48} {c}/{t} ({pct:.0f}%) weight~{WEIGHTS[d]*100:.0f}%{flag}")
            else:
                print(f"  D{d} {DOMAINS[d]:<48} not attempted")
        exams = [h for h in hist if h["mode"] == "exam"]
        if exams:
            last = exams[-1]["domains"]
            c = sum(v[0] for v in last.values())
            t = sum(v[1] for v in last.values())
            print(f"\nLast exam simulation: {c}/{t} ({100*c/t:.0f}%)")
    st = _state("cards.json", {})
    boxes = {b: 0 for b in range(1, 6)}
    for v in st.values():
        boxes[v["box"]] += 1
    print("\nFlashcard boxes (1=new/missed ... 5=mastered):", boxes)
    print("Missed questions queued:", len(_state("missed.json", [])))
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description="GH-600 study CLI")
    p.add_argument("--seed", type=int, help="random seed (for reproducibility)")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("cards", help="spaced-repetition flashcards")
    c.add_argument("-d", "--domain", type=int, choices=DOMAINS)
    c.add_argument("--limit", type=int, default=20)
    c.add_argument("--all", action="store_true", help="ignore due dates")
    c.set_defaults(fn=cmd_cards)
    q = sub.add_parser("practice", help="practice with instant feedback")
    q.add_argument("-d", "--domain", type=int, choices=DOMAINS)
    q.add_argument("--limit", type=int, default=10)
    q.add_argument("--missed", action="store_true", help="only questions you missed before")
    q.set_defaults(fn=cmd_practice)
    e = sub.add_parser("exam", help="timed exam simulation")
    e.add_argument("-n", "--questions", type=int, default=60)
    e.add_argument("--minutes", type=int, help="default scales 120 min per 60 questions")
    e.set_defaults(fn=cmd_exam)
    s = sub.add_parser("stats", help="progress summary")
    s.set_defaults(fn=cmd_stats)
    args = p.parse_args(argv)
    if args.seed is not None:
        random.seed(args.seed)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
