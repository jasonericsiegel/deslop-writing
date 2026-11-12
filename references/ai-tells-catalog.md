# AI-Tells Catalog

*Catalog version: 1.5*

The subtract half of plain language: patterns that mark prose as machine-made, each with its one-line fix. Drawn from Zinsser, the humanizer skill (blader/humanizer), Wikipedia's *Signs of AI writing*, PubMed frequency data, and editor commentary — not a wholesale import of any single list.

**How to use this:** locate tells in context, then apply the fix. Tells are statistical and era-specific — a word here is a *signal*, not a banned token. Never blanket-delete on sight; check that the rewrite keeps the claim and the voice (see the meaning-preservation and false-positive guardrails in SKILL.md).

**This catalog decays.** Refresh against current data and bump the version line above.

**Contractions are NOT a tell — never expand them.** *We've, isn't, don't, it's* are the plainer, more human form. Expanding them (*we've* → *we have*) is the canonical backwards edit: it makes prose stiffer, not plainer. No row in this catalog licenses it. If you catch yourself expanding contractions to "sound less like AI," stop — that reflex is exactly wrong. (Prefer contractions; see `plain-language-rules.md`.)

## Lexical

| Tell | Fix |
|---|---|
| Inflated vocabulary: *delve, tapestry, testament, underscore, pivotal, crucial, robust, vibrant, garner, boasts, foster, showcase, leverage, harness, landscape* (abstract) | Use the plain, specific word the meaning needs |
| Copula avoidance: *serves as, stands as, marks, represents, features, offers* | Restore *is / are / has* |
| Elegant variation — rotating synonyms for one thing to dodge repetition | Repeat the noun; clarity beats variety |
| Empty intensifiers: *very, really, quite, genuinely, actually* | Cut, or find one word that carries the force |

## Punctuation and typography

| Tell | Fix |
|---|---|
| Em-dash as a default connective (the signature tell): a pair setting off an aside, or a single one splicing two clauses | Default to converting it: period or semicolon between independent clauses, comma or parentheses around an aside, colon before a payoff. Keep an em-dash only where no other mark does the job (a true appositive or a sharp interruptive break), at most one per paragraph. Don't blanket-delete; check each conversion keeps the claim and the voice |
| Title-case headings (*The Key Benefits Of Using AI*) | Sentence case |
| Decorative bold on mid-sentence keywords | Reserve bold for scannable labels |
| Curly quotes where straight quotes are the house style | Match the house style |

## Rhetorical

| Tell | Fix |
|---|---|
| Negative parallelism: *it's not just X, it's Y* / *not merely X but Y* | State the positive claim directly |
| Authority trope: *the real question is… / at its core / what really matters* | Delete the frame; say the thing |
| Drumroll windup — a framing/evaluative clause that only announces a point is coming, then delivers it (often colon-delimited): *The rule is simple: X / The principle that matters here: X / Here's the design point we can't get wrong: X* | Delete the windup; lead with the point. Keep the colon when its left side is a bare noun phrase with no verb or evaluative modifier — genuine enumeration (*three options: …*), a data/code label (*latency: 1,840ms*), or a glossary term (*Stigmergy: …*) |
| Rhetorical setup — a question or teaser posed only so the writer can answer it: *What if I told you…, Ever wonder…, Think about it:, Plot twist:*, and self-answered *Question? Answer.* pairs | Delete the setup; state the point. **Keep a genuine question the text actually investigates** — a real question answered substantively is a legitimate structure, and flattening it into a declarative is a voice loss |
| Vague attribution: *experts argue, observers note, studies show* | Name the source or cut the claim |
| Signposting: *let's dive in, without further ado, in this post we'll* | Delete the frame; state the content |
| Rule of three — forcing ideas into triads to sound complete | Keep what's real; drop the padding |
| False ranges: *from the Big Bang to dark matter* where the ends aren't a real scale | List the actual items |

## Structural

| Tell | Fix |
|---|---|
| Dramatic fragmentation — one claim split into stacked fragments or *And*-chained sentences for beat, or a self-referential closer: *X. And Y. And Z.* / *That's it. That's the whole thing.* | Rejoin into complete sentences and cut the closer. **Keep genuine spoken-voice fragments** that carry the writer's own rhythm — the tell is manufactured beat, not short sentences |
| Superficial *-ing* impact claims: *…, highlighting the growing importance of…* | Make the claim directly or cut it |
| "Challenges and future prospects" boilerplate: *Despite its success, X faces challenges…* | Keep only if you can name them specifically |
| Generic upbeat conclusion: *the future looks bright; exciting times ahead* | End on the last real point |
| Fake-profound kicker — a closing "deep" line that turns the piece's point into an aphorism, metaphor, or mic-drop | **Anchor gate — run this FIRST and obey it.** Does the closing line reuse a concrete noun, number, or fact already established earlier in the piece? **If yes, STOP: keep the line exactly as written.** It is earned, no matter how profound, clever, or mic-drop it sounds — how it *sounds* is not evidence and never overrides this gate. Only if the line fails the gate — it introduces a new abstract noun (*simplicity, discipline, presence, speed, time, technical debt*) and would read the same pasted onto an unrelated piece — is it decorative: delete it and end on the clearest concrete sentence already present. Never rewrite a kicker into a plainer or better line: keep it untouched, or cut it entirely |
| Broader-trend inflation — zooming out to manufacture importance: *reflects a broader shift…, symbolizing…, a new era of…, leaves an indelible mark, underscores its importance* | Cut the zoom-out; state what actually happened and let the reader judge its size |
| Diff-anchored description — describing how a thing *changed* instead of what it *is*: *was added to replace…, formerly…, now updated to…* | Describe the current behavior directly. NOT a tell in a genuine changelog/upgrade note where the change itself is the content |

## Formatting

| Tell | Fix |
|---|---|
| Inline bold-header lists (*- **Performance:** Performance was improved…*) | Prose when ideas relate; restore the connectives |
| Emoji bullets and emoji headings | Remove in editorial/professional contexts |
| Tables for non-comparative content | Use prose unless there's a real comparison |
| Fragmented header — a heading followed by a line that restates it | Delete the warm-up line; start with content |

## Tone and chatbot artifacts

| Tell | Fix |
|---|---|
| Puffery: *groundbreaking, renowned, profound, nestled, breathtaking, must-visit* | State the fact; drop the adjective |
| Sycophancy: *Great question! Certainly! You're absolutely right!* | Delete; answer directly |
| Hedging frames: *it's important to note that / it's worth mentioning that* | Cut the frame; state the point |
| Knowledge-cutoff disclaimers: *as of my last update / while details are scarce* | Cut; state what's known |
| Correspondence leftovers: *I hope this helps / let me know / would you like…* | Remove; it's chat, not content |

## Headings and structure (above the sentence)

- **Sentence case, not Title Case.**
- **No fragmented header** — a heading followed by a one-line restatement of it. Start with the content.
- **No bold-header bullet lists** where ideas relate; write the prose and restore the connective tissue.
- **Plain-language names over index numbers.** Name an ordered set's items so the reader can hold them (*the teaching end*), not *position 2 / bucket 3*.
- **Orientation before the answer.** Lead with enough framing to make the conclusion parseable; don't open with a verdict the reader can't yet decode.
- **Don't over-structure.** Bullets and tables are for scanning and comparison. Prose with logical flow stays prose.
