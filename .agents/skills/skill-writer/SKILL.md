---
name: skill-writer
description: Write a new skill (a reusable one-page recipe for the agent) for a task the user repeats - coding interviews, cleaning a survey export, extracting data from reports, making slides. Use when the user says "make a skill for...", "I always do X", or wants the agent to do a task the same way every time.
---

1. **Ask, in one message:** what the task is, what goes in and what should come out (an example file helps), and what must never happen. Then a few follow-ups if needed. Summarise in three lines and check.
2. **Write** `.agents/skills/<short-name>/SKILL.md`: a front matter with `name` and a `description` that uses the user's own words for when to use it (this line decides when the agent picks the skill), then the goal in one line, the steps, the checks, the don'ts. Under half a page. If it processes data or documents, say "Work as in the `notebook` skill".
3. **Test** it on the user's example, show the result, fix the skill (not just the output), and run again until the user is happy. It also works in Claude Code (`.claude/skills/` points to the same folder).
