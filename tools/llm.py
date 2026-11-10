"""Cached, logged model calls for a run folder. Standard library only.

    from llm import ask
    answer = ask("Is this abstract about AI adoption in firms? ...", system="You screen abstracts.")
    record = ask(prompt, json=True)          # parsed JSON object back
    vectors = embed(list_of_texts)            # mistral-embed vectors, one list of floats per text
    answers = ask_many(prompts, system=..., json=True, workers=8)   # many prompts in parallel, same order
    ask(prompt, model="ollama/qwen3.5:2b")   # a local model through Ollama: nothing leaves the machine
    decide(text, "Which kind of AI talk?", {"concrete": "names a product or number", ...})
                                              # local decision model (Ollama tev1): one option + probabilities

Every call is stored in <run>/llm/<hash>.json (request, answer, model, time). The same prompt, system,
model and settings give the stored answer again, so replaying a run costs nothing and gives identical
results. NOCACHE=1 forces fresh calls (useful to see how stable the answers are).
The run folder is the current directory (run.sh changes into it), or $RUN_DIR.
Key: $MISTRAL_API_KEY, else ~/.config/mistral/key, else the Mistral key saved in OpenCode (/connect).
"""
import datetime, hashlib, json, os, pathlib, time, urllib.error, urllib.request

MODEL = os.environ.get("LLM_MODEL", "deepseek-v4-1-flash-1017")
CACHE = pathlib.Path(os.environ.get("RUN_DIR", ".")) / "llm"


def _key():
    """$MISTRAL_API_KEY, else ~/.config/mistral/key, else the key OpenCode stored with /connect."""
    if os.environ.get("MISTRAL_API_KEY"):
        return os.environ["MISTRAL_API_KEY"]
    f = pathlib.Path.home() / ".config/mistral/key"
    if f.exists():
        return f.read_text().strip()
    auth = pathlib.Path.home() / ".local/share/opencode/auth.json"
    if auth.exists() and "mistral" in _json.loads(auth.read_text()):
        return _json.loads(auth.read_text())["mistral"]["key"]
    raise SystemExit("No Mistral key found. In OpenCode run /connect and choose Mistral, or run tools/set-mistral-key.")


