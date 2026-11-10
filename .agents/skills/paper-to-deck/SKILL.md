---
name: paper-to-deck
description: Turn a research paper (PDF) into an AAU-style Beamer talk with figures from the paper, rebuilt tables and a fact check. Use when the user wants slides, a talk, a seminar or a lecture made from a paper or report.
---

Ask first, if not given: talk length (default 20 minutes, about 12 slides) and audience (colleagues, students, policy). If the paper is unpublished or under review, confirm it may go to the Mistral API.

1. **Read.** `python3 tools/mistral.py ocr <paper.pdf>` gives `out/<name>.ocr.md` (page markers, LaTeX equations, Markdown tables) and the paper's figures in `out/<name>_img/`. Read the whole file, not just the abstract.

2. **Outline first**, in `out/<name>-deck/OUTLINE.md`:
   - the paper's claim in one sentence, in plain words;
   - the story: a hook (a case, a number or a bit of history), the question, what the authors did, two or three results, "So what?", open questions;
   - one line per slide: title, subtitle that states the point, and the page, figure or table that backs it.
   Show the outline to the user and wait for an OK, unless they asked you to go straight through.

3. **Build.** Copy `templates/aau/` into `out/<name>-deck/` and write `deck.tex` from `aau-template.tex`. Rules:
   - the frame title names the topic, the subtitle states the point;
   - at most four bullets, short phrases, define each term the first time it appears, examples before abstractions;
   - figures: use the paper's own images from `out/<name>_img/` (copy them into the deck folder), one per slide, with `\kilde{Figure N in Author (Year)}`;
   - tables: rebuild with `booktabs`, keep only the rows and columns the point needs, highlight the key number with `\hl{}`;
   - no numbers, quotes or claims that are not in the paper.

4. **Compile and look.** `cd out/<name>-deck && latexmk -pdf -interaction=nonstopmode deck.tex`. Fix every error and any overflow you can see on the slides. Then follow the `visual-review` skill (`python3 tools/mistral.py review out/<name>-deck/deck.pdf` from the lab folder) and look at the contact sheets yourself: cut-off text, overlaps, figures too small to read. Fix and repeat.

5. **Fact check** in `out/<name>-deck/CHECK.md`: every number, quote and claim on the slides, with the page it comes from in the OCR file. Anything you cannot trace goes off the slide.

6. Report: page count, the slides you are least sure about, and anything from the outline you dropped.
