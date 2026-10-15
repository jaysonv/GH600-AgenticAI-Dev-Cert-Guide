# Study plan: 15 Oct to the 3rd week of November 2026

Assumes ~10-12 hours per week (about 1.5 h on weekdays plus a longer weekend block). Stretch or compress as needed. The 3rd week of November is 16-22 Nov.

| When | Focus | Do |
|---|---|---|
| **Thu 15 - Sun 18 Oct** (setup) | Orientation | Read `docs/00-exam-overview.md`. Schedule the exam. Launch the official sandbox. Skim the official study guide. Finish the three Microsoft Learn modules listed in `docs/03-sources.md`. If GitHub Copilot is new to you, take GH-300-level material first |
| **Week 1: 19-25 Oct** | Domain 1 + start Domain 2 | Lesson 1, Labs 1-2. Lesson 2 up to MCP. Cards for D1. 16 D1 practice questions |
| **Week 2: 26 Oct - 1 Nov** | Domain 2 (largest) | Finish Lesson 2, Labs 3-5. Cards D2. 21 D2 questions. Keep a "mistakes" list |
| **Week 3: 2-8 Nov** | Domains 3 and 4 | Lessons 3-4, Labs 6-7. Cards D3-D4. Practice D3, D4 |
| **Week 4: 9-15 Nov** | Domains 5 and 6 + full mocks | Lessons 5-6, Labs 8-9. Take one full timed exam (`python gh600.py exam`) on 12 Nov and a second on 14-15 Nov. Re-read cheat sheet |
| **Exam week: 16-22 Nov** | Taper | Cards for weak domains only. Re-do the missed-question set. Sleep. Check ID and test the proctoring software the day before |

## Daily loop (works for any domain)

1. 10 min: flashcards due today (`python gh600.py cards`).
2. 40-60 min: lesson section or lab.
3. 15 min: practice questions for that domain (`python gh600.py practice -d N`).
4. 5 min: write every wrong answer as one sentence in your own words.

## Readiness checklist

- [ ] 80%+ on two full timed simulator runs
- [ ] Every domain at 70%+ in `python gh600.py stats`
- [ ] You can explain, from memory: plan/execute gate, MCP config keys, `COPILOT_MCP_` secrets, copilot-setup-steps, cloud agent branch/PR limits, Copilot Memory rules, autonomy levels
- [ ] You completed every lab at least once on a real repo
- [ ] You tried all question types in the official sandbox