def ask(prompt, system=None, model=None, json=False, temperature=0, max_tokens=4000, **extra):
    model = model or MODEL
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
    body = {"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens, **extra}
    if model.startswith("zai-glm") and "reasoning_effort" not in extra:
        body["reasoning_effort"] = "low"  # GLM always thinks; "low" keeps it to a sentence
    if json:
        body["response_format"] = {"type": "json_object"}
    h = hashlib.sha256(_json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]
    f = CACHE / f"{h}.json"
    if f.exists() and not os.environ.get("NOCACHE"):
        text = _json.loads(f.read_text())["answer"]
    else:
        text, usage = _post(body)
        CACHE.mkdir(exist_ok=True)
        f.write_text(_json.dumps({"model": model, "time": datetime.datetime.now().isoformat(timespec="seconds"),
                                  "usage": usage, "request": body, "answer": text}, ensure_ascii=False, indent=1))
    if os.environ.get("LLM_LOG_USED"):  # set by notebook.py verify, to find answers no step uses any more
        with open(CACHE / ".used", "a") as u:
            u.write(h + "\n")
    return _json.loads(text) if json else text


def embed(texts, model="mistral-embed", batch=64):
    """Embeddings for a list of texts, cached in llm/ (one file per batch, keyed by its texts).

    model="ollama/nomic-embed-text" runs locally through Ollama: nothing leaves the machine.
    """
    out = []
    for i in range(0, len(texts), batch):
        chunk = texts[i:i + batch]
        body = {"model": model, "input": chunk}
        h = hashlib.sha256(_json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]
        f = CACHE / f"emb_{h}.json"
        if f.exists() and not os.environ.get("NOCACHE"):
            vecs = _json.loads(f.read_text())["vectors"]
        else:
            if model.startswith("ollama/"):  # local model, Ollama /api/embed
                body = {"model": model[7:], "input": chunk}
                req = urllib.request.Request("http://127.0.0.1:11434/api/embed", _json.dumps(body).encode(),
                                             {"Content-Type": "application/json"})
                res = _json.loads(urllib.request.urlopen(req, timeout=600).read())
                vecs, usage = res["embeddings"], {}
            else:
                req = urllib.request.Request("https://api.mistral.ai/v1/embeddings", _json.dumps(body).encode(),
                                             {"Authorization": "Bearer " + _key(), "Content-Type": "application/json"})
                res = _json.loads(urllib.request.urlopen(req, timeout=300).read())
                vecs = [d["embedding"] for d in sorted(res["data"], key=lambda d: d["index"])]
                usage = res.get("usage", {})
            CACHE.mkdir(exist_ok=True)
            f.write_text(_json.dumps({"model": model, "time": datetime.datetime.now().isoformat(timespec="seconds"),
                                      "usage": usage, "n": len(chunk), "vectors": vecs}))
        if os.environ.get("LLM_LOG_USED"):
            with open(CACHE / ".used", "a") as u:
                u.write(f.stem + "\n")
        out += vecs
    return out


def decide(state, instructions, criteria, model="tev1:0.8b"):
    """A local decision model (Ollama /v1/systemone): picks one of `criteria` {name: description} for `state`.
    Returns {"choice", "probabilities", "confidence"}. Cached in llm/ like ask(). Nothing leaves the machine."""
    body = {"model": model, "state": state,
            "questions": {"q": {"type": "choice", "instructions": instructions, "criteria": criteria}}}
    h = hashlib.sha256(_json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]
    f = CACHE / f"{h}.json"
    if f.exists() and not os.environ.get("NOCACHE"):
        ans = _json.loads(f.read_text())["answer"]
    else:
        req = urllib.request.Request("http://127.0.0.1:11434/v1/systemone", _json.dumps(body).encode(),
                                     {"Content-Type": "application/json"})
        res = _json.loads(urllib.request.urlopen(req, timeout=120).read())
        ans = res["answers"]["q"]
        CACHE.mkdir(exist_ok=True)
        f.write_text(_json.dumps({"model": "ollama/" + model, "time": datetime.datetime.now().isoformat(timespec="seconds"),
                                  "usage": res.get("usage", {}), "request": body, "answer": ans}, ensure_ascii=False, indent=1))
    if os.environ.get("LLM_LOG_USED"):
        with open(CACHE / ".used", "a") as u:
            u.write(h + "\n")
    return ans


def ask_many(prompts, workers=8, **kw):
    """ask() for a list of prompts, `workers` at a time; answers come back in the same order."""
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(workers) as pool:
        return list(pool.map(lambda p: ask(p, **kw), prompts))


def _post(body, tries=4):
    if body["model"].startswith("ollama/"):  # local model, OpenAI-compatible endpoint of Ollama
        body = {"reasoning_effort": "none", **body, "model": body["model"][7:]}  # thinking off unless asked for
        req = urllib.request.Request("http://127.0.0.1:11434/v1/chat/completions", _json.dumps(body).encode(),
                                     {"Content-Type": "application/json"})
    else:
        req = urllib.request.Request("https://api.mistral.ai/v1/chat/completions", _json.dumps(body).encode(),
                                     {"Authorization": "Bearer " + _key(), "Content-Type": "application/json"})
    for i in range(tries):
        try:
            res = _json.loads(urllib.request.urlopen(req, timeout=600).read())
            msg = res["choices"][0]["message"]["content"]
            if isinstance(msg, list):  # reasoning models answer with thinking + text blocks
                msg = "".join(b.get("text", "") for b in msg if b.get("type") == "text")
            return msg.strip(), res.get("usage", {})
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503) or i == tries - 1:
                raise SystemExit(f"Mistral said HTTP {e.code}: {e.read()[:300].decode(errors='replace')}")
            time.sleep(2 ** i * 3)  # rate limit or hiccup: wait and retry


_json = json  # `json` is also a parameter name of ask()
