#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Fast, deterministic AI-tell scanner for the plain-language skill.

Two jobs:
  1. Pre-scan a text and report a tell count + density, so the skill can
     short-circuit already-clean prose instead of paying for a rewrite.
  2. Diff two drafts and report new-tell count + an edit-distance ratio,
     giving the loop a cheap, non-model stop signal (never loop unbounded).

Prose only: code fences, inline code, YAML frontmatter, and blockquoted
source text are stripped before scanning, so the scanner never flags a tell
inside a region the skill is forbidden to edit.

Usage:
  scan_tells.py --file PATH
  scan_tells.py --stdin                 (pipe text on stdin)
  scan_tells.py --diff OLD_PATH NEW_PATH
  add --json for machine-readable output

Exit codes: 0 = clean (below threshold), 1 = tells found (at/above threshold),
2 = usage error. With --diff: 0 = converged, 1 = not converged.
"""
from __future__ import annotations

import argparse
import json
import re
import sys

# Density (tells per 100 words) at or above which text is "not clean".
DEFAULT_THRESHOLD = 1.0
# --diff convergence: stop when new tells == 0 AND change ratio below this.
CONVERGENCE_CHANGE_RATIO = 0.05

# Each pattern is (label, compiled regex). Patterns are deliberately narrow to
# limit false positives; this is a signal, not a verdict.
_AI_VOCAB = (
    r"\b(?:delve[sd]?|tapestry|testament|underscore[sd]?|pivotal|crucial|"
    r"robust|vibrant|boasts?|nestled|groundbreaking|renowned|"
    r"meticulous|seamless|bustling)\b"
)
_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("ai-vocab", re.compile(_AI_VOCAB, re.I)),
    ("copula-avoidance", re.compile(r"\b(?:serves as|stands as)\b", re.I)),
    ("negative-parallelism", re.compile(r"\bnot (?:just|only|merely)\b", re.I)),
    ("authority-trope", re.compile(r"\b(?:the real question is|at its core|what really matters)\b", re.I)),
    ("vague-attribution", re.compile(r"\b(?:experts (?:argue|say|believe)|studies show|observers (?:note|have noted))\b", re.I)),
    ("signposting", re.compile(r"\b(?:let'?s dive in|without further ado|let'?s explore)\b", re.I)),
    ("hedging-frame", re.compile(r"\bit(?:'?s| is) (?:important|worth) (?:to note|noting|mentioning)\b", re.I)),
    ("sycophancy", re.compile(r"(?:great question!|you'?re absolutely right|certainly!)", re.I)),
    ("chatbot-artifact", re.compile(r"\b(?:i hope this helps|let me know if|would you like me to)\b", re.I)),
    ("empty-intensifier", re.compile(r"\b(?:very|really|quite|genuinely|actually)\b", re.I)),
    ("filler-phrase", re.compile(r"\b(?:in order to|due to the fact that|at this point in time|has the ability to)\b", re.I)),
    ("em-dash", re.compile(r"\s[—–]\s|\w[—–]\w")),
    ("curly-quote", re.compile(r"[‘’“”]")),
    ("emoji-bullet", re.compile(r"^\s*[\U0001F300-\U0001FAFF☀-➿]", re.M)),
    ("title-case-heading", re.compile(r"^#{1,6}\s+(?:[A-Z][a-z]+\s+){2,}[A-Z][a-z]+\s*$", re.M)),
    ("bold-header-list", re.compile(r"^\s*[-*]\s+\*\*[^*]+:\*\*", re.M)),
]


def strip_non_prose(text: str) -> str:
    """Remove regions the skill must not edit, so they can't register tells."""
    # YAML frontmatter (leading --- ... ---).
    text = re.sub(r"\A---\n.*?\n---\n", "", text, count=1, flags=re.S)
    # Fenced code blocks.
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"~~~.*?~~~", " ", text, flags=re.S)
    # Inline code.
    text = re.sub(r"`[^`]*`", " ", text)
    # Blockquoted source text (lines starting with >).
    text = re.sub(r"^\s*>.*$", " ", text, flags=re.M)
    # Bare URLs and markdown link targets.
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"\]\([^)]*\)", "] ", text)
    return text


def count_words(prose: str) -> int:
    return len(re.findall(r"\b\w+\b", prose))


def scan(text: str) -> dict:
    """Return tell hits, total, word count, and density (tells per 100 words)."""
    prose = strip_non_prose(text)
    hits: dict[str, int] = {}
    located: list[dict] = []
    for label, pat in _PATTERNS:
        matches = pat.findall(prose)
        if matches:
            hits[label] = len(matches)
            located.append({"tell": label, "count": len(matches)})
    total = sum(hits.values())
    words = count_words(prose)
    density = (total / words * 100) if words else 0.0
    return {
        "total_tells": total,
        "words": words,
        "density_per_100w": round(density, 2),
        "by_type": hits,
        "located": located,
    }


def _tell_multiset(text: str) -> dict[str, int]:
    return scan(text)["by_type"]


def change_ratio(old: str, new: str) -> float:
    """Cheap word-level edit-distance ratio in [0, 1]. 0 = identical."""
    a = re.findall(r"\b\w+\b", old.lower())
    b = re.findall(r"\b\w+\b", new.lower())
    if not a and not b:
        return 0.0
    import difflib

    ratio = difflib.SequenceMatcher(None, a, b).ratio()
    return round(1.0 - ratio, 4)


def diff(old: str, new: str) -> dict:
    """Report new tells introduced and the change ratio, for the stop signal."""
    old_tells = _tell_multiset(old)
    new_tells = _tell_multiset(new)
    introduced = {
        label: new_tells[label] - old_tells.get(label, 0)
        for label in new_tells
        if new_tells[label] > old_tells.get(label, 0)
    }
    new_total = sum(introduced.values())
    ratio = change_ratio(old, new)
    converged = new_total == 0 and ratio < CONVERGENCE_CHANGE_RATIO
    return {
        "new_tells": new_total,
        "new_by_type": introduced,
        "change_ratio": ratio,
        "converged": converged,
    }


def _read(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Deterministic AI-tell scanner.")
    src = parser.add_mutually_exclusive_group()
    src.add_argument("--file", help="path to a text/markdown file")
    src.add_argument("--stdin", action="store_true", help="read text from stdin")
    parser.add_argument("--diff", nargs=2, metavar=("OLD", "NEW"),
                        help="compare two drafts for the convergence stop signal")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                        help="density (tells/100w) at/above which text is not clean")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args(argv)

    if args.diff:
        old, new = _read(args.diff[0]), _read(args.diff[1])
        result = diff(old, new)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"new tells introduced: {result['new_tells']}")
            print(f"change ratio: {result['change_ratio']}")
            print(f"converged: {result['converged']}")
        return 0 if result["converged"] else 1

    if args.file:
        text = _read(args.file)
    elif args.stdin:
        text = sys.stdin.read()
    else:
        parser.error("one of --file, --stdin, or --diff is required")
        return 2

    result = scan(text)
    clean = result["density_per_100w"] < args.threshold
    result["clean"] = clean
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"tells: {result['total_tells']}  words: {result['words']}  "
              f"density: {result['density_per_100w']}/100w  "
              f"{'CLEAN' if clean else 'NOT CLEAN'}")
        for item in result["located"]:
            print(f"  {item['tell']}: {item['count']}")
    return 0 if clean else 1


if __name__ == "__main__":
    sys.exit(main())
