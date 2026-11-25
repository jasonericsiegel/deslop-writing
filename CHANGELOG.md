# Changelog

## 1.13.1 (2026-11-25)

- Added a link to deslop-writing's page, [jasoneric.com/deslop-writing](https://jasoneric.com/deslop-writing/), in the README.
- Removed two outdated notes from the quality rubric.

## 1.13.0 (2026-11-23)

- The second read now names its model: Sonnet in Claude Code, and GPT-6.1 Terra at medium effort in Codex. If that model isn't available, it uses the one your session is on.
- The fresh agent gets its instructions, your text, and the rewrite, but not the list of AI phrases.
- Fixed: a `codex exec` run could skip the second read. It now starts its own helper agent.

## 1.12.0 (2026-11-12)

First public release.

- Rewrites text in plain, human language: plainer words, shorter sentences, active voice, and the point first.
- Cuts the common tells of AI writing, such as "it's not just X, it's Y", stacked em-dashes, and words like "delve".
- Keeps your meaning and your voice. It checks each simpler word still says the same thing, and leaves code, links, file paths, and quotes alone.
- Picks a mode for the job: quick while your agent writes, normal for casual text, and precision for technical or legal text.
- Checks that every number, date, time, amount, link, file path, code snippet, and quote survives the rewrite, with nothing changed or added.
- A fresh agent, in Claude Code or Codex, reads the rewrite beside your original and flags a changed claim, a new mistake, or a flattened voice, which gets fixed before you see the result.
- Includes the AI-phrase counter and fact check scripts, a grading rubric, and a one-prompt version for Raycast or any chat.
