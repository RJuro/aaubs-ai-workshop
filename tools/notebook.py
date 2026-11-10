"""Run folders: a research notebook an agent fills in and anyone can replay. Standard library + pandoc.

  python3 tools/notebook.py init <folder>                 -> makes an exercise folder (README.md + input/) a run folder
  python3 tools/notebook.py new <slug> [input files...]   -> runs/<date>-<slug>/ with NOTEBOOK.md and run.sh
  python3 tools/notebook.py render <run>                 -> <run>/notebook.html (narrative, figures, tables, code, record)
  python3 tools/notebook.py verify <run>                 -> replays run.sh in a copy and compares every result file

A run folder:
  input/       the input files, never changed
  steps/       one script per step (01_load.py, 02_clean.R, ...); each reads earlier results, writes to results/
  results/     tables (.csv), figures (.png), text (.md)
  llm/         every model call with its answer (see tools/llm.py), so replays give the same answers
  cache/       raw downloads and service output (web data, OCR, transcripts), fetched once and reused
  NOTEBOOK.md  the story: per step what was done and why, key output, the check, decisions
  run.sh       replays all steps from input/
"""
import datetime, hashlib, json, os, pathlib, re, shutil, subprocess, sys, tempfile

LAB = pathlib.Path(__file__).resolve().parent.parent
RUNSH = """#!/bin/sh
# Replays every step in order from input/. Model calls come from llm/ (NOCACHE=1 asks the model again).
set -e
cd "$(dirname "$0")"
mkdir -p results
for s in steps/[0-9]*; do
  echo "== $s"
  case "$s" in
    *.py) python3 "$s" ;;
    *.R) Rscript "$s" ;;
    *.sh) sh "$s" ;;
  esac
done
"""


def sha(p):
    if p.suffix == ".pdf":  # PDF engines stamp IDs and dates into the bytes: compare the text and page count instead
        text = subprocess.run(["pdftotext", str(p), "-"], capture_output=True, text=True).stdout
        return "pdf:" + hashlib.sha256(text.encode()).hexdigest()[:12]
    if p.suffix == ".svg":  # matplotlib writes random ids and a date into SVGs: compare without them
        text = re.sub(r'(id="|url\(#|href="#)[^")]*|<dc:date>.*?</dc:date>', "", p.read_text())
        return "svg:" + hashlib.sha256(text.encode()).hexdigest()[:12]
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def new(slug, inputs):
    run = LAB / "runs" / f"{datetime.date.today()}-{slug}"
    if run.exists():
        sys.exit(f"{run} exists already")
    for d in ("input", "steps", "results", "llm", "cache"):
        (run / d).mkdir(parents=True)
    for f in inputs:
        shutil.copy2(f, run / "input")
    shutil.copy2(LAB / "tools" / "llm.py", run / "steps" / "llm.py")  # a frozen copy travels with the run
    (run / "run.sh").write_text(RUNSH)
    (run / "run.sh").chmod(0o755)
    (run / "NOTEBOOK.md").write_text(f"---\ntitle: \"{slug}\"\ndate: {datetime.date.today()}\n---\n\n")
    print(run)


def init(folder):
    """Adds the run scaffolding to an existing folder; never touches input/, README.md or files already there."""
    run = pathlib.Path(folder).resolve()
    for d in ("input", "steps", "results", "llm", "cache"):
        (run / d).mkdir(exist_ok=True)
    if not (run / "steps" / "llm.py").exists():
        shutil.copy2(LAB / "tools" / "llm.py", run / "steps" / "llm.py")
    if not (run / "run.sh").exists():
        (run / "run.sh").write_text(RUNSH); (run / "run.sh").chmod(0o755)
    if not (run / "NOTEBOOK.md").exists():
        (run / "NOTEBOOK.md").write_text(f"---\ntitle: \"{run.name}\"\ndate: {datetime.date.today()}\n---\n\n")
    print(run)


def manifest(run):
    files = lambda d: {str(p.relative_to(run)): sha(p) for p in sorted((run / d).rglob("*")) if p.is_file() and p.name != ".DS_Store"}
    calls = [json.loads(p.read_text()) for p in sorted((run / "llm").glob("*.json")) if not p.name.startswith("emb_")]  # .used (replay log) is not *.json
    m = {"rendered": datetime.datetime.now().isoformat(timespec="seconds"), "input": files("input"),
         "steps": files("steps"), "results": files("results"),
         "model_calls": len(calls), "models": sorted({c["model"] for c in calls}),
         "tokens_in": sum(c.get("usage", {}).get("prompt_tokens", 0) for c in calls),
         "tokens_out": sum(c.get("usage", {}).get("completion_tokens", 0) for c in calls),
         "first_call": min((c["time"] for c in calls), default=None), "last_call": max((c["time"] for c in calls), default=None)}
    (run / "MANIFEST.json").write_text(json.dumps(m, indent=1))
    return m


