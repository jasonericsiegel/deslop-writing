---
name: deslop-writing
description: Rewrites prose in plain, human language and strips the tells of AI writing, keeping the meaning and the writer's voice. Use for "deslop this", "make this plainer", or "tighten this". Not for code cleanup.
license: MIT
compatibility: Any agent that loads skills. The optional tell scanner needs Python 3.10 or later.
allowed-tools: Read Write Edit Grep Glob Bash Agent AskUserQuestion
metadata:
  version: 1.13.1
  changed: 2026-11-25
---

# Deslop Writing

Strip the slop and rewrite prose so it reads as a clear, plain, human voice: fewer AI tells, plainer words, less clutter — without losing meaning or flattening the writer. "Deslopping" is the job; **plain language** is the technique it applies. Works on any text, from Claude or from a person.

## Critical rules (read first)

1. **Meaning beats plainness, always.** Never let a simpler word change the claim. Before swapping a word, run the term-of-art test: *does the simpler word make the same claim?* "Near peak" and "near-superintelligent" are different claims — keep the specific one. When unsure, keep the original word.
2. **Edit prose only.** Never rewrite inside code blocks, YAML frontmatter, command snippets, URLs, file paths, or quoted source text. Detect those regions and pass them through untouched.
3. **Bounded and cheap: one pass, plus repairs.** The rewrite pass runs once. Another pass runs only to repair a BLOCKING finding from step 5, up to two passes in all (three for normal mode; inline runs no loop at all). Never run a pass to polish: a note, a tell count, or an edit distance never earns one. That first pass always runs, and it is the pass — not the scanner — that judges whether already-plain text should come back near-verbatim.
4. **Preserve voice.** The goal is to sound like a specific person, not like no one. Match the input's rhythm and word level; if a voice sample is provided, match it.

## The two halves

Deslopping is two steps fused into one move — but they are not equal partners. The rewrite is the engine; the tell-scan only checks the work.

- **Add plain-language discipline — the primary move.** Short common words for fancy ones, cut clutter, active sentences, one clear claim per line, run-on sentences broken up. This is where most of the work happens. Load `references/plain-language-rules.md`.
- **Subtract the AI tells — a check, not the engine.** A mostly mechanical, catalogued set of patterns. Load `references/ai-tells-catalog.md`. The tell-scanner (`scripts/scan_tells.py`) locates mechanical tells, but finding and clipping tells is *not* rewriting for plainness — and it never substitutes for it.

The tells are the symptom; the rewrite is the treatment; the scanner only checks the work. Voice and meaning are what you must not kill applying it. The skill's core failure mode is stopping at the subtract half — clipping em-dashes and intensifiers, then returning prose that was never actually rewritten plainer.

## Modes (pick one)

Three modes. Two axes decide which one: **is there a saved artifact to edit, or am I writing the prose right now?** and, for an artifact, **how precious are its terms?**

| Mode | When | Behavior |
|---|---|---|
| **inline (quick)** | No artifact to edit — the prose is the response being written right now, in this context. "Explain X, deslopped." A chat answer, a message, a paragraph drafted mid-conversation | Load `references/drafting-rules.md` and apply it **while drafting**. No scanner, no subagent audit, no loop. The rules shape the sentence as it forms rather than repairing it afterwards. The output is the response itself, so there is nothing to return separately and nothing to audit — the draft rules either governed the writing or they didn't. |
| **normal (loose)** | An artifact of casual / reflective everyday prose with **no precious terms** — a personal note, an impressions email, fresh AI copy being de-slopped | Cut padding and rebuild crisper, flattening freely for maximum plainness and economy. You're creating the voice as you go. Meaning still holds, but there are no terms to protect. Full pipeline, 3-pass cap. |
| **precision (accurate)** | An artifact where a flattened term or softened claim is a real loss — technical/legal/spec prose, reports, plans, anything terms-dense | Cut clear tells and genuinely improve plainness, but protect meaning + terms of art **above** plainness. Precision does NOT mean skipping the work — the rewrite pass (step 4) always runs, and skipping it is the failure. Judge the result against the input on the rewrite dimensions, not on how different it looks: break giant run-ons into shorter sentences **even if every term and claim is already preserved** — a run-on that keeps all its meaning still fails on plainness. A clean tell-scan never licenses skipping the rewrite (a clean scan means few mechanical tells, not that the prose is already plain). But when the rewrite pass has run and found nothing left to improve, returning the text near-verbatim is the **correct** result, not a failure. The one thing you never do: flatten a genuine term-of-art to look plainer. Full pipeline, 2-pass cap. |

