# Mistral's platform, November 2026 (for the 11 Nov workshop)

Checked 9 Nov 2026 against docs.mistral.ai, mistral.ai/news, help.mistral.ai and hpc.aau.dk/mistral. "Unverified" means only third-party sources said it, or the official page did not say it outright.

## The one-slide version

- **Three doors to the same models.** Vibe (the chat app, formerly Le Chat) for everyone; AI Studio (console.mistral.ai) for experiments, agents and API keys; Vibe Code (a coding agent in the terminal or VS Code).
- **AAU access is by application.** Default workspace: Vibe + AI Studio playground, Level 1 data, no personal data, no API keys. Dedicated workspace: full API, keys, Level 2/3 and personal data (with WorkZone case + DPIA).
- **EU company, EU inference available, training opt-out per product.** Chat history at AAU is deleted after 90 days.

## Le Chat is now Vibe

- Renamed 28 May 2026 ("Vibe gets to work"). Same address, chat.mistral.ai; history and plans carried over.
- Two modes: **Work** (web/mobile: plans multi-step tasks, asks for sign-off, then runs) and **Code** (coding agents in the terminal, VS Code or remote cloud sessions).
- The old "Chat" mode is legacy and will be sunset. "Agents" in Le Chat were replaced by **Skills** (invoked with `@`).

## Models on the API now

From the official models page (docs.mistral.ai, read 9 Nov 2026).

| Family | Current model | Notes |
|---|---|---|
| Flagship | **Mistral Large 4** (v26.10, id `mistral-large-4`) | Preview 6 Oct 2026; final build with open weights 29 Oct 2026 ("Le Chonk"). About 1T parameters (mixture of experts), multimodal, 1M context (third-party figure), reasoning low/medium/high. $0.70 in / $2.10 out per M tokens. |
| Mid | Mistral Medium 3.5 | **Deprecated 31 Oct 2026**, retired 30 Apr 2027. Still callable, but do not build new work on it. |
| Small | **Mistral Small 4** (v26.03) | Instruct, reasoning and coding in one model; Apache 2.0. |
| Edge | Ministral 3 (3B, 8B, 14B, v25.12) | Text + vision; Apache 2.0; runs on a laptop. |
| Reasoning | (no separate line) | Magistral retired 31 Jul 2026; reasoning is now a mode of Large 4 and Small 4. |
| Code | Codestral (v25.08) | Code completion. Devstral 2 retired 31 Jul 2026. |
| Third-party, hosted by Mistral | **DeepSeek V4.1 Flash 1017**, **Z.ai GLM 5.3**, **GLM 5.3 Flash** | Open-weight Chinese models run on Mistral's infrastructure under the same regional controls. All 1M context. |
| Documents | **OCR 4.1** | PDFs and scans to Markdown; tables, equations, boxes, confidence scores. |
| Speech to text | **Voxtral Mini / Small Transcribe 3**, Realtime 3 | Speaker labels (diarization). Voxtral 3 announced 20 Oct 2026. |
| Text to speech | **Voxtral TTS 3** | Preset voices, voice cloning, streaming. No Danish voice in our 3 Nov test. |
| Embeddings | Mistral Embed, Codestral Embed | For search over own documents. |
| Other | Mistral Moderation 2, Shieldstral 1.0 (safety); Timestral 1.0 (time series, 15 Oct 2026) | |

**Correction to our notes:** "5 Nov 2026: Mistral Large 4 release" is not right. Large 4 preview was 6 Oct, the final open-weight build 29 Oct. The 5 Nov post is about Studio ("Le Chonk brings the brains. Studio puts it to work").

## AI Studio (console.mistral.ai)

- **Playground**: try any model with your own prompt, compare settings.
- **Agents**: managed multi-step agents with built-in tools (web search, code interpreter, image generation, document library), subagents, sandboxes, human approval for chosen actions.
- **Libraries / Search**: upload documents, get them indexed, let an agent answer from them (RAG). Also search indexes and a Search Toolkit.
- **Prompts and Skills**: a registry so a team keeps one versioned copy of each prompt or skill (Jul 2026).
- **Connectors / MCP**: register MCP servers so agents can call outside tools and data (May 2026). There is also a Mistral MCP server for building from a coding agent.
- **Workflows**: processes that mix fixed steps, agent reasoning and human decisions; resume after interruption (public preview since Apr 2026).
- **Apps** (5 Nov 2026, public preview): small hosted apps with login and access control that put agents, workflows and document search behind a simple interface for colleagues. Built and tested locally, deployed with one command to a link or inside Vibe; can also be built from a coding agent through the Mistral MCP server. Mistral's examples: a staffing app that recommends people for projects with evidence, an idea-triage workflow, an incident-investigation agent.
- **Managed agents** (5 Nov 2026, public preview): Studio runs the agent with skills, code sandboxes, subagents, hooks, limits on tools and data, and human approval before sensitive actions.
- **Observability and evaluations**: OpenTelemetry traces of every step; test prompt or model changes on your own dataset before switching.
- **Batch API**: run large jobs (thousands of documents) asynchronously at lower priority.
- **Audio and OCR**: transcription, TTS and Document AI can be tried in the browser.
- **Fine-tuning**: the classic fine-tuning guide is marked "deprecated and no longer actively supported". Text and vision fine-tuning and Classifier Factory are still listed. Treat as not a workshop topic.
- **Workspaces and API keys**: keys belong to a workspace; admins set budgets and privacy toggles in admin.mistral.ai.

