# Contributing

Docs move fast. Corrections are the most valuable contribution.

1. Open an issue or PR with the **doc URL** that contradicts a card, question or lesson.
2. Add or change content only in `flashcards/*.json`, `simulator/questions/*.json`, `lessons/` or `labs/`.
3. Run `python tools/validate.py && python tools/build.py && python -m unittest discover tests`.
4. Never submit real exam questions or content from "exam dumps". Questions here must be original and must be checkable against public documentation (put the URL in the `ref` field).