### Selection rule

**An explicitly named mode always wins.** The caller saying "inline", "quick", "normal", "loose", "precision", or "accurate" ends the decision — the router below never overrides a named mode, and never second-guesses it even when the target looks like a different mode's job.

Absent a named mode, route on the target:

1. **No artifact — the text is this response** → **inline (quick)**. The tell: nothing was handed over. No path, no pasted block, no prior draft. The user asked for something to be written or explained and attached the skill to how it should read.
2. **An artifact, terms-dense** → **precision (accurate)**. A file path, a pasted block, or a prior draft, holding technical/legal/spec prose.
3. **An artifact, casual with no precious terms** → **normal (loose)**.

Between the two artifact modes, **precision is the default** — pick normal only when the content is plainly casual. The wrong-mode penalty is **asymmetric**: running *normal* on terms-dense text catastrophically flattens terms-of-art, while running *precision* on casual text only leaves mild clutter.

Authorship does **not** decide the mode. Claude generates precision prose too, so "Claude wrote it" never implies normal.

**Aliases (backward-compatible):** `loose` = `normal`, `aggressive` = `normal`, `conservative` = `precision`, `quick` = `inline`. Callers and pipelines that pass the old names still work.

### Announce the mode

Every interactive run opens by stating the mode as a three-item checklist, so the roster is visible and the pick is checkable:

```
- [x] inline (quick)
- [ ] normal (loose)
- [ ] precision (accurate)
```

Add ` — named by caller` or ` — auto-routed` after the checked line, so an override is distinguishable from a guess. Wrong pick → the user renames the mode and the run restarts in it.

The announcement is **chat output, never part of the rewritten text**, and it is **suppressed entirely when running headless or called as a pass from another skill** — those callers consume the returned text as data, and a checklist prepended to it would corrupt the output. Step 7's "return only the rewritten text" still holds absolutely for the returned artifact.

## Pipeline

**Inline (quick) does not run this pipeline.** Inline has no artifact to scope, scan, or audit — it loads `references/drafting-rules.md` and writes. That's the whole procedure. Announce the mode, then write the response under those rules. Steps 1–7 below are for **normal** and **precision** only.

Run these in order. Do not skip the scoping or the audit.

1. **Scope.** Isolate editable prose. Mark and protect code blocks, frontmatter, quotes, URLs, paths. Only the prose regions get edited.
2. **Pre-scan (informational — never a gate).** Run the tell scanner:
   ```bash
   python3 scripts/scan_tells.py --file <path>
   # or: ... scan_tells.py --stdin   (pipe text in)
   ```
   It prints a tell count, density, and a count for each kind of tell. Use it to *locate* mechanical tells — not to decide whether to rewrite. **A low or clean scan never licenses skipping the rewrite pass.** The scanner counts mechanical tells (em-dashes, intensifiers); it is blind to the things the rewrite pass exists to fix — long words, clutter, run-on sentences, clause-packing. A low density just means *fewer mechanical tells to cut*; the rewrite pass (step 4) still runs and judges the prose on those dimensions. The only real short-circuit is text already plain on the rewrite dimensions too — short sentences, plain words, no clutter — and that call is made by the rewrite pass reading the prose, never by the scanner's count. When in doubt, run the full pipeline.
