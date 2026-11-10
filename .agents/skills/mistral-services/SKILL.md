---
name: mistral-services
description: Which Mistral service and model to use for which job (chat models, OCR, transcription, speech, embeddings, batch), and how to call them fast and cheap through the workshop tools. Read before any task that calls Mistral.
---

# Mistral services: what to use, and how

Everything goes through two files: `tools/mistral.py` (OCR, transcription, speech) and `steps/llm.py` (model calls from scripts: `ask`, `ask_many`, `embed`). Both find the key themselves. Never write new API code, never print the key.

## Pick the right service

| Job | Use | Not this |
|---|---|---|
| Read a PDF, a scan, a photo of a table | `mistral.py ocr` | reading numbers off page images with your own vision: slower, worse, and expensive in tokens |
| Audio or video to text | `mistral.py transcribe` | |
| Many short items (label, screen, classify, extract one field) | `ask_many(prompts, model="zai-glm-5-3-flash")` | a loop of single `ask` calls |
| Long documents, extraction with quotes, writing | `ask()` (default DeepSeek V4.1 Flash) | |
| Hard judgement on few items | `ask(..., model="mistral-large-4")` | |
| Search, topics, similarity | `embed(texts)` (mistral-embed) | asking a chat model to compare texts pairwise |
| Text to speech | `mistral.py tts` | |

## Rules that save time and money

- **One call per item, all in parallel.** `ask_many` runs 8 at a time: 100 labels in about 15 seconds. Do not put 100 items in one prompt.
- **Small pilot first.** 5 to 10 items, look at the answers, fix the prompt, then the rest.
- **Cache everything.** `llm.py` stores every answer in `llm/`; OCR and transcripts go straight to the run's `cache/` with `--out cache`. A rerun then costs nothing.
- **Ask for JSON** (`json=True`) when a script reads the answer, with a quote or reason field so a person can check it.
- **Reasoning.** GLM gets low reasoning automatically. Do not raise it for routine items; it makes calls slower, not better.
- **Batch API** is cheaper but sits in a queue (more than 15 minutes in our test): only for thousands of items you do not need today.
- **Errors.** 429 (too many requests) is retried by the tools. 401 means the key is wrong or expired: tell the user, do not retry.

## Rough prices (AAU account, Nov 2026)

OCR about 0.03 kr per page. Transcription about 0.02 kr per minute of audio. 100 short labels with GLM Flash well under 1 kr. A 50-minute podcast, transcribed and analysed: about 2.5 kr.

## Data

Default and workshop workspaces: no personal data. Interviews with identifiable people, student data, HR: ask the user first (dedicated workspace with a DPIA, or a local model).
