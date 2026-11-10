# Setup (15 minutes)

## 1. Mistral access

1. Apply in the AAU Serviceportal: https://serviceportal.aau.dk/serviceportal?id=sc_cat_item&sys_id=b3a364e5c3a336d4f0f3041ad001316e
2. When approved, log in once at https://v2.auth.mistral.ai/login with **Continue with AAU – SSO**.
3. Tell Roman. He asks CLAAUDIA to add you to the workshop workspace (API keys only come from a named workspace).

## 2. Your API key

https://console.mistral.ai → bottom left, switch from **Default Workspace** to the workshop workspace → **API Keys** → **Create new key** → copy it (shown once). Personal: never paste it into a chat or a file you share.

## 3. OpenCode

Install the desktop app from https://opencode.ai/download (Mac, Windows, Linux).

## 4. Connect

1. Get the folder (see `README.md`), then OpenCode → **Open project** → `aaubs-ai-workshop` (the folder itself, not a subfolder).
2. Type `/connect`, choose **Mistral**, paste the key. The workshop scripts find it there too.
3. Type `/models`, choose **DeepSeek V4.1 Flash** (provider Mistral), and pick the **low** reasoning variant. High reasoning makes the agent think for minutes between steps.
4. Test: type *"Run `python3 tools/mistral.py voices en` and tell me how many voices there are."* About 36 means everything works.

## 5. Python packages

The agent asks before installing anything. To do it yourself once:

```
pip install pandas matplotlib openpyxl
```

Mac without Python: `xcode-select --install`. Windows: python.org installer (tick "Add to PATH").

---

## Other routes

- **Claude Code or Codex instead of OpenCode:** open this folder there; the same recipes are in `.agents/skills/` (`.claude/skills` points to them). Save the Mistral key for the scripts with `tools/set-mistral-key` (Mac/Linux) or set `MISTRAL_API_KEY`.
- **ChatGPT plan:** OpenCode can sign in with it (`/connect` → OpenAI), fine to try, but research data belongs on the Mistral connection (AAU agreement).
- **Fixed default model:** `~/.config/opencode/opencode.jsonc` with `{"model": "mistral/deepseek-v4-1-flash-1017"}`, then restart OpenCode.

## If something does not work

- **"No Mistral key found"**: `/connect` → Mistral again, or set `MISTRAL_API_KEY`.
- **HTTP 401**: key wrong or expired; make a new one.
- **"This workspace can't be used"**: you made the key in the default workspace; switch workspace and make a new one.
- **The agent cannot see the recipes**: open the workshop folder itself, not a subfolder.