3. **Subtract (cleanup — secondary).** Apply the tells catalog. Cut or rewrite each located tell per its fix. This clears mechanical noise so the rewrite can work; it is not itself the rewrite. **Every located tell is resolved — cut it, or keep it deliberately under its row's keep-clause.** A catalogued tell is a specific, named thing, so removing it is never churn; the licence to return already-plain prose near-verbatim applies to the rewrite pass in step 4, and never to leaving a located tell standing out of caution.
4. **Add — the primary pass, where most of the work happens.** Apply the plain-language rules and genuinely rewrite the text: plain words for fancy ones, cut clutter, active voice, lead with the point, one idea per line, break run-on sentences into shorter ones. Text that only had its mechanical tells clipped in step 3 but was not rewritten on these dimensions has NOT been made plain — do not stop at subtract.
5. **Audit with fresh eyes.** First run the fact check, `python3 scripts/check_facts.py <input> <rewrite>`. It lists every figure, link, path, code span, and quote the rewrite dropped, changed, or added. A changed or added one is BLOCKING. A dropped one is BLOCKING unless it only counted something the rewrite still shows in full ("3 tips" above a list of three). Then dispatch a **fresh subagent** with **both the input and the rewrite**: in Claude Code the Agent tool (read-only Explore, `model: sonnet`), in Codex `spawn_agent` (`model: gpt-6.1-terra`, `reasoning_effort: medium`, `fork_turns: none`), in a `codex exec` run too. If that model isn't available, use the session's own. Give the auditor this prompt and the two texts, not the catalog. The prompt: *"What still reads as AI-generated here? List remaining tells. Then: did any rewrite change a claim, or flatten the voice? Finally — comparing the two, is the rewrite genuinely plainer on words, clutter, and sentence length? If it came back near-identical, is that because the input was already plain, or because the rewrite pass never really ran? Last, mark as BLOCKING any error the rewrite introduced (broken grammar, a typo, a dropped word) and any claim it changed. For each one, quote the input's words and the rewrite's words side by side and say what changed. A concern that depends on something you can't check from the input ('only if speed is unverified') is a note, not BLOCKING. Everything else is a note."* Do not run the audit inline in the context that wrote the rewrite — the writer is blind to its own tells. (Only a script, or a harness with no subagent tool: a separate `claude -p --model sonnet` or `codex exec --sandbox read-only -m gpt-6.1-terra -c model_reasoning_effort=medium` call with a clean prompt; see "From a script" below.)

   That last question is what keeps step 4 honest. "The rewrite pass ran and found nothing to improve" is otherwise an unfalsifiable claim by the same context that would benefit from skipping the work, and no scanner can check it — the scanner is blind to exactly the dimensions the rewrite pass owns. A fresh reader holding both versions can check it, so that reader is the gate, not the writer's own say-so.

   **Fix every BLOCKING finding before moving on.** It is a defect in the output, and the scanner cannot see it, so a clean scan never closes it. Repair only the quoted passage, with the input as the source of truth, then run the fact check and the audit again on the repaired draft. Each repair and re-audit counts as a pass. If a BLOCKING finding is still open on the last pass, put back the input's own words for the claim it names, and only those: a catalogued tell around them that carries no part of the claim (a frame like "In essence," or "It's important to note that") still goes. Never ship a changed claim, and never go past the cap. Notes are optional, and a note alone never earns another pass.
6. **Stop.** Once the fact check and the audit leave no BLOCKING finding open, return the draft. That is usually after the first pass. After a repair pass, `scan_tells.py --diff <prior> <new>` confirms the repair added no new tells; it never decides whether to run another pass. Hard cap: 2 passes (3 for normal). Stop even if not "perfect" — over-editing sands out the voice. If a *caller* keeps sending prose this pass returns near-verbatim, that is a signal to tighten the rules upstream of that caller so the prose arrives good, not a signal to edit more aggressively here.
7. **Return.** Output **only the rewritten text** — no preamble, no "here's my rewrite," no self-audit notes or commentary. The audit happens in step 5; its notes are working scratch, not output. Append a short grouped change list (what was cut and why) **only if the caller explicitly asked for one**.

