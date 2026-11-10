---
name: latex-paper
description: Write or extend a short academic paper in LaTeX from notes, data and a bibliography, and compile it. Use when the user wants a paper, note, chapter or report written in LaTeX.
---

# A paper in LaTeX

What you cannot know without being told:

- **Setup:** `main.tex` is the spine (`\input{preamble}`, one `\input{sections/NN-name}` per section, `\bibliography{references}`), `preamble.tex` holds the packages, `sections/` one file per section, `references.bib`. Build with `latexmk -pdf main`. If the user has a template, use it.
- **Order:** first an outline in the chat (sections, the point of each, which figure or table goes where). Wait for "go". Then figures and tables from scripts (numbers never typed by hand into the text), then the sections, then compile.
- **Citations:** only keys that are in `references.bib`. Never invent a reference; where a claim needs one that is missing, write `\needcite`.
- **Style:** plain language, short sentences, no em-dashes, one idea per paragraph. Avoid the usual model words (delve, crucial, landscape, tapestry, underscore, pivotal). State results with the number and what it means.

Before you report: it compiles without errors, no undefined references or citations (`grep -i "undefined" main.log`), every number in the text matches the script output, and you have looked at the PDF pages. List anything left as `\needcite` or `\todo`.
