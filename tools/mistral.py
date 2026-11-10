"""Mistral services from the command line (university contract). Standard library only.

  python3 tools/mistral.py transcribe <audio> [--accurate]       -> out/<name>.transcript.md (+ .json)
  python3 tools/mistral.py ocr <pdf|image>                        -> out/<name>.ocr.md
  python3 tools/mistral.py tts <text.txt> [--voice ID] [--ref clip] -> out/<name>.mp3
  python3 tools/mistral.py voices [lang]                          -> list preset voices
  python3 tools/mistral.py review <deck.pdf | page images...> [--model ID] [--prompt TEXT]
                                                                  -> out/<name>-sheet-N.png + out/<name>.review.md

Every command takes --out DIR (default: out/ in the lab folder). In a notebook run use --out cache.

Key: $MISTRAL_API_KEY, else ~/.config/mistral/key (set-mistral-key), else the Mistral key saved in OpenCode (/connect).
Standard library only, except `review`, which needs Pillow for the contact sheets.
"""
import base64, json, mimetypes, os, pathlib, re, subprocess, sys, tempfile, urllib.request, uuid

API = "https://api.mistral.ai/v1"
OUT = pathlib.Path(__file__).resolve().parent.parent / "out"
def _key():
    """$MISTRAL_API_KEY, else ~/.config/mistral/key, else the key OpenCode stored with /connect."""
    if os.environ.get("MISTRAL_API_KEY"):
        return os.environ["MISTRAL_API_KEY"]
    f = pathlib.Path.home() / ".config/mistral/key"
    if f.exists():
        return f.read_text().strip()
    auth = pathlib.Path.home() / ".local/share/opencode/auth.json"
    if auth.exists() and "mistral" in json.loads(auth.read_text()):
        return json.loads(auth.read_text())["mistral"]["key"]
    raise SystemExit("No Mistral key found. In OpenCode run /connect and choose Mistral, or run tools/set-mistral-key.")


KEY = _key()


def call(path, body=None, data=None, ctype="application/json", method=None):
    req = urllib.request.Request(API + path, data if data is not None else (json.dumps(body).encode() if body else None),
                                 {"Authorization": "Bearer " + KEY, "Content-Type": ctype}, method=method)
    try:
        return json.loads(urllib.request.urlopen(req, timeout=1800).read())
    except urllib.error.HTTPError as e:
        sys.exit(f"Mistral said HTTP {e.code}: {e.read()[:400].decode(errors='replace')}")


