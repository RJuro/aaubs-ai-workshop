---
name: ocr
description: Turn a PDF, a scan or a photo of a document into text and tables with Mistral OCR (keeps tables and equations). Use when the user wants to read, quote, convert or extract data from a PDF or a scanned page.
---

# OCR with Mistral

**Mistral OCR is the reader. You are not.** Do not read numbers or names off page images yourself; that is slower and less accurate than OCR. Look at an image only to understand the layout or to check one spot.

1. **Run it once on the file:** `python3 tools/mistral.py ocr <file.pdf|file.png> --out cache` writes `cache/<name>.ocr.md` (one `<!-- page N -->` marker per page; tables as Markdown, equations as LaTeX). About 10 seconds per page.
2. **Read the result before you parse.** Check that the tables have the columns you expect and that rows line up.
3. **Tables printed in two or more blocks side by side** (old yearbooks, statistics tables): OCR of the whole page often merges the blocks and shifts rows. Instead, render the page and OCR each block separately:
   ```
   pdftoppm -r 300 -png -f N -l N input/file.pdf cache/pN
   python3 -c "from PIL import Image; im=Image.open('cache/pN-N.png'); w,h=im.size; im.crop((0,0,w//2+20,h)).save('cache/pN_left.png'); im.crop((w//2-20,0,w,h)).save('cache/pN_right.png')"
   python3 tools/mistral.py ocr cache/pN_left.png --out cache    # then the right block
   ```
   Each block comes back as its own clean table. (Adjust the crop if the blocks are not at the middle.)
   Tested on the 1930 yearbook: OCR of the whole page shifted rows in the right block (towns lost, numbers on the wrong town) in a way the printed totals could not see; block by block it was right.
4. **Let a model build the table, not a hand-written parser.** One `ask(prompt + block_markdown, json=True)` per block (or `ask_many` for all blocks at once): describe the columns, the row types and what "—" means, ask for JSON rows in printed order with numbers copied exactly. About 10 to 20 seconds per block. Then a script checks the rows (totals, counts) and converts them to CSV.
5. **A region that looks wrong:** OCR that region again as a crop at 300 to 400 dpi. Do not transcribe it by eye.
6. **Check with the document's own structure:** printed totals, row counts, the order of entries. A script does the checking.
7. **Stop rule:** if a check still fails after one re-OCR of that region, write down the difference and the likely reason, and move on. Stay on the pages the user asked for.

To LaTeX or a readable PDF: convert the Markdown (headings to `\section`, tables to `booktabs`, equations as they are), compile with `latexmk -pdf`, and compare numbers with the original by script.