## Vibe (chat app): what researchers would use

From docs.mistral.ai/vibe/work.

- **Libraries**: curated, indexed document collections you can query and share. At AAU: shareable with other AAU Mistral users, files up to 100 MB, files cannot be downloaded back out.
- **File analysis**: upload PDFs, spreadsheets, slides, images; summarise or extract data.
- **Code Interpreter**: a sandbox that runs Python, makes charts (paid plans).
- **Web search and open URL.**
- **Deep research**: provided as a built-in "Deep Research" skill.
- **Skills**: reusable methods, checklists, templates.
- **Connectors**: email, calendar, Slack, Google Drive, custom MCP. At AAU only AAU-managed, approved MCP servers are allowed.
- **Projects, Canvas, Knowledge (memory), image generation, scheduled runs.**
- **Temporary Chat**: not saved to history, not used for training.

## Vibe Code and the CLI, and how it relates to OpenCode

- **Vibe Code** = Mistral's coding agent: CLI (`vibe`), VS Code extension, remote sandboxed sessions at chat.mistral.ai/code tied to GitHub.
- CLI is open source on GitHub (mistralai/mistral-vibe). Latest release v3.1.1 (dated 9 Nov; year not shown on the page). Features: skills as `/` commands, MCP servers, parallel subagents, `/teleport` to move a session to the browser, editor integration via ACP.
- It can also call non-Mistral models (custom API base, LiteLLM, local servers).
- **Relation to OpenCode**: same kind of tool. Both are open-source agent harnesses that read skills and call MCP servers. Vibe is Mistral's own and defaults to Mistral models; OpenCode is provider-neutral and has a built-in Mistral provider. With an AAU key either one works; the skills folder is portable between them and Claude Code.
- **At AAU**: "Launch browser" sign-in is disabled. You need a dedicated workspace, create a key in AI Studio, then `vibe --setup` and paste it (or set `MISTRAL_API_KEY`). AAU also documents Vibe on UCloud.

## Data and hosting facts

- **Training on your data** (help.mistral.ai, 3 Sep 2026): Vibe Enterprise is "opted out of training by default". Vibe on other plans is "not opted out by default" (user or Team admin can turn it off). Studio and API: customers can opt out under Admin > Privacy > "Anonymous improvement data". The Vibe and API toggles are separate. Unverified for AAU: which state AAU's workspaces are in; ask CLAAUDIA.
- **Zero data retention**: official docs say ZDR is available on paid plans for supported stateless API calls, requested via Admin > API > Privacy; Mistral approves case by case. Not available for stateful features (agents, libraries, chat history).
- **Default API retention**: third-party summaries of the privacy policy say 30 days for abuse monitoring unless ZDR is on. Unverified on Mistral's own page.
- **Where it runs**: Regional Endpoints (GA, 11 Aug 2026) let customers choose EU or US inference; "limited, safeguarded transfers to sub-processors" outside the region may occur. Hosted third-party models (DeepSeek, GLM) run under the same regional controls. "EU by default" appears only in third-party sources: unverified.
- **Open weights**: Large 4, Small 4, Ministral 3 can also run on own hardware (Large 4 needs datacenter GPUs).

## What AAU enables (hpc.aau.dk/mistral, CLAAUDIA)