def render(run):
    run = pathlib.Path(run).resolve()
    m = manifest(run)
    lang = {".py": "python", ".R": "r", ".sh": "sh"}
    code = "\n".join(f"### `{p.name}`\n\n```{lang.get(p.suffix, '')}\n{p.read_text().rstrip()}\n```\n"
                     for p in sorted((run / "steps").glob("[0-9]*")))
    rows = lambda d: "\n".join(f"| `{k}` | `{v}` |" for k, v in m[d].items())
    record = (f"\n\n# Run record\n\n- Model calls: {m['model_calls']} ({', '.join(m['models']) or 'none'}), "
              f"{m['first_call'] or ''} to {m['last_call'] or ''}" + (f", {m['tokens_in']:,} tokens in, {m['tokens_out']:,} out" if m['tokens_in'] else "") + f"\n- Replay: `sh run.sh` (answers come from `llm/`), "
              f"check with `python3 tools/notebook.py verify`\n\n| Input | sha256 |\n|---|---|\n{rows('input')}\n\n"
              f"| Result | sha256 |\n|---|---|\n{rows('results')}\n\n# Code\n\n{code}")
    md = (run / "NOTEBOOK.md").read_text()
    brief = (run / "BRIEF.md").read_text().split("\n", 1)[1] if (run / "BRIEF.md").exists() else ""
    head, body = (md.split("---\n", 2)[1], md.split("---\n", 2)[2]) if md.startswith("---") else ("", md)
    brief = f"# Brief\n{brief}\n" if brief else ""
    src = (f"---\n{head}---\n\n{brief}" if head else brief) + body + record
    with tempfile.NamedTemporaryFile("w", suffix=".md", dir=run, delete=False) as t:
        t.write(src)
    try:
        subprocess.run(["pandoc", t.name, "-o", str(run / "notebook.html"), "--standalone", "--embed-resources",
                        "--toc", "--toc-depth=2", "--resource-path", str(run), "--css", str(LAB / "tools" / "notebook.css"),
                        "--metadata", "lang=en"], check=True)
    finally:
        os.unlink(t.name)
    print(run / "notebook.html")


def verify(run):
    run = pathlib.Path(run).resolve()
    before = {str(p.relative_to(run)): sha(p) for p in (run / "results").rglob("*") if p.is_file() and p.name != ".DS_Store"}
    with tempfile.TemporaryDirectory() as tmp:
        copy = pathlib.Path(tmp) / run.name
        shutil.copytree(run, copy, ignore=shutil.ignore_patterns("results", "notebook.html"))
        r = subprocess.run(["sh", "run.sh"], cwd=copy, capture_output=True, text=True, env={**os.environ, "LLM_LOG_USED": "1"})
        if r.returncode:
            sys.exit(f"Replay failed:\n{r.stdout[-1500:]}\n{r.stderr[-1500:]}")
        after = {str(p.relative_to(copy)): sha(p) for p in (copy / "results").rglob("*") if p.is_file()}
        used = copy / "llm" / ".used"
        unused = sorted({f.stem for f in (run / "llm").glob("*.json")} - set(used.read_text().split())) if used.exists() else []
    same = [k for k in before if after.get(k) == before[k]]
    print(f"Replayed {run.name}: {len(same)} of {len(before)} result files identical")
    for k in sorted(set(before) | set(after)):
        if before.get(k) != after.get(k):
            print("  differs:" if k in before and k in after else "  missing:" if k in before else "  new:   ", k)
    if unused:
        print(f"{len(unused)} stored model answers were not used by the replay (from earlier prompts). "
              f"Keep them as history or delete them: " + " ".join(f"llm/{u}.json" for u in unused[:5]) + (" ..." if len(unused) > 5 else ""))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cmd, args = sys.argv[1], sys.argv[2:]
    {"new": lambda: new(args[0], args[1:]), "init": lambda: init(args[0]), "render": lambda: render(args[0]), "verify": lambda: verify(args[0])}.get(cmd, lambda: sys.exit(__doc__))()
