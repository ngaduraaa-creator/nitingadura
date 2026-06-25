#!/usr/bin/env python3
"""
add_sell_hreflang.py
Adds reciprocal hreflang annotations to the "Sell your home" page and its 5
language variants so Google serves the right language to each searcher and does
not treat them as duplicate/competing content.

Cluster: en (/sell/) · hi · bn · es · pa · ur · x-default (=en)
Every page in the set gets the SAME complete block (hreflang must be reciprocal
and include a self-reference). Idempotent: skips a page that already has it.

Run from repo root:
  python3 scripts/add_sell_hreflang.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://nitingadura.com/'

# file → its absolute URL
CLUSTER = [
    ('en',        'sell/index.html', BASE + 'sell/'),
    ('hi',        'sell-hi.html',    BASE + 'sell-hi.html'),
    ('bn',        'sell-bn.html',    BASE + 'sell-bn.html'),
    ('es',        'sell-es.html',    BASE + 'sell-es.html'),
    ('pa',        'sell-pa.html',    BASE + 'sell-pa.html'),
    ('ur',        'sell-ur.html',    BASE + 'sell-ur.html'),
]
X_DEFAULT = BASE + 'sell/'

MARK_START = '<!-- hreflang-sell:start -->'
MARK_END = '<!-- hreflang-sell:end -->'


def block() -> str:
    lines = [MARK_START]
    for lang, _f, url in CLUSTER:
        lines.append(f'<link rel="alternate" hreflang="{lang}" href="{url}">')
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{X_DEFAULT}">')
    lines.append(MARK_END)
    return '\n'.join('  ' + ln for ln in lines)


def main():
    blk = block()
    updated = skipped = 0
    for _lang, rel, _url in CLUSTER:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            print(f'  MISSING: {rel}')
            continue
        with open(path, encoding='utf-8') as fh:
            html = fh.read()
        if MARK_START in html:
            print(f'  SKIP (already present): {rel}')
            skipped += 1
            continue
        # insert right after the canonical link; fall back to before </head>
        m = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]*>', html)
        if m:
            i = m.end()
            new = html[:i] + '\n' + blk + html[i:]
        else:
            new = html.replace('</head>', blk + '\n</head>', 1)
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(new)
        print(f'  OK: {rel}')
        updated += 1
    print(f'\nDone. Updated: {updated}  Skipped: {skipped}')


if __name__ == '__main__':
    main()
