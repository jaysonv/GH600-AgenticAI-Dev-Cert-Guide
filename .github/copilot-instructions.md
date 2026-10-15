# Repository instructions

This repo is a study guide for the GitHub Certified: Agentic AI Developer (GH-600) exam.

- Content lives in `lessons/`, `labs/`, `flashcards/domain-*.json` and `simulator/questions/domain-*.json`.
- After editing JSON run: `python tools/validate.py && python tools/build.py && python -m unittest discover tests`.
- Question and card ids follow `D<domain>-Q<nn>` / `D<domain>-C<nn>`. Keep them unique.
- Facts must be checkable against Microsoft Learn or docs.github.com. Put the source in `ref`.
- Never add real exam questions or "dump" content.
- Standard library only for Python code.
