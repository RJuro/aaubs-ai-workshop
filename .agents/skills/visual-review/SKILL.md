---
name: visual-review
description: Check rendered slides, figures or pages for layout defects (cut-off text, overlaps, labels on arrows, crowding) with contact sheets and a vision model. Use after compiling a deck or document, or when the user asks whether slides look right.
---

1. Run `python3 tools/mistral.py review <deck.pdf>` (or page PNGs in order). It renders the pages, lays them out 8 per contact sheet (`out/<name>-sheet-N.png`, each labelled "Slide N"), sends each sheet to DeepSeek V4.1 Flash and writes one line per slide to `out/<name>.review.md`.
2. Open the contact sheets yourself and look at every slide the review flags. Then look closely at the slides with dense text, tables, source lines or diagrams, even if marked OK: the models miss small overlaps (a source line touching the last sentence was missed in testing).
3. Fix in the source, recompile, run the review once more. At most three rounds; then report what is left.
4. Report which slides were fixed and anything left that you could not fix.

Notes from testing (3 Nov 2026): DeepSeek found a planted defect and real ones in about 4 s per sheet. Mistral Medium 3.5 and Small 4 called every slide OK, even the broken one, and Medium invented defects when given single slides. Do not use those two for visual checks.
