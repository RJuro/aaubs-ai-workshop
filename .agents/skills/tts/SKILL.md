---
name: tts
description: Turn text into spoken audio (summary, narration, slide voiceover) with Mistral Voxtral TTS. Use when the user wants text read aloud or an mp3.
---

# Speech with Mistral

1. **Write for the ear** into a `.txt`: short sentences, one idea each, numbers as words ("thirty-two percent"), no bullets, brackets or abbreviations. Read decimals and codes aloud in your head: ".0632" must become "zero point zero six three two".
2. **Voice:** `python3 tools/mistral.py voices en` lists them (also `de`, `fr`, ...). Default `gb_oliver_neutral`. There is **no Danish voice**. Danish or confidential text needs a voice model running on your own machine (not part of this folder).
3. **Generate:** `python3 tools/mistral.py tts file.txt --voice <slug> --out results` writes `results/<name>.mp3`. Keep each call to about a minute of speech; for longer texts make numbered parts and join them: `ffmpeg -f concat -safe 0 -i list.txt -c copy out.mp3` (all parts in the same format).
4. **Check:** transcribe the mp3 back (`mistral.py transcribe <mp3> --out cache`) and compare with the script; fix words it misread.

Voice cloning (`--ref clip.mp3`, 5 to 25 s of clean speech) only with that speaker's consent.