## Guardrails

- **Meaning-preservation (top guardrail).** The term-of-art test from rule 1. A genuine technical term that *is* the concept stays. Decorative jargon goes.
- **Voice-preservation.** Don't iron a real author into corporate-neutral. Match their sentence length and word level.
- **Register-fit.** In legal, scientific, or technical text, some complexity is load-bearing. Plain is not dumbed-down. Don't strip a qualifier or term the reader needs to judge the claim.
- **False-positive caution.** Tells are statistical and era-specific. Em-dashes and words like "delve" have honest human uses. Flag tells in context; never blanket-delete a word on sight.
- **Judgment over checklist.** Running every rule at full strength produces flat prose — the very thing this fixes. Break any rule sooner than write something clumsy.

## Running headless or from another skill

This skill is a callable cleanup pass. Contract:

- **Input:** a block of text or a file path, an optional mode (`precision` (default) / `normal`; aliases `loose`/`aggressive`/`conservative` accepted), and an optional voice sample.
- **Output:** the rewritten text, and nothing else. **No mode checklist** — the announcement is interactive-only, and prepending it here would corrupt the returned text.
- **Inline is not available headless.** Inline means "the model applies drafting rules to prose it is writing in its own context." A headless caller handing over text has an artifact by definition, so it gets `precision` or `normal`. A caller that wants drafting discipline in its own generation should load `references/drafting-rules.md` directly rather than calling this skill.
- **From a script** (an agent run with `claude -p` or `codex exec` has a subagent tool, so it uses step 5's): shell out to the `claude` CLI (subscription, never the API) with the catalog and rules as context. Run `scripts/check_facts.py`, then the audit as a **second, separate** `claude` or `codex exec` call, on the models step 5 names, so the auditor has fresh eyes, and handle its BLOCKING findings as step 5 says. One rewrite pass, plus repair passes up to the cap, so a script never loops unbounded.
- **From another skill/workflow:** call this as the final "make the output plain" step before text ships (an email, a report, a digest). Default is `precision`; pass `normal` only for casual text with no precious terms — fresh generation alone does NOT imply normal (Claude also generates technical/precision prose, where normal would flatten terms).

## Improving this skill (evals)

This skill is meant to get sharper on real text over time. Use the eval loop.

- Grade against `references/quality-rubric.md` (five dimensions: meaning fidelity, plainness, terms-of-art, voice, economy).
- **Test the rules and prompts, not just the process.** A rule earns its place only if an eval shows it helps without overreaching; a prompt's exact wording is itself a variant to test. Also A/B the open questions: loop vs. single combined pass (on **cost and quality**). (The auditor's model is settled: step 5 names it. Retest when a newer model replaces either. The precision-vs-loose default question is settled — see Modes; precision is the safe default. Grade precision content under the rubric's PRECISION profile, casual content under LOOSE.)
- Lock a gold set of before/after pairs with confirmed labels: pick the pairs, agree the labels, calibrate the boundary calls, then freeze the set.
- When a graded failure teaches a new rule or guardrail, add it to the matching reference file (`references/ai-tells-catalog.md`, `references/plain-language-rules.md`, or `references/drafting-rules.md`) and bump that file's version line. That is the compounding loop.

## References (load on demand)

- `references/drafting-rules.md` — moves for writing prose plainly in the first place. **Load in inline (quick) mode**, where it is the only reference the mode uses.
- `references/ai-tells-catalog.md` — the versioned tell catalog (the subtract half). Load at step 3.
- `references/plain-language-rules.md` — the validated Zinsser block + plain-language canon (the add half). Load at step 4.
- `references/quality-rubric.md` — the five-dimension grading rubric. Load when running an eval.
