# The one-prompt version

[`deslop-command.md`](deslop-command.md) is the skill's core rewrite rules in a single prompt you can use anywhere. It's a lighter version of the skill, with no scanner, no second read, and no modes.

## In Raycast

1. Run **Create AI Command**.
2. Paste the whole of `deslop-command.md` as the prompt.
3. Set **Creativity** to **None** or **Low**, so it rewrites rather than adds.
4. Name it (for example, "Deslop"), save it, and give it a hotkey if you like.

Copy some text, run the command, and it returns only the rewritten version. The prompt ends with `{clipboard}`, so it works on whatever you copied last.

## In any chat

Paste the prompt into ChatGPT, Claude, or another chat, replace `{clipboard}` at the end with your text, and send it.
