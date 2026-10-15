# GH600-AgenticAI-Dev-Cert-Guide

A self-contained study kit for **GitHub Certified: Agentic AI Developer (exam GH-600, "Developing in Agentic AI Systems")**: lessons, flashcards, hands-on labs and an exam simulator, organized around the six official skill domains.

> **Unofficial.** Not affiliated with or endorsed by GitHub or Microsoft. Questions are original practice items, not real exam content. Docs change quickly, so verify anything marked *verify* against [Microsoft Learn](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-600) and [GitHub Docs](https://docs.github.com/en/copilot). Content last checked against the published study guide on 15 Oct 2026.

## Exam at a glance

120 minutes, passing score 700 (scaled), proctored, English, Pearson VUE. Details and sources: [docs/00-exam-overview.md](docs/00-exam-overview.md).

| # | Domain | Weight | Lesson | Lab(s) |
|---|---|---|---|---|
| 1 | Prepare agent architecture and SDLC processes | 15-20% | [01](lessons/01-agent-architecture-and-sdlc.md) | [1](labs/lab-01-instructions-and-agent-boundaries/README.md), [2](labs/lab-02-plan-then-execute/README.md) |
| 2 | Implement tool use and environment interaction | 20-25% | [02](lessons/02-tool-use-and-environment.md) | [3](labs/lab-03-environment-and-firewall/README.md), [4](labs/lab-04-mcp-servers/README.md), [5](labs/lab-05-safe-execution-paths/README.md) |
| 3 | Manage memory, state, and execution | 10-15% | [03](lessons/03-memory-state-and-execution.md) | [6](labs/lab-06-memory-and-state/README.md) |
| 4 | Perform evaluation, error analysis, and tuning | 15-20% | [04](lessons/04-evaluation-error-analysis-and-tuning.md) | [7](labs/lab-07-evaluate-and-tune/README.md) |
| 5 | Orchestrate multi-agent coordination | 15-20% | [05](lessons/05-multi-agent-coordination.md) | [8](labs/lab-08-multi-agent/README.md) |
| 6 | Implement guardrails and accountability | 10-15% | [06](lessons/06-guardrails-and-accountability.md) | [9](labs/lab-09-guardrails-and-autonomy/README.md) |

## What is inside

| Path | Contents |
|---|---|
| `docs/` | Exam overview, 4-week study plan, cheat sheet, sources |
| `lessons/` | Six lessons mapped one-to-one to the official objectives, with exam traps and self-checks |
| `labs/` | Nine hands-on labs plus a tiny sandbox app, each with a "Break it" drill |
| `flashcards/` | **123 cards** (JSON) and an Anki import file (`flashcards/anki/gh600-flashcards.tsv`) |
| `simulator/questions/` | **90 questions** (single, multi-select, ordering) with explanations and references |
| `gh600.py` | CLI: spaced-repetition cards, practice, timed weighted exam, stats. Python 3.9+, no dependencies |
| `web/` | Browser study desk (open `web/index.html`; deployable to GitHub Pages) |
| `tools/`, `tests/` | Content validator, builder, unit tests |

## Quick start

```bash
git clone https://github.com/<you>/GH600-AgenticAI-Dev-Cert-Guide.git
cd GH600-AgenticAI-Dev-Cert-Guide

python gh600.py cards                  # due flashcards (add -d 2 for one domain)
python gh600.py practice -d 2          # instant-feedback practice
python gh600.py exam                   # 60 questions, 120 minutes, weighted by domain
python gh600.py practice --missed      # drill what you got wrong
python gh600.py stats                  # weak domains

open web/index.html                    # or double-click it; no server needed
```

Import `flashcards/anki/gh600-flashcards.tsv` into Anki (File > Import). Tags carry the domain.

## Suggested path

1. Read [docs/00-exam-overview.md](docs/00-exam-overview.md) and the official study guide.
2. Follow [docs/01-study-plan.md](docs/01-study-plan.md) (written for a mid-November exam).
3. For each domain: lesson, then lab, then cards, then practice questions.
4. Two full timed simulations in the last two weeks, then review misses.
5. Try every question type in the [official exam sandbox](https://ghcertdemo.starttest.com/).

## Publishing this as your own repo

```bash
gh repo create GH600-AgenticAI-Dev-Cert-Guide --public --source=. --push
# optional: Settings > Pages > Source: GitHub Actions  (the web study desk deploys from /web)
```

## Maintaining content

Edit `flashcards/domain-N.json` or `simulator/questions/domain-N.json`, then run
`python tools/validate.py && python tools/build.py && python -m unittest discover tests`. CI does the same. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Known limits

- Domain 2 is the largest, but also the most UI-dependent. GitHub menus and policy names move, so labs say *verify* where I could not confirm current wording.
- Copilot Memory was in public preview when checked, and the exam may include commonly used preview features.
- 90 questions is a practice set, not a guarantee of coverage. Expand it from the docs as you study; writing your own questions is excellent revision.
- The simulator's percentage is not the real scaled score.

License: MIT.
