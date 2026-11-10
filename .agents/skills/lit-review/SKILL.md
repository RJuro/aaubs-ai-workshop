---
name: lit-review
description: A documented literature pass - search (arXiv; OpenAlex with a key), screen abstracts with a model, read full texts by OCR, extract facts with verbatim quotes checked by script, evidence table. Use when the user wants to map, screen or extract from research literature on a topic.
---

Work as in the `notebook` skill. Start from a short protocol in `input/protocol.md` (question, search, inclusion criteria C1, C2, ..., fields to extract); write it with the user if it is missing. Scripts read the criteria from it, so a changed protocol plus a replay gives a new review.

Steps: search and cache the raw answer → screen each abstract with `ask(..., json=True)` (include / exclude / unsure, reason, supporting phrase) → PDFs and OCR into `cache/` → extract each field with a verbatim quote → **check every quote against the text by script** (ignore case, punctuation, page markers, hyphenation) → evidence table, counts per stage, check sample (random screening decisions, all unsure ones, all quotes not found).

Say plainly that one model screening one database is a first pass. Unknown fields are "not reported", never guessed.

