#!/usr/bin/env python3
"""
inject_ai_schema.py — Inject the Nitin-centric AI master schema across all pages.

Idempotent. Replaces any existing block with id="ai-master-schema" (and the
include's header comment in front of it, so re-runs do not stack comments).
Does NOT touch existing JSON-LD blocks (they may have unique BreadcrumbList,
ItemList, Product, etc. — those are kept).

By default only pages that already carry the block are updated. Pages without
it are changed only with --insert-missing, and even then a page is skipped when
its own JSON-LD already uses an @id that the master graph defines, because
scripts/validate_schema.py allows each @id once per page.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_FILE = ROOT / "_includes" / "ai-master-schema.html"
MARKER_ID = "ai-master-schema"

GLOBS = [
    "*.html",
    "**/*.html",
]
SKIP_PARTS = {"_includes", "scripts", ".git", ".github", "_site"}
SKIP_FILES = {"404.html"}

SCRIPT_RE = re.compile(
    rf'(?:<!--\s*AI MASTER SCHEMA\b.*?-->\s*)*'
    rf'<script type="application/ld\+json" id="{MARKER_ID}">.*?</script>\s*',
    re.DOTALL | re.IGNORECASE,
)
LD_RE = re.compile(
    r'<script type="application/ld\+json"[^>]*>(.*?)</script>',
    re.DOTALL | re.IGNORECASE,
)


def ids_in(text):
    """Every @id value used in the JSON-LD blocks of an HTML string."""
    found = set()

    def walk(node):
        if isinstance(node, dict):
            if isinstance(node.get("@id"), str):
                found.add(node["@id"])
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    for raw in LD_RE.findall(text):
        raw = raw.strip()
        if raw:
            walk(json.loads(raw))
    return found


def collect():
    seen = set()
    out = []
    for pat in GLOBS:
        for p in ROOT.glob(pat):
            if not p.is_file() or p.suffix != ".html":
                continue
            if p.name in SKIP_FILES:
                continue
            if any(part in SKIP_PARTS for part in p.relative_to(ROOT).parts):
                continue
            if p in seen:
                continue
            seen.add(p)
            out.append(p)
    return out


def inject(html, block, insert_missing=False, master_ids=frozenset()):
    if MARKER_ID in html:
        new, n = SCRIPT_RE.subn(lambda _m: block + "\n", html, count=1)
        if n:
            return new, "replaced"
        return html, "noop"
    if not insert_missing:
        return html, "skipped (no block; see --insert-missing)"
    if "</head>" not in html:
        return html, "noop"
    if ids_in(html) & master_ids:
        return html, "skipped (@id already used on page)"
    return html.replace("</head>", f"{block}\n</head>", 1), "inserted"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--insert-missing", action="store_true",
                    help="also add the block to pages that do not carry it yet")
    args = ap.parse_args()
    block = SCHEMA_FILE.read_text(encoding="utf-8").rstrip()
    master_ids = frozenset(ids_in(block))
    pages = collect()
    print(f"Targets: {len(pages)}")
    counts = {"inserted": 0, "replaced": 0, "noop": 0}
    for p in pages:
        try:
            html = p.read_text(encoding="utf-8")
        except Exception:
            continue
        new_html, action = inject(html, block, args.insert_missing, master_ids)
        counts[action] = counts.get(action, 0) + 1
        if args.apply and new_html != html:
            p.write_text(new_html, encoding="utf-8")
    for k, v in counts.items():
        print(f"  {k}: {v}")
    print(f"\nMode: {'APPLIED' if args.apply else 'DRY-RUN'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
