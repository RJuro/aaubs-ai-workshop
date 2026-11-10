---
name: notebook
description: Do a research task on data or documents (analysis, maps, coding texts, literature, extracting data from PDFs) so the user can follow it - a short plan, one script per step, cached downloads and model calls, a short notebook at the end. Use whenever the user gives data or documents and wants a result they can check.
---

# Notebook: work the user can follow

Keep it light. The user wants the result; the trail is a by-product.

1. **Start.** Exercise folder (has `README.md`): `python3 tools/notebook.py init <folder>`. Own task: `python3 tools/notebook.py new <slug> <files>`.
2. **Plan in the chat.** 3 to 6 short lines. Ask only if something important is unclear. Wait for "go".
3. **Small scripts.** One per step in `steps/` (`01_fetch.py`, `02_map.py`, ...). Run each, fix errors, move on. Read from `input/`, write to `results/`, never change `input/`. Downloads and OCR/transcripts go to `cache/` and are reused.
   - Model calls: `from llm import ask, ask_many` (the copy in `steps/`). Every answer is stored in `llm/`.
   - Many short items (labels, screening): `ask_many(prompts, model="zai-glm-5-3-flash")`, one item per prompt, all in parallel. Long documents: `ask()` with the default model.
4. **Look at what you made, once.** Open the figure, fix what is wrong or unreadable, then show it to the user. One PNG per figure, at most two rounds of polish in total. Make only the figures that were asked for.
5. **When a model judges** (labels, codes, extracted values): keep a quote or reason for each, and write `results/check_sample.csv` (10 to 20 rows, an empty `human` column).
6. **Finish.** `NOTEBOOK.md`: two or three sentences per step, the key table or figure, what you checked, and *What this shows / What it does not show*. Then `python3 tools/notebook.py render <folder>` and give the path to `notebook.html`. No replay or verify unless the user asks.

No invented numbers or quotes. Write Markdown tables yourself (`to_markdown` needs `tabulate`).
