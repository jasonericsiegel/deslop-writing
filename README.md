# deslop-writing

deslop-writing is a free skill for Claude Code, Codex, and other AI agents. Ask your agent to deslop some text, and it rewrites it in plain, human language: plainer words, shorter sentences, and none of the phrases that make writing sound like AI. It's built to keep your meaning and your voice.

```sh
npx skills add jasonericsiegel/deslop-writing
```

![A bike club newsletter sentence, deslopped in Normal mode, shown as tracked changes. Struck in red: "Exciting news! We're thrilled to announce that our", "isn't just a ride — it's a", "vibrant community experience that fosters connection", and "showcases the breathtaking beauty of". In green: "Our", "is a", "chance to meet people", and "see". The result reads: Our Saturday group ride is a chance to meet people and see the riverfront.](media/deslop-before-after.png)

## What it does

A bike club's newsletter, before:

> Exciting news! We're thrilled to announce that our Saturday group ride isn't just a ride — it's a vibrant community experience that fosters connection and showcases the breathtaking beauty of the riverfront. Whether you're a seasoned cyclist or just starting your journey, there's something for everyone. It's important to note that helmets are required. Let's dive into what's new: the ride now leaves at 9:00 AM instead of 8:00 AM, and we've added a coffee stop at mile 12. See you on the road!

After, in Normal mode:

> Our Saturday group ride is a chance to meet people and see the riverfront. Everyone is welcome, whether you ride every week or are just starting out. Helmets are required. The ride now leaves at 9:00 AM instead of 8:00 AM, and we've added a coffee stop at mile 12. See you on the road!

Every fact stayed, down to the start times and the mile marker.

Technical writing keeps its technical terms. Here the rewrite drops the filler but keeps "write-through policy" and "stale reads", because plainer words would change what the sentences claim:

> It's important to note that the cache plays a pivotal role in our checkout service. It leverages a write-through policy, which serves as a robust safeguard against stale reads — even under heavy concurrent load. This ensures that customers always see accurate inventory counts.

After, in Precision mode:

> The cache is central to our checkout service. It uses a write-through policy, a strong safeguard against stale reads even under heavy concurrent load. So customers always see accurate inventory counts.

Both samples are real output from this skill, run on text made up for this page.

## What it changes, and what it leaves alone

It cuts more than 30 kinds of AI phrases. Some of them:

- Puffed-up words like "delve", "pivotal", "robust", and "leverage".
- Set phrases like "it's not just X, it's Y", "it's important to note that", and "let's dive in".
- Em-dashes used everywhere, empty words like "very" and "truly", and closing lines that sound deep but say nothing.

It rewrites with about 15 plain-language rules, such as:

- The plain word over the fancy one, and active sentences.
- Long sentences broken up, one idea at a time, and the point first.

It leaves alone:

- Your meaning. Before it swaps a word, it checks that the simpler word says the same thing. If not, the original stays.
- Your voice. It keeps your rhythm and word choice, and it can match a sample of your writing.
- Your facts. A script checks that every number, date, time, amount, link, and file path is still there, unchanged, and that nothing new crept in.
- Code and quotes.

## Install

1. Open your agent:
   - **Claude desktop app:** open the **Code** tab, choose a folder to work in (Documents is fine), and use a **Local** session for this step. Cloud sessions are below.
   - **ChatGPT desktop app:** switch to **Codex** at the top of the window, choose a folder, and use **Local** for this step.
   - **Claude Code, Codex, Cursor, Copilot, Gemini CLI, or another agent in a terminal or code editor:** open it as usual.
2. Paste this in:

   > Install the deslop-writing skill from https://github.com/jasonericsiegel/deslop-writing

3. Start a new chat in the same place, so your agent loads the skill, and try it:

   > Write me a short welcome note for a new neighbor, deslopped.

