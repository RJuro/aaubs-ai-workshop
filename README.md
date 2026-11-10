# AAUBS AI workshop: agents for research

Recipes (skills), small tools and workflow ideas for letting an AI agent do research tasks on your own laptop: fetch and clean data, transcribe a recording, turn a paper into something readable and listenable, write a short paper in LaTeX, map a literature. Made for the AAUBS seminar on 11 November 2026, with Mistral models through AAU and the open-source agent OpenCode. The same folder works in Claude Code or Codex.

There is no data of ours in here beyond a few small public files. You bring your own: a recording, a paper, an export.

## Get it

**Ask your agent.** In OpenCode (or Claude Code), from any folder:

> Download https://github.com/RJuro/aaubs-ai-workshop/archive/refs/heads/main.zip, unzip it to my Desktop and rename the folder to aaubs-ai-workshop.

Then open that folder as your project (OpenCode: **Open project**).

**Or by hand:** on GitHub, **Code → Download ZIP**, unzip it to your Desktop. With git: `git clone https://github.com/RJuro/aaubs-ai-workshop`.

Then: **`SETUP.md`** (Mistral key, OpenCode, 15 minutes), and ask the agent:

> Explore this folder and tell me in five lines what I can do with it.

## Workflows

Each folder in `workflows/` has a short README with one prompt to paste. The how lives in the skills (`.agents/skills/`), which the agent reads itself.

| Folder | What | Brings its own data? |
|---|---|---|
| `01-denmark-map` | a map from Statistics Denmark's open data | no, the agent fetches it |
| `02-your-recording` | your own voice memo or meeting: transcript, summary, themes | yes: record something on your phone |
| `03-your-paper` | your own paper as a clean, readable PDF and a short audio summary | yes: a paper you wrote |
| `04-latex-paper` | a short paper written and compiled from notes and a data file | included (small, public data) |
| `05-messy-merge` | two messy files from a "colleague", cleaned and merged, with a log of every fix | included (small, made up from public data) |
| `06-literature-review` | an arXiv search, screened, with an evidence table of checked quotes | the agent searches arXiv |
| `07-bibliometrics` | what a field looks like, from your own Web of Science or Scopus export | yes: your own export |

## What is in the folder

| Path | What |
|---|---|
| `AGENTS.md` | house rules the agent reads first, and how to use the tools |
| `.agents/skills/` | one-page recipes; `.claude/skills` points to the same folder |
| `tools/mistral.py` | Mistral OCR, transcription, speech |
| `tools/llm.py` | model calls from scripts, cached: `ask`, `ask_many`, `embed` |
| `tools/notebook.py` | turns a workflow folder into a run you can read and replay |
| `templates/aau/` | AAU Beamer template |
| `docs/MISTRAL-PLATFORM.md` | what AAU's Mistral account offers, and the rules |

## Rules in one breath

AAU's Mistral is for research and research support, not teaching. No personal data in the default workspace; recordings of identifiable people need a dedicated workspace and a DPIA, or a model on your own machine. Your key is personal. The model's judgements are a first pass: you check.