- **Apply first** via the Serviceportal Mistral access form; direct SSO login is disabled until approved. Login: "Continue with AAU - SSO".
- **Default workspace**: Vibe + AI Studio (Playground, Document AI, audio transcription). Level 1 data, no personal data. No API keys.
- **Dedicated workspace (no personal data)**: full Vibe, AI Studio and API, with API keys.
- **Dedicated workspace with personal data** (incl. Level 2/3): needs a WorkZone case number and a DPIA with Grants and Contracts.
- **Rules worth a slide**: chat history deleted after 90 days (Vibe is not an archive); API keys personal, rotated at least every 30 days; monthly token quota per workspace (bigger models use it faster; more on request); no unapproved third-party plugins/tools; MCP only if AAU-managed and approved; no CPR numbers; output reviewed by a person; no uptime guarantee.
- **Use restriction**: the T&C say use "for teaching, commercial, or private purposes is prohibited". The workshop is for researchers, so fine, but do not pitch it for classes.
- AAU's page does not say anything about training on data or hosting location; it defers to Mistral's terms.

## Table: what it is / what researchers would use it for / AAU access

| What it is | What researchers would use it for | AAU access |
|---|---|---|
| **Vibe** (chat.mistral.ai, ex Le Chat) | Ask, draft, summarise; web search; deep research skill | Default workspace (Level 1, no personal data) |
| Vibe **Libraries** | Ask questions across a folder of papers or reports; share with a project group | Default workspace; shareable with AAU users; 100 MB per file |
| Vibe **file analysis + Code Interpreter** | Read a spreadsheet or PDF, make a chart, check numbers | Default workspace (code interpreter is a paid-plan feature; AAU plan not stated) |
| Vibe **connectors / MCP** | Pull from Drive, mail, own tools | Only AAU-managed, approved MCP servers |
| **AI Studio Playground** | Compare models on the same prompt before scaling up | Default workspace |
| **Document AI / OCR 4.1** | Scans and PDFs to Markdown/LaTeX, tables and equations kept | Default workspace (in the browser); API needs dedicated |
| **Voxtral transcription** | Interviews and focus groups to text with speaker labels | Default workspace (browser); personal data needs dedicated workspace + DPIA |
| **Voxtral TTS** | Audio versions of papers, slide voiceovers | API, dedicated workspace (not listed for default) |
| **API + keys** | Scripts, batch coding of texts, OpenCode or Vibe Code | Dedicated workspace only |
| **Agents, Workflows, Batch** | Repeatable pipelines (e.g. classify 10,000 abstracts) | Dedicated workspace (API); quota applies |
| **Vibe Code** (CLI, VS Code) | Coding agent for analysis scripts, papers in LaTeX | Dedicated workspace; key from AI Studio; browser login disabled |
| **Third-party models** (DeepSeek V4.1 Flash, GLM 5.3) | Cheap, strong agent drivers, same contract and region | Via API in dedicated workspace (assumed: AAU does not list models) |

## Sources

- Models overview: https://docs.mistral.ai/getting-started/models/models_overview/
- Large 4 preview (6 Oct 2026): https://mistral.ai/news/mistral-large-4/
- Large 4 open weights (29 Oct 2026): https://mistral.ai/news/mistral-large-4-oss/
- Studio post (5 Nov 2026): https://mistral.ai/news/build-with-studio/
- Voxtral 3 (20 Oct 2026): https://mistral.ai/news/voxtral-3/
- Vibe launch (28 May 2026): https://mistral.ai/news/vibe-agent/ and https://help.mistral.ai/en/articles/682992-le-chat-is-now-vibe
- Vibe docs: https://docs.mistral.ai/vibe and https://docs.mistral.ai/vibe/work/get-started
- Agent tools: https://docs.mistral.ai/studio/agents/agent-tools
- Connectors: https://docs.mistral.ai/studio/connectors/quickstart and https://mistral.ai/news/connectors/
- Workflows (27 Apr 2026): https://mistral.ai/news/workflows/
- Prompts and Skills (9 Jul 2026): https://mistral.ai/news/manage-prompts-and-skills-in-studio/
- Batch: https://docs.mistral.ai/inference/quickstarts/run-a-batch-job
- Fine-tuning (deprecated notice): https://docs.mistral.ai/guides/finetuning/
- Training opt-out (3 Sep 2026): https://help.mistral.ai/en/articles/455207
- Zero data retention: https://docs.mistral.ai/admin/monitor-comply/zero-data-retention
- Regional endpoints (11 Aug 2026): https://mistral.ai/news/regional-inference-open-models-new-compute/
- Vibe CLI releases: https://github.com/mistralai/mistral-vibe/releases
- AAU: https://hpc.aau.dk/mistral/ , https://hpc.aau.dk/mistral/how-to-access/ , https://hpc.aau.dk/mistral/terms-and-conditions/ , https://hpc.aau.dk/mistral/guides/vibe/ , https://hpc.aau.dk/mistral/guides/vibe/vibe-code/ , https://hpc.aau.dk/mistral/guides/ai-studio/ , https://hpc.aau.dk/mistral/guides/responsible-use/
