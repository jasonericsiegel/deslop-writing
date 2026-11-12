#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Check that a rewrite kept the original's facts.

Compares two texts and reports every figure, link, path, code span and quote
that the rewrite dropped, changed or added. A rewrite may move these around or
spell "two" as "2"; it may not lose one, alter one ("$47.3 million" to
"$47.3 billion") or invent one ("9:00" to "9:00 PM").

Usage:
  check_facts.py ORIGINAL REWRITE
  add --json for machine-readable output

Exit codes: 0 = every fact kept, 1 = a fact was dropped, changed or added,
2 = usage error.
"""
from __future__ import annotations

import json
import re
import sys

KINDS = ("numbers", "links", "paths", "code", "quotes")

_WORDS = {w: str(i) for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen "
    "fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}
_UNITS = (r"(?:%|percent|million|billion|trillion|thousand|[kmb]n?\b|ms|s\b|sec|min|"
          r"hours?|hrs?|days?|weeks?|months?|years?|km|kg|mb|gb|tb|px|x\b)")

_FENCE = re.compile(r"(```|~~~)[^\n]*\n(.*?)\1", re.S)
_INLINE = re.compile(r"`([^`\n]+)`")
_LINK = re.compile(r"https?://[^\s<>()\"']+|[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
_PATH = re.compile(r"(?<![\w/])(?:~|\.{1,2})?/[\w.~-]+(?:/[\w.~-]+)*|(?<![\w/])[\w-]+/[\w.-]+\.\w{1,5}\b")
_QUOTE = re.compile(r"[\"“]([^\"“”\n]+)[\"”]")
_BLOCKQUOTE = re.compile(r"^\s*>\s?(.+)$", re.M)
_DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}/\d{1,2}/\d{2,4}\b")
_VERSION = re.compile(r"\bv?\d+(?:\.\d+){2,}\b")
_TIME = re.compile(r"\b\d{1,2}(?::\d{2})?\s*([ap])\.?\s?m\b\.?|\b\d{1,2}:\d{2}\b", re.I)
_ORDINAL = re.compile(r"\b\d+(?:st|nd|rd|th)\b", re.I)
_NUMBER = re.compile(r"(\$|€|£)?\s?(\d[\d,]*(?:\.\d+)?)\s?(" + _UNITS + r")?", re.I)
_NUMWORD = re.compile(r"\b(" + "|".join(_WORDS) + r")\b", re.I)


def _strip_frontmatter(text: str) -> str:
    return re.sub(r"\A---\n.*?\n---\n", "", text, count=1, flags=re.S)


def extract(text: str) -> dict[str, set[str]]:
    """Return the facts in text, grouped by kind and normalized for comparison."""
    out: dict[str, set[str]] = {k: set() for k in KINDS}
    text = _strip_frontmatter(text)

    for m in _FENCE.finditer(text):
        out["code"].add(m.group(2).strip())
    text = _FENCE.sub(" ", text)
    for m in _INLINE.finditer(text):
        out["code"].add(m.group(1).strip())
    text = _INLINE.sub(" ", text)

    for m in _LINK.finditer(text):
        out["links"].add(m.group(0).rstrip(".,;:!?"))
    text = _LINK.sub(" ", text)
    for m in _PATH.finditer(text):
        out["paths"].add(m.group(0).rstrip(".,;:!?"))
    text = _PATH.sub(" ", text)

    for m in _BLOCKQUOTE.finditer(text):
        out["quotes"].add(m.group(1).strip())
    for m in _QUOTE.finditer(text):
        if len(m.group(1).split()) > 1:  # one word in quotes is usually a scare quote
            out["quotes"].add(m.group(1).strip())

    nums = out["numbers"]
    for pattern in (_DATE, _VERSION):
        for m in pattern.finditer(text):
            nums.add(m.group(0).lower())
        text = pattern.sub(" ", text)
    for m in _TIME.finditer(text):
        base = re.match(r"\d{1,2}(?::\d{2})?", m.group(0)).group(0)
        nums.add(base + (m.group(1).lower() + "m" if m.group(1) else ""))
    text = _TIME.sub(" ", text)
    for m in _ORDINAL.finditer(text):
        nums.add(m.group(0).lower())
    text = _ORDINAL.sub(" ", text)
    for m in _NUMBER.finditer(text):
        cur, value, unit = m.group(1) or "", m.group(2).replace(",", ""), (m.group(3) or "")
        nums.add(cur + value + unit.lower().replace(" ", ""))
    for m in _NUMWORD.finditer(text):
        nums.add(_WORDS[m.group(1).lower()])
    return out


def compare(original: str, rewrite: str) -> dict:
    """Facts the rewrite dropped (missing) or brought in (added), by kind."""
    a, b = extract(original), extract(rewrite)
    missing = {k: sorted(a[k] - b[k]) for k in KINDS if a[k] - b[k]}
    added = {k: sorted(b[k] - a[k]) for k in KINDS if b[k] - a[k]}
    return {"ok": not missing and not added, "missing": missing, "added": added}


def main(argv: list[str]) -> int:
    as_json = "--json" in argv
    args = [a for a in argv if a != "--json"]
    if len(args) != 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    try:
        original, rewrite = (open(p, encoding="utf-8").read() for p in args)
    except OSError as e:
        print(f"cannot read {e.filename}", file=sys.stderr)
        return 2
    result = compare(original, rewrite)
    if as_json:
        print(json.dumps(result, indent=2))
    elif result["ok"]:
        print("facts kept: no figure, link, path, code or quote dropped, changed or added")
    else:
        for label, group in (("missing", result["missing"]), ("added", result["added"])):
            for kind, items in group.items():
                print(f"{label} {kind}: {', '.join(items)}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main(sys.argv[1:]))
