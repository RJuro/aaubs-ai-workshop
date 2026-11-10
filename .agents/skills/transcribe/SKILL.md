---
name: transcribe
description: Transcribe audio or video (interview, podcast, meeting, lecture) with Mistral Voxtral, with speaker labels and timestamps, then clean it up or analyse it. Use when the user gives an audio or video file.
---

# Transcription with Mistral

0. **Use the audio the README gives** (a short clip if there is one). Download full episodes only when the user asks.
1. **Make the file small first.** Mono, 16 kHz, compressed: `ffmpeg -i in.mp4 -ac 1 -ar 16000 -b:a 32k cache/audio.mp3`. Uploads are faster and nothing is lost for speech.
2. **Transcribe once:** `python3 tools/mistral.py transcribe cache/audio.mp3 --out cache` (shell timeout 600000 ms) (Voxtral Mini, speaker labels, timestamps; about 0.02 kr per minute; a 50-minute file takes one to two minutes). `--accurate` uses the larger model at about 3 times the price: only for poor audio or heavy accents. Output: `cache/<name>.transcript.md` and `.json`; reuse them, never transcribe twice.
3. **Speakers:** the labels are `speaker_1`, `speaker_2`. Work out who is who from what they say (the host introduces the guests) and keep a small mapping table; ask the user if unsure.
4. **Analysis:** split the transcript into chunks of a few minutes, keep the timestamps, and send chunks with `ask_many` (one chunk per prompt, JSON out, a verbatim quote per item). Then check by script that every quote is really in the transcript.
5. **Cleanup** (only if asked for a readable transcript): fix obvious mishearings of names and terms, remove filler words, never add content. Mark doubts with `[?]`.

Confidential recordings (interviews with identifiable people, exams, HR): ask the user before sending them to any API.
