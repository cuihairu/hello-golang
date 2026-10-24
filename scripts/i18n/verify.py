#!/usr/bin/env python3
"""Batch gate for the English translations: compare every EN page with its zh twin.

    python3 scripts/i18n/verify.py            # report all mismatches
    python3 scripts/i18n/verify.py --list     # list pages that still need translating

The checks are the ones that catch a sloppy translation:

  HEAD   heading count differs from the zh source
  LINES  total line count differs
  FENCE  code-fence count differs (a block was dropped or altered)
  LINK   markdown link count differs (a reference was dropped or invented)
  CJK    CJK text left in English prose. Code blocks, inline code and
         docs/zh path mentions are allowed: code stays byte-identical to the
         source, and some pages are literally about Chinese characters in Go.
  H1     page has no heading at all (the frontmatter home page is exempt)

Exit status is 1 when any check fails.
"""
import argparse
import re
from pathlib import Path

DOCS = Path(__file__).resolve().parents[2] / "docs"
ZH = DOCS / "zh"

CJK = re.compile(r"[一-鿿]")
FENCE = re.compile(r"^\s*(```+|~~~+)")
HEADING = re.compile(r"^\s{0,3}#{1,6}\s")
LINK = re.compile(r"(?<!!)\[([^\]\n]*)\]\(([^)\n]*)\)")


def spans(line: str):
    """(text, is_code) pairs, tracking backtick runs (same logic as linkfix)."""
    spans, i = [], 0
    while i < len(line):
        if line[i] != "`":
            j = line.find("`", i)
            spans.append((line[i:] if j == -1 else line[i:j], False))
            if j == -1:
                return spans
            i = j
            continue
        run = 1
        while i + run < len(line) and line[i + run] == "`":
            run += 1
        closed = -1
        j = i + run
        while j < len(line):
            if line[j] == "`":
                k = j
                while k < len(line) and line[k] == "`":
                    k += 1
                if k - j == run:
                    closed = k
                    break
            j += 1
        if closed == -1:
            spans.append((line[i:], True))
            return spans
        spans.append((line[i:closed], True))
        i = closed
    return spans


def stats(page: Path):
    lines = page.read_text(encoding="utf-8").rstrip("\n").split("\n")
    headings = fences = links = 0
    cjk = []
    in_fence = False
    for n, line in enumerate(lines, 1):
        if FENCE.match(line):
            fences += 1
            in_fence = not in_fence
            continue
        if HEADING.match(line):
            headings += 1
        for text, is_code in spans(line):
            if is_code or in_fence:
                continue
            links += len(LINK.findall(text))
            if CJK.search(text) and "docs/zh/" not in text:
                cjk.append((n, text.strip()[:70]))
    return {"lines": len(lines), "headings": headings, "fences": fences,
            "links": links, "cjk": cjk}


def is_home(page: Path) -> bool:
    """The VitePress home page is a frontmatter page and has no H1 by design."""
    text = page.read_text(encoding="utf-8")
    return text.startswith("---") and "layout: home" in text.split("---")[1]


def pages():
    out = []
    for en in sorted(DOCS.rglob("*.md")):
        if ZH in en.parents or ".vitepress" in en.parts or en.name == "SUMMARY.md":
            continue
        zh = ZH / en.relative_to(DOCS)
        if zh.exists():
            out.append((en, zh))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--list", action="store_true",
                    help="list zh pages without an English twin")
    args = ap.parse_args()

    if args.list:
        missing = sorted(
            p.relative_to(ZH)
            for p in ZH.rglob("*.md")
            if not (DOCS / p.relative_to(ZH)).exists()
        )
        for rel in missing:
            print(rel)
        print(f"\n{len(missing)} of {sum(1 for _ in ZH.rglob('*.md'))} pages need translating")
        return 0

    fails = 0
    for en, zh in pages():
        rel = str(en.relative_to(DOCS))
        s_en, s_zh = stats(en), stats(zh)
        for key in ("headings", "fences", "links", "lines"):
            if s_en[key] != s_zh[key]:
                name = {"headings": "HEAD", "fences": "FENCE",
                        "links": "LINK", "lines": "LINES"}[key]
                print(f"{name:5} {rel}: zh={s_zh[key]} en={s_en[key]}")
                fails += 1
        if not s_en["headings"] and not is_home(en):
            print(f"H1    {rel}: no heading at all")
            fails += 1
        for n, line in s_en["cjk"]:
            print(f"CJK   {rel}:{n}: {line}")
            fails += 1

    print(f"\n{len(pages())} pages checked, {fails} failures")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
