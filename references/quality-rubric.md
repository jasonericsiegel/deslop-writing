# Plain Language — Quality Rubric

*Rubric version: 1.2*

Grade a plain-language rewrite against five dimensions, 0–2 each. Use this rubric to test variants — and remember the rule from SKILL.md: **test the rules and prompts themselves, not only the process.** A passing grade on a weak rewrite is worse than useless.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| **Meaning fidelity** | A claim was lost or changed | Minor nuance softened | Full meaning preserved, nothing substantive lost |
| **Plainness** | Still cluttered or jargon-heavy | Some clutter remains | Stripped to cleanest form, no needless jargon |
| **Terms-of-art preservation** | A real technical term was flattened | One borderline call wrong | Genuine terms kept, decorative jargon cut |
| **Voice** | Flattened to corporate-neutral, or voice destroyed | Voice partly muted | Sounds like a specific person, not no one |
| **Sentence economy** | Expanded or padded | Roughly same length | Tighter, no wasted words |

## Weighting profiles

The five raw dimension scores (0–2) are the same regardless of profile. What changes is the **weight** each dimension carries when you sum a variant's total. Three profiles; pick the one that matches the *content* being edited, not the rewriter's mood.

| Dimension | NEUTRAL (v1.0) | PRECISION | LOOSE |
|---|---|---|---|
| Meaning fidelity | 1 | **3** | 2 |
| Terms-of-art | 1 | **3** | 1 |
| Plainness | 1 | 1 | **3** |
| Voice | 1 | 2 | 2 |
| Sentence economy | 1 | 1 | 2 |
| **Max weighted total** | **10** | **20** | **20** |

**Weighted total = Σ (dimension score × profile weight).** Normalize to a percentage (weighted total ÷ max) when comparing across profiles.

- **NEUTRAL** — the original equal-weight scorecard. General-purpose; use when content type is genuinely mixed or unknown. *Known limitation: on terms-heavy text it lets a baseline that flattens terms to look "plainer" tie a skill that protects them. Don't use it to grade precision content.*
- **PRECISION** — for terms-heavy / meaning-sensitive text (technical prose, debriefs with names + decisions, anything where a flattened term is a real loss). Weights **meaning + terms-of-art at 3×**, plainness at 1×. Reflects the real job: edit someone else's careful prose without breaking it. A rewrite that buys plainness by dropping a claim or flattening a term should *lose* here — that's the point.
- **LOOSE** — for casual / reflective everyday prose with no precious terms (an impressions email, a personal note, fresh AI-generated copy being de-slopped). Weights **plainness at 3×, economy at 2×**, terms at 1× (there are few to protect). Aggressive flattening is *good* here; meaning still matters (2×) so it can't go fully off the rails.

**Mode ↔ profile pairing (for the two-mode design):** grade PRECISION-mode rewrites of precision content under the PRECISION profile; grade LOOSE-mode rewrites of casual content under the LOOSE profile. The two-mode hypothesis holds if each mode wins on its home-turf content under that content's profile.

## Grading a fresh draft (drafted-cell re-anchoring)

Everything above grades a **rewrite** — an edit of a source text you can compare against. Two of the five dimensions have no meaning without that source, so grading a draft written from scratch needs them re-anchored.

| Dimension | Editing an existing text (default) | Grading a fresh draft |
|---|---|---|
| **Meaning fidelity** | Faithful to the source text | Faithful to the brief and its source notes; nothing invented, nothing required left out |
| **Terms-of-art** | Genuine terms in the source survived | Kept the terms the source notes require |
| Plainness, Voice, Sentence economy | unchanged | unchanged |

Same five dimensions, same 0–2 scale, same weighting profiles. Only the referent moves: from *the text this was edited from* to *the brief this was written from*.

**Which column to use depends on the question, not on whether a source text happens to exist.**

- **Grading an edit** — "did this pass improve the text it was given?" — use the default column and grade against the source. This is the skill's everyday case.
- **Comparing candidate final artifacts** — "which of these is the better piece of writing?" — use the drafted column for **all** of them, including ones produced by editing something else. They are competing as deliverables, so they all grade against the same referent: the brief.

The second case is easy to get wrong. In a four-variant design where B is `deslop(A)`, grading A against the brief but B against A scores A on *how good a draft is* and B on *how good an edit is*. Those are different constructs, and a ranking that mixes them is meaningless no matter how carefully each half was scored. When the four are being ranked against each other, all four grade against the brief.

**What the re-anchoring costs, stated plainly.** Re-anchoring a dimension changes the construct it measures. Shared dimension names do **not** make the numbers comparable across constructs, so drafted-cell scores are a new benchmark starting at zero. Never plot them against editing-side eval history.

**Voice is weak on a fresh draft** with no voice sample to match. Every brief must carry an explicit voice target, or the voice dimension is reported as low-confidence for that brief.

## How to run an eval (sketch)

1. **Gold set.** Collect before/after pairs with confirmed labels. Lock the labels, calibrate the boundary calls, then freeze the set.
2. **Variants to test.** The skill's open questions are the variants:
   - Rule content — does each catalog/rule line earn its place, or does removing it not hurt (or help)?
   - Prompt wording — the exact phrasing that applies a rule without overreaching.
   - Process — one combined pass vs. subtract → add → audit loop, graded on **cost and quality**.
   - Auditor — same-model fresh inference vs. a different (cheaper) model vs. human.
3. **Judge.** Score each output on the five dimensions. Watch for the known failure mode: over-simplification that flattens a term of art (the meaning-fidelity dimension catches it).
4. **Confirmation round.** Re-test the apparent winner on fresh cases before locking it in.
5. **Feed the catalog.** When a graded failure teaches a new rule or guardrail, add it to the matching reference file and bump that file's version line. That is the compounding loop.
