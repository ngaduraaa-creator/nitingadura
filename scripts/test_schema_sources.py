#!/usr/bin/env python3
"""
test_schema_sources.py — keep scripts/validate_schema.py at zero errors,
including after the local page generators run.

Checks:
  1. validate_schema.py on this tree prints "errors found:  0" (the string the
     weekly schema workflow looks for).
  2. _includes/ai-master-schema.html: every @id occurs once, and every Person
     node has an @id.
  3. On a temporary copy of the tree (never this tree), the local generators
     that write HTML are run, then validate_schema.py must still print
     "errors found:  0". inject_ai_schema.py runs in its default mode and with
     --insert-missing. build_sell_rent_pages.py skips pages that exist, so the
     copy's sell/ and rent/ pages (except index.html) are removed first and
     rebuilt from the template.
  4. inject_ai_schema.py --apply is idempotent: a second run changes nothing.

Usage:  python3 scripts/test_schema_sources.py [--skip-generators]
Exit:   0 pass, 1 findings, 2 setup error. Stdlib only; no network.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLEAN = "errors found:  0"
LD_RE = re.compile(
    r'<script type="application/ld\+json"[^>]*>(.*?)</script>',
    re.DOTALL | re.IGNORECASE,
)
# (script, args) — local generators that write HTML. Network scripts are excluded.
GENERATORS = [
    ("build_sell_rent_pages.py", ["--apply"]),
    ("build_busy_streets.py", []),
    ("build_howto_pages.py", []),
    ("inject_faqpage_schema.py", ["--apply"]),
    ("add_sell_hreflang.py", []),
    ("optimize_page_speed.py", ["--apply"]),
    ("freshen_pages.py", ["--apply"]),
    ("inject_ai_schema.py", ["--apply"]),
    ("inject_ai_schema.py", ["--apply", "--insert-missing"]),
]
TIMEOUT = 300


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True, timeout=TIMEOUT,
        env={"PYTHONDONTWRITEBYTECODE": "1", "PATH": "/usr/bin:/bin:/usr/local/bin"},
    )


def validate(tree: Path) -> tuple[bool, str]:
    proc = run([sys.executable, "scripts/validate_schema.py"], tree)
    summary = "\n".join(
        line for line in proc.stdout.splitlines() if "errors found" in line or "✗" in line
    )
    return CLEAN in proc.stdout, summary[:2000]


def check_master_include(tree: Path) -> list[str]:
    problems: list[str] = []
    path = tree / "_includes" / "ai-master-schema.html"
    blocks = LD_RE.findall(path.read_text(encoding="utf-8"))
    if len(blocks) != 1:
        return [f"{path.name}: expected 1 JSON-LD block, found {len(blocks)}"]
    seen: dict[str, int] = {}

    def walk(node):
        if isinstance(node, dict):
            aid = node.get("@id")
            if aid:
                seen[aid] = seen.get(aid, 0) + 1
            if node.get("@type") == "Person" and "@id" not in node:
                problems.append(f"{path.name}: Person node without @id")
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(json.loads(blocks[0]))
    problems += [f"{path.name}: @id used {n} times: {aid}" for aid, n in seen.items() if n > 1]
    return problems


def tree_digest(tree: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(tree.rglob("*.html")):
        h.update(p.relative_to(tree).as_posix().encode())
        h.update(p.read_bytes())
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-generators", action="store_true",
                    help="only run checks 1 and 2")
    args = ap.parse_args()
    if not (ROOT / "scripts" / "validate_schema.py").is_file():
        print("SETUP ERROR: scripts/validate_schema.py not found", file=sys.stderr)
        return 2
    failures: list[str] = []

    ok, summary = validate(ROOT)
    print(f"[1] validate_schema on this tree: {'PASS' if ok else 'FAIL'}")
    if not ok:
        failures.append("validate_schema on this tree:\n" + summary)

    problems = check_master_include(ROOT)
    print(f"[2] master include @id / Person checks: {'PASS' if not problems else 'FAIL'}")
    failures += problems

    if not args.skip_generators:
        with tempfile.TemporaryDirectory(prefix="ng-schema-") as tmp:
            copy = Path(tmp) / "site"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            removed = 0
            for sub in ("sell", "rent"):
                for page in (copy / sub).glob("*.html"):
                    if page.name != "index.html":
                        page.unlink()
                        removed += 1
            for script, extra in GENERATORS:
                proc = run([sys.executable, f"scripts/{script}", *extra], copy)
                if proc.returncode != 0:
                    failures.append(f"{script} {' '.join(extra)} exited {proc.returncode}: "
                                    f"{proc.stderr.strip()[-300:]}")
                    continue
                if script == "build_sell_rent_pages.py":
                    created = sum(int(n) for n in re.findall(r"_created: (\d+)", proc.stdout))
                    print(f"    build_sell_rent_pages.py rebuilt {created} of {removed} removed pages")
                    if removed == 0 or created != removed:
                        failures.append(f"sell/rent rebuild: {created} built, {removed} removed")
            ok, summary = validate(copy)
            print(f"[3] validate_schema after generators (temporary copy): {'PASS' if ok else 'FAIL'}")
            if not ok:
                failures.append("validate_schema after generators:\n" + summary)

            before = tree_digest(copy)
            proc = run([sys.executable, "scripts/inject_ai_schema.py", "--apply"], copy)
            same = proc.returncode == 0 and before == tree_digest(copy)
            print(f"[4] inject_ai_schema.py second run changes nothing: {'PASS' if same else 'FAIL'}")
            if not same:
                failures.append("inject_ai_schema.py --apply is not idempotent")

    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        print("RESULT FAIL")
        return 1
    print("RESULT PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