def transcribe(src, accurate=False):
    # mono 48 kbps keeps uploads small; Voxtral returns speaker-labelled segments
    with tempfile.NamedTemporaryFile(suffix=".mp3") as tmp:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ac", "1", "-b:a", "48k", tmp.name], check=True)
        audio = pathlib.Path(tmp.name).read_bytes()
    model = "voxtral-small-transcribe-3" if accurate else "voxtral-mini-transcribe-3"
    b = uuid.uuid4().hex
    fields = [("model", model), ("diarize", "true"), ("timestamp_granularities[]", "segment")]
    body = b"".join(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode() for k, v in fields)
    body += f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="a.mp3"\r\nContent-Type: audio/mpeg\r\n\r\n'.encode() + audio + f"\r\n--{b}--\r\n".encode()
    res = call("/audio/transcriptions", data=body, ctype=f"multipart/form-data; boundary={b}")
    name = pathlib.Path(src).stem
    (OUT / f"{name}.transcript.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    lines, last = [], None
    for s in res.get("segments", []):
        spk = s.get("speaker_id") or s.get("speaker") or "?"
        stamp = f"{int(s['start'] // 60):02d}:{int(s['start'] % 60):02d}"
        if spk != last:
            lines.append(f"\n**{spk}** [{stamp}]")
            last = spk
        lines.append(s["text"].strip())
    md = OUT / f"{name}.transcript.md"
    md.write_text(f"# Transcript: {name} ({model})\n" + "\n".join(lines).replace("]\n", "] ") + "\n")
    print(md, len(res.get("segments", [])), "segments", res.get("language"))


def ocr(src):
    mime = mimetypes.guess_type(src)[0] or "application/pdf"
    uri = f"data:{mime};base64," + base64.b64encode(pathlib.Path(src).read_bytes()).decode()
    doc = {"type": "image_url", "image_url": uri} if mime.startswith("image/") else {"type": "document_url", "document_url": uri}
    res = call("/ocr", {"model": "mistral-ocr-latest", "document": doc, "include_image_base64": True})
    pages = res.get("pages", [])
    name = pathlib.Path(src).stem
    img_dir = OUT / f"{name}_img"  # figures cut from the pages; the markdown links point here
    n_img = 0
    for p in pages:
        for im in p.get("images", []):
            if im.get("image_base64"):
                img_dir.mkdir(exist_ok=True)
                (img_dir / im["id"]).write_bytes(base64.b64decode(im["image_base64"].split(",", 1)[-1]))
                p["markdown"] = p["markdown"].replace(f"]({im['id']})", f"]({img_dir.name}/{im['id']})")
                n_img += 1
    md = OUT / f"{name}.ocr.md"
    md.write_text("\n\n".join(f"<!-- page {p['index'] + 1} -->\n{p['markdown']}" for p in pages))
    print(md, len(pages), "pages", n_img, "images")


def tts(src, voice="gb_oliver_neutral", ref=None):
    text = pathlib.Path(src).read_text().strip()
    body = {"model": "voxtral-mini-tts-3", "input": text, "response_format": "mp3"}
    if ref:  # zero-shot clone from a 5-25 s clip of the speaker, with their consent
        body["ref_audio"] = base64.b64encode(pathlib.Path(ref).read_bytes()).decode()
    else:
        body["voice_id"] = voice
    out = OUT / f"{pathlib.Path(src).stem}.mp3"
    out.write_bytes(base64.b64decode(call("/audio/speech", body)["audio_data"]))
    print(out, out.stat().st_size, "bytes")


def voices(lang=None):
    for v in call("/audio/voices?limit=100")["items"]:
        if not lang or any(l.lower().startswith(lang.lower()) for l in v["languages"]):
            print(f"{v.get('slug') or v.get('id', ''):24} {v.get('name') or '':24} {','.join(v['languages']):10} {v.get('gender') or ''}")


def contact_sheets(pages, name, first=1, per=8, cols=4, width=640):
    """Lay out page images 4x2 per sheet, each labelled 'Slide N'. Needs Pillow."""
    from PIL import Image, ImageDraw, ImageFont
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 26)
    except OSError:
        font = ImageFont.load_default()
    sheets = []
    for k in range(0, len(pages), per):
        ims = [Image.open(p).convert("RGB") for p in pages[k:k + per]]
        ims = [im.resize((width, round(im.height * width / im.width))) for im in ims]
        h, pad, lab = max(im.height for im in ims), 12, 34
        rows = -(-len(ims) // cols)
        sheet = Image.new("RGB", (cols * width + (cols + 1) * pad, rows * (h + lab + pad) + pad), "white")
        d = ImageDraw.Draw(sheet)
        for i, im in enumerate(ims):
            x, y = pad + (i % cols) * (width + pad), pad + (i // cols) * (h + lab + pad)
            d.text((x, y), f"Slide {first + k + i}", fill="black", font=font)
            sheet.paste(im, (x, y + lab))
            d.rectangle([x, y + lab, x + width - 1, y + lab + im.height - 1], outline="gray")
        path = OUT / f"{name}-sheet-{len(sheets) + 1}.png"
        sheet.save(path)
        sheets.append(path)
    return sheets


def review(src, model="deepseek-v4-1-flash-1017", prompt=None):
    """Contact sheets of the slides -> vision model -> one line per slide. src: a PDF or page images in order.
    Tested 3 Nov 2026: DeepSeek V4.1 Flash found the planted defects and real ones in ~4 s per sheet;
    Mistral Medium 3.5 and Small 4 called everything OK. Models still miss small overlaps: look at flagged slides yourself."""
    if src[0].lower().endswith(".pdf"):
        name = pathlib.Path(src[0]).stem
        pages_dir = OUT / f"{name}-pages"
        pages_dir.mkdir(exist_ok=True)
        subprocess.run(["pdftoppm", "-r", "60", "-png", src[0], str(pages_dir / "p")], check=True)
        pages = sorted(pages_dir.glob("p-*.png"), key=lambda p: int(p.stem.split("-")[-1]))
    else:
        name, pages = pathlib.Path(src[0]).stem.split("-")[0], src
    prompt = prompt or (
        "This is a contact sheet of lecture slides, each labelled 'Slide N'. Review each slide for visual layout "
        "defects only: text cut off or running off the slide, elements overlapping each other or covering text, "
        "labels colliding with arrows, text running into the source line or footer, crowded or unreadable areas, "
        "titles that wrap badly or run into the logo. Be concrete and do not invent problems. Do not comment on "
        "content. Answer with one line per slide: 'Slide N: OK' or 'Slide N: <defect>; <defect>'.")
    lines = []
    for sheet in contact_sheets(pages, name):
        uri = "data:image/png;base64," + base64.b64encode(sheet.read_bytes()).decode()
        res = call("/chat/completions", {"model": model, "temperature": 0.1, "max_tokens": 4000, "messages": [
            {"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": uri}]}]})
        text = res["choices"][0]["message"]["content"]
        if isinstance(text, list):  # reasoning models return thinking + text blocks
            text = "".join(b.get("text", "") for b in text if b.get("type") == "text")
        lines.append(f"## {sheet.name}\n\n{text.strip()}\n")
    out = OUT / f"{name}.review.md"
    out.write_text(f"# Slide review ({model}), {len(pages)} slides\n\n" + "\n".join(lines))
    print(out, len(pages), "slides", model)
    print("\n".join(lines))


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    opt = lambda f: args[args.index(f) + 1] if f in args else None
    if opt("--out"):  # e.g. --out cache: write into the run folder instead of the lab's out/
        OUT = pathlib.Path(opt("--out")).resolve()
    OUT.mkdir(parents=True, exist_ok=True)
    if cmd == "transcribe":
        transcribe(args[0], "--accurate" in args)
    elif cmd == "ocr":
        ocr(args[0])
    elif cmd == "tts":
        tts(args[0], opt("--voice") or "gb_oliver_neutral", opt("--ref"))
    elif cmd == "voices":
        voices(args[0] if args else None)
    elif cmd == "review":
        imgs = [a for a in args if not a.startswith("--") and a not in (opt("--model"), opt("--prompt"), opt("--out"))]
        review(imgs, opt("--model") or "deepseek-v4-1-flash-1017", opt("--prompt"))
    else:
        sys.exit(__doc__)
