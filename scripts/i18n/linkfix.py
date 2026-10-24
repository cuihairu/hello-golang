#!/usr/bin/env python3
"""Rewrite internal links in the English (root-locale) pages.

Run once per translation batch, after the new pages have been written:

    python3 scripts/i18n/linkfix.py             # rewrite, then report
    python3 scripts/i18n/linkfix.py --check     # report only, no writes

The English pages are translated straight from docs/zh/, so their links still
point at the Chinese locale. These rules settle them:

1. A target that resolves to an existing English page points at the English
   page. This also lifts targets that were parked at /zh while the English
   page was still missing, so the pass is idempotent and self-healing.
2. A target with no English page yet falls back to its /zh page, so a reader
   hits Chinese text instead of a 404 while translation catches up.
3. Link labels containing CJK on internal links become the page name taken
   from the file name; file names are already English.

docs/zh/ is never touched, and neither is SUMMARY.md (excluded from the build).
"""
import argparse
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DOCS = REPO / "docs"
ZH = DOCS / "zh"

CJK = re.compile(r"[一-鿿]")
FENCE = re.compile(r"^\s*(```+|~~~+)")
PAREN = re.compile(r"(?<!!)\[([^\]\n]*)\]\(([^)\n]*)\)")
SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


def inline_spans(line: str):
    """Split a line into (text, is_code) pairs, tracking backtick runs."""
    spans = []
    i = 0
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


def page_name(rel: str) -> str:
    """'start/BuildConstraint.md' -> 'Build Constraint'."""
    base = Path(rel).name
    if base.lower().endswith(".md"):
        base = base[:-3]
    base = re.sub(r"[_-]+", " ", base)
    base = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", base)
    return base[:1].upper() + base[1:] if base else base


def split_target(inner: str):
    """(target, rest) from the parenthesised part, keeping any link title."""
    target = inner.strip()
    if not target:
        return "", ""
    if target[0] in "\"'":
        quote = target[0]
        end = target.find(quote, 1)
        if end == -1:
            return target, ""
        return target[1:end], target[end + 1:]
    if " " in target:
        cut = target.index(" ")
        return target[:cut], target[cut:]
    return target, ""


def locate(target: str, page: Path):
    """('en'|'zh'|None, docs-relative path without .md) for a page target."""
    core = target.split("#", 1)[0].split("?", 1)[0]
    if not core:
        return None, None, core
    base = DOCS if core.startswith("/") else page.parent
    # an absolute markdown path must be joined as a relative one
    rel_target = core.lstrip("/")
    try:
        full = (base / rel_target).resolve()
        rel = full.relative_to(REPO).as_posix()
    except ValueError:
        return None, None, core
    if rel.startswith("docs/zh/"):
        rel = rel[len("docs/zh/"):]
        locale = "zh"
    elif rel.startswith("docs/"):
        rel = rel[len("docs/"):]
        locale = "en"
    else:
        return None, None, core
    if rel.lower().endswith(".md"):
        rel = rel[:-3]
    en = (DOCS / rel).with_suffix(".md")
    zh = (ZH / rel).with_suffix(".md")
    if en.exists():
        return "en", rel, core
    if zh.exists():
        return "zh", rel, core
    return None, None, core


def rewrite_line(line: str, page: Path, problems: list) -> str:
    """Rewrite one markdown line; code spans are skipped, fences handled by caller."""
    out = []
    for text, is_code in inline_spans(line):
        if is_code:
            out.append(text)
            continue
        start = 0
        for m in PAREN.finditer(text):
            label, inner = m.group(1), m.group(2)
            target, rest = split_target(inner)
            if not target:
                continue
            if SCHEME.match(target) or target.startswith("//") or target.startswith("#"):
                continue
            locale, rel, core = locate(target, page)
            if locale is None and rel is None and not core.startswith(("/", "./", "../")) and "/" not in core:
                continue  # plain word, not a page reference
            if locale is None:
                problems.append(f"{page.relative_to(REPO)}: no page behind {target}")
                continue
            ext = ".md" if core.lower().endswith(".md") else ""
            frag = target[len(core):]
            new_target = ("/zh/" + rel) if locale == "zh" else ("/" + rel)
            new_label = page_name(core) if CJK.search(label) else label
            out.append(text[start:m.start()])
            out.append(f"[{new_label}]({new_target}{ext}{frag}{rest})")
            start = m.end()
        out.append(text[start:])
    return "".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="report only, no writes")
    args = ap.parse_args()

    pages = [
        p for p in sorted(DOCS.rglob("*.md"))
        if ZH not in p.parents and p != DOCS / "SUMMARY.md" and ".vitepress" not in p.parts
    ]
    problems: list[str] = []
    changed: list[str] = []
    cjk_lines: list[str] = []
    for page in pages:
        src = page.read_text(encoding="utf-8")
        lines = src.split("\n")
        in_fence = False
        new_lines = []
        for line in lines:
            if FENCE.match(line):
                in_fence = not in_fence
                new_lines.append(line)
                continue
            if in_fence:
                new_lines.append(line)
            else:
                new_lines.append(rewrite_line(line, page, problems))
            if CJK.search(line) and "docs/zh/" not in line:
                cjk_lines.append(f"{page.relative_to(REPO)}:{line.strip()[:60]}")
        new = "\n".join(new_lines)
        if new != src:
            changed.append(str(page.relative_to(REPO)))
            if not args.check:
                page.write_text(new, encoding="utf-8")

    for line in problems:
        print(f"DEAD  {line}")
    for line in cjk_lines:
        print(f"CJK   {line}")
    print(f"\n{len(pages)} pages scanned, {len(changed)} rewritten, "
          f"{len(problems)} dead targets, {len(cjk_lines)} CJK lines")
    return 1 if (problems or cjk_lines) and not args.check else 0


if __name__ == "__main__":
    raise SystemExit(main())