No agent? Paste the [one-prompt version](raycast/deslop-command.md) into any chat with your text. See [Use it without an agent](#use-it-without-an-agent).

<details>
<summary>Use it in Claude chats and cloud sessions</summary>

A cloud session runs on Anthropic's or OpenAI's computers, so it can't see the skills folder on yours. It needs a slightly different setup.

**Claude (claude.ai, the Claude apps, and Claude Code cloud sessions).** Add the skill to your Claude account once. Regular Claude chats can then use it, with code execution turned on in **Settings → Capabilities**, and Claude Code cloud sessions load it on their own.

1. [Download this repository as a ZIP](https://github.com/jasonericsiegel/deslop-writing/archive/refs/heads/main.zip) and unzip it.
2. Rename the folder from `deslop-writing-main` to `deslop-writing`, then compress that folder into a new ZIP.
3. In Claude, open **Customize → Skills**, press **+**, then **Create skill → Upload a skill**, and choose the new ZIP.

**One project, in any cloud agent.** Commit the `deslop-writing` folder to the project's repository, in `.claude/skills/` for Claude Code or `.agents/skills/` for Codex. Every cloud session on that repository then has it.

Claude Code cloud sessions are documented to work this way, and Codex cloud tasks should too. Neither has been tested yet. In a regular Claude chat, the second read by a fresh agent may be skipped, because starting a separate agent is a Claude Code feature.

</details>

<details>
<summary>Install from a terminal instead</summary>

Use Vercel's `skills` installer, which needs [Node.js](https://nodejs.org) 22.20 or later and asks which agents to install for:

```sh
npx skills add jasonericsiegel/deslop-writing -g
```

The installer sends anonymous install details (the repo, skill, and agent names) to skills.sh by default. Put `DISABLE_TELEMETRY=1` in front of the command to turn that off.

Or copy the folder with git:

```sh
git clone https://github.com/jasonericsiegel/deslop-writing ~/.claude/skills/deslop-writing
```

That's the Claude Code folder. Codex, Cursor, GitHub Copilot, Gemini CLI, and most other agents read `~/.agents/skills/` instead.

</details>

<details>
<summary>Install by hand</summary>

1. [Download this repository as a ZIP](https://github.com/jasonericsiegel/deslop-writing/archive/refs/heads/main.zip) and unzip it.
2. Rename the folder from `deslop-writing-main` to `deslop-writing`.
3. Move it into `~/.claude/skills/` for Claude Code, or `~/.agents/skills/` for Codex and most other agents. These folders are hidden in your home folder: in Finder, press ⇧⌘G and paste the path. Create the folder if it's missing.
4. Start a new chat with your agent.

</details>

To remove it, ask your agent to remove the deslop-writing skill, or delete the `deslop-writing` folder from `~/.claude/skills/` or `~/.agents/skills/`.

## Use it

Ask in your own words, for example:

- "**Deslop this**" with the text pasted after it.
- "**Make this plainer**: `draft.md`"
- "**Tighten this** email before I send it."
- "Explain how DNS works, **deslopped**."
- "Deslop this contract summary in **precision mode**."
- "**Deslop** my LinkedIn post, **normal mode**."

Your agent says which of three modes it picked. Name one in your request, as in the last two, and it uses that one instead:

| Mode | When | What it does |
|---|---|---|
| **Quick** | Your agent is writing something new for you | Writes plainly from the start, with no second pass |
| **Normal** | Casual text: a note, an email, a post | Rewrites freely for the plainest, shortest version |
| **Precision** | Technical, legal, or other careful text | Rewrites too, but never trades a precise term for a plainer one |

With no mode named, it picks Precision for text you hand it unless the text is plainly casual. Running Normal on careful writing can blur a precise term; running Precision on casual text only leaves a little extra wording.

Other skills and scripts can call it as a last cleanup step before text goes out. It then returns only the rewritten text.

## How it works

A skill is a folder of instructions and small scripts that your agent can use. Claude Code is Anthropic's agent, also found in the Code tab of the Claude desktop app. Codex is OpenAI's, also found in the ChatGPT desktop app.

For text you hand it, your agent:

1. Sets aside code, links, file paths, and quotes, so they come back untouched.
2. Runs a small script that counts the most common AI phrases, as a quick check.
3. Cuts or fixes each AI phrase it finds.
4. Rewrites the text for plain language. This is the main step: a text with no AI phrases can still be wordy.
5. Runs a second script that compares the rewrite with your original and lists any number, date, link, path, code, or quote that was dropped, changed, or added.
6. Asks a fresh agent, one that didn't write the rewrite, to compare the two. It looks for a changed claim, a new mistake, or a flattened voice. Anything either check finds gets fixed. If a fix doesn't hold, your own words for that claim go back in.
7. Stops. One rewrite is the norm. Another round runs only to fix something a check found, and never more than two or three in all, so it doesn't keep rewriting past the point where it helps.

The second read adds a little time and usage to each run. Both scripts read only the text they're given and make no network calls.

The rules live in plain Markdown files in `references/`, so you can read or change them. New rules are tested side by side against the current version before they go in.

## Use it without an agent

[`raycast/deslop-command.md`](raycast/deslop-command.md) has the core rewrite rules in one prompt. Paste it into ChatGPT, Claude, or another chat with your text, or save it as a Raycast AI command. It's a lighter version of the skill, with no scanner, no second read, and no modes. [Setup steps](raycast/README.md).

## Better together

deslop-writing works on its own. When both are installed, [human-feedback](https://github.com/jasonericsiegel/human-feedback) uses it to write plainer questions and replies on its review pages.

## How it compares

What you get with deslop-writing:

- **It rewrites the whole text.** It cuts the AI phrases first, then rewrites what's left so it reads plainly.
- **It keeps what you meant.** A precise word stays when a plainer one would change the claim, and a script checks that every number, date, and link survived.
- **A second read before you see it.** In Claude Code or Codex, a fresh agent compares the rewrite with your original and flags a changed claim, a new mistake, or a flattened voice. It can still miss something, so read the result before you send it.
- **Two kinds of rewrite.** Precision mode protects technical and legal terms; Normal mode trims freely.
- **It helps your agent write plainly to begin with**, not only clean up afterwards.
- **You can change it.** The rules are plain Markdown files your agent reads.

What each tool can do:

| What you can do | deslop-writing | [humanizer](https://github.com/blader/humanizer) | [stop-slop](https://github.com/hardikpandya/stop-slop) | [unslop](https://github.com/theclaymethod/unslop) | [Grammarly AI Humanizer](https://www.grammarly.com/ai-humanizer) |
|---|:---:|:---:|:---:|:---:|:---:|
| Get a plain rewrite, not just AI phrases removed | ✅ | Partly | Partly | ✅ | ✅ |
| Keep code, links, and quotes exactly as they were | ✅ | ✅ | — | ✅ | — |
| Keep precise terms in technical or legal writing | ✅ | — | — | ✅ | — |
| Match your own voice from a sample | ✅ | ✅ | — | ✅ | ✅ |
| Have a second, fresh read check the rewrite for changed meaning | ✅ | — | — | — | — |
| Have your agent write plainly from the start | ✅ | — | — | Partly | — |
| Use it in Claude Code, Codex, and other agents | ✅ | ✅ | Partly | ✅ | — |
| Count AI phrases with a script, not only by asking the model | ✅ | — | — | ✅ | — |
| Check with a script that numbers, dates, and links survived | ✅ | — | — | ✅ | — |
| Use it free | ✅ | ✅ | ✅ | ✅ | Free tier |

— means we didn't find it in that tool's documentation, as of November 2026. "Partly" means its documentation describes a narrower version.

**Compared with asking your agent to "make this plainer":** deslop-writing adds checks a plain request doesn't: it tests that each simpler word says the same thing, checks with a script that every number and link survived, and has a fresh agent read the result.

## License

MIT. Two entries in the AI-phrase list are adapted from [humanizer](https://github.com/blader/humanizer) by Siqi Chen, also MIT. The full terms are in [LICENSE](LICENSE).

## Found a problem or have an idea?

[Open an issue](https://github.com/jasonericsiegel/deslop-writing/issues/new/choose). A before-and-after sample helps most. Code contributions aren't accepted; see [CONTRIBUTING.md](CONTRIBUTING.md). Changes are listed in [CHANGELOG.md](CHANGELOG.md).

Made by [Jason Eric Siegel](https://www.linkedin.com/in/jasonericsiegel) · [More of my work on GitHub](https://github.com/jasonericsiegel)
