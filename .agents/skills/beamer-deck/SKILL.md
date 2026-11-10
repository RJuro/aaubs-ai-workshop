---
name: beamer-deck
description: Build a LaTeX Beamer slide deck from notes, compile it, and check every slide visually. Use when the user wants slides, a presentation or a deck in LaTeX/PDF.
---

1. Write `out/<name>.tex`. Beamer, 16:9 (`aspectratio=169`), a plain theme (`metropolis` if `kpsewhich beamerthememetropolis.sty` finds it, else `default`). One idea per slide, at most 4 bullets, no full sentences on slides. Use TikZ or `pgfplots` for simple figures, never invent data.
2. Compile: `cd out && latexmk -pdf -interaction=nonstopmode <name>.tex`. Fix every error and any overflow you can see on the slides (not every warning).
3. Look at it with the `visual-review` skill: `python3 tools/mistral.py review out/<name>.pdf`, then open the contact sheets yourself. Fix and recompile.
4. Report the page count and anything you could not fix. Clean up with `latexmk -c`.
