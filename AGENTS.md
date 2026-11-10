# House rules for agents in this folder

Recipes are in `.agents/skills/*/SKILL.md`. Read the one that matches the task, plus `notebook` for any task on data or documents and `mistral-services` for anything that calls Mistral. Do not read the source code of the tools below: their use is described here.

## The tools (use them, do not rewrite or edit them)

| Tool | What it does |
|---|---|
| `python3 tools/notebook.py init <workflow-folder>` | makes the folder a run: `steps/`, `cache/`, `results/`, `llm/`, `run.sh`, and a copy of `llm.py` in `steps/` |
| `python3 tools/notebook.py render <folder>` | `NOTEBOOK.md` + figures to `notebook.html` |
| `python3 tools/mistral.py ocr <pdf or png> --out cache` | Mistral OCR to `cache/<name>.ocr.md`, `<!-- page N -->` markers, tables as Markdown (about 10 s per page) |
| `python3 tools/mistral.py transcribe <audio> --out cache` | Voxtral transcript with speakers and timestamps to `cache/<name>.transcript.md` + `.json`; waits until done (1 to 2 min for 50 min of audio) |
| `python3 tools/mistral.py tts <text.txt> --voice <id> --out results` | speech to `results/<name>.mp3`; `voices en` lists voices |
| `from llm import ask, ask_many, embed` (in `steps/`) | `ask(prompt, system=None, model=None, json=False)`; `ask_many(prompts, model=..., json=...)` runs 8 in parallel, same order; `embed(texts)` mistral-embed, or `model="ollama/nomic-embed-text"` locally. Every answer is cached in `llm/` |

If a tool lacks something, write it in `steps/` and tell the user. Never edit files in `tools/`.

## How to work

- **Workflows:** the user names a folder in `workflows/`. Read its README, work only inside that folder, run `notebook.py init` first. If `input/` is empty and the README asks for the user's own file, ask for it.
- **Plan in the chat** in 3 to 6 lines and wait for "go". Use the input the README gives (a short clip, the first page, 100 rows); bigger only when the user asks.
- **Make exactly what was asked.** No extra figures, formats, exports or checks of the input data against outside sources. Ideas for more go in one line at the end of your report.
- **Look at a figure or page once, fix once, then show it to the user.** At most two rounds of polishing on anything visual. Do not read page images to check numbers: scripts check numbers.
- **When something does not add up** after one fix: write down the difference and the likely reason, and move on. Do not loop.
- **Waiting:** commands that call Mistral wait until they are done: give them a 10-minute shell timeout (600000 ms) so they are not sent to the background. Do not poll with `sleep`, and do not open files in a browser; give the user the path.
- **Files:** downloads and service output in `cache/`, results in `results/`, scripts in `steps/`. Nothing at the top of the workshop folder.
- **Exploring:** if the user asks what this folder can do, read `README.md` and the workflow READMEs and answer briefly; do not run anything.
- Say plainly what you could not do or are unsure about. Never invent data, quotes or references.
- No personal or confidential data to an API without asking the user first. Ask before installing packages.
- **Windows:** use `python` instead of `python3`, and run the steps one by one instead of `sh run.sh`.
