# Lab 7: Evaluate, analyze failures, tune (Domain 4)

**Goal:** run a small evaluation set, classify failures and improve one lever at a time.

## Steps

1. Create five issues from `labs/sandbox-app/ISSUES.md` (#1, #2, #3, #5, #6). This is your **evaluation set**.
2. Copy `assets/eval-sheet.csv`. For each task define expected outcome and constraints *before* running.
3. **Baseline:** run each issue with Copilot (no extra instructions). Record signals: tests pass, CodeQL alerts, diff size, files outside scope, review rounds, notes. Read the session log for each failure.
4. **Classify** each failure as reasoning, tool misuse or context/environment (use the triage questions in Lesson 4).
5. Change **one** lever (for example add a verification step to instructions, or fix an environment issue). Re-run the *same* set. Compare.
6. Keep or revert the change. Write a one-line conclusion.

## Verify

- [ ] Every run has recorded signals, not impressions
- [ ] Every failure has a root-cause class and evidence link
- [ ] Only one variable changed between runs

## Break it

Add the instruction "tests are optional". Re-run and see which metric exposes the regression. Then explain why an intent-based criterion ("test count must not decrease") matters.

## Exam link

Success criteria, quantitative vs qualitative signals, automated scanning signals, failure classification, tuning instructions/workflows/memory/tools.
