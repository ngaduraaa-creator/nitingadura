#!/usr/bin/env python3
"""Regression gate: a page may only say a message was sent if it really sends it.

Scans every .html file in the site tree (stdlib only, no network) and fails
(exit 1) when a page:

  F1  has a <form> with no real submission path: no absolute http(s) action on
      another host, and no handler bound to the form that makes a request
      (fetch / XMLHttpRequest / sendBeacon / .submit()).
  F2  has a <form> that collects personal fields (name, phone, email, address)
      but would send them by GET (method missing or "get"), which puts the
      visitor's details in a URL.
  F3  has a click or submit handler that reveals an element whose text reads
      as a confirmation ("Message Received", "will be in touch", ...), or
      writes such text, without making any request.
  F4  carries confirmation copy in an element hidden on load, or in a JS
      string, while the page has no real submission path at all.
  F5  has personal-data inputs outside any <form> that no request-making
      script reads (a dead lead block).
  F6  is a page that used to fake a confirmation (REQUIRED_CONTACT_PAGES) but
      lacks the honest contact block ([data-contact-fallback] with a tel: and
      a mailto: link), or any contact block carries a response-time promise,
      confirmation copy, or a phone/email target that differs from the others.

Exit codes: 0 pass, 1 findings, 2 usage or setup error (fails closed).
Usage: python3 scripts/test_no_false_confirmation.py [SITE_ROOT]
"""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

SITE_HOSTS = {"nitingadura.com", "www.nitingadura.com"}

# Pages that showed a fake confirmation before the repair. Each must keep a
# working, honest way to reach a person.
REQUIRED_CONTACT_PAGES = (
    "index.html", "queens.html", "brooklyn.html", "long-island.html",
    "long-island/elmont.html", "long-island/garden-city.html",
    "long-island/great-neck.html", "long-island/hempstead.html",
    "long-island/levittown.html", "long-island/valley-stream.html",
    "queens/astoria.html", "queens/bayside.html", "queens/flushing.html",
    "queens/forest-hills.html", "queens/howard-beach.html",
    "queens/jackson-heights.html", "queens/jamaica.html",
    "queens/ozone-park.html", "queens/richmond-hill.html",
    "queens/woodside.html",
    "resources/best-neighborhoods-queens-south-asian-families.html",
    "resources/buy-a-home-queens.html",
    "resources/first-time-home-buyer-queens.html",
    "resources/home-valuation-queens.html",
    "resources/sell-your-home-queens.html",
)

NET = re.compile(r"\bfetch\s*\(|XMLHttpRequest|sendBeacon|\.submit\s*\(\s*\)|\$\.(?:ajax|post|get)\s*\(|axios\.")

CONFIRM = re.compile(
    r"""\bmessage\s+(?:sent|received)\b
      | \b(?:request|inquiry|enquiry|submission|application|details)\s+(?:has\s+been\s+|was\s+|were\s+)?(?:sent|received|submitted)\b
      | \b(?:thank\s*you|thanks)\b[^<.!?]{0,60}?\b(?:submi|request|message|inquir|enquir|reaching\s+out|contacting|getting\s+in\s+touch)
      | \b(?:we|i|nitin|nitin\s+gadura|he|she|our\s+team|an?\s+agent)(?:'ll|’ll|\s+will)\s+(?:personally\s+)?(?:be\s+in\s+touch|reach\s+out|get\s+back\s+to\s+you|contact\s+you|call\s+you|follow\s+up)\b
      | \bsuccessfully\s+(?:sent|submitted|received)\b
      | \byou(?:'re|’re|\s+are)\s+all\s+set\b
    """,
    re.I | re.X,
)

RESPONSE_PROMISE = re.compile(
    r"within\s+(?:\d+|one|two|a\s+few|an?)\s*(?:-\s*\d+\s*)?(?:hours?|hrs?|minutes?|mins?|business\s+days?|days?)"
    r"|same[- ]day\s+(?:response|reply|callback)|\b\d+[- ]hour\s+(?:response|reply|turnaround|delivery)"
    r"|respond(?:s)?\s+(?:fast|quickly|immediately|right\s+away|promptly)",
    re.I,
)

PERSONAL_FIELD = re.compile(r"name|phone|tel|email|e-mail|address|telefono|correo", re.I)
PERSONAL_TYPES = {"tel", "email"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
JS_TYPES = {"", "text/javascript", "application/javascript", "module"}
REVEAL_CLASSES = r"show|shown|active|visible|is-visible|open|success|done|sent"


class Node:
    __slots__ = ("tag", "attrs", "parent", "children", "text", "content", "line")

    def __init__(self, tag: str, attrs: dict, parent: "Node | None", line: int):
        self.tag, self.attrs, self.parent, self.line = tag, attrs, parent, line
        self.children: list[Node] = []
        self.text: list[str] = []
        self.content: list = []  # text and child nodes in document order

    def ancestors(self):
        node = self.parent
        while node is not None:
            yield node
            node = node.parent

    def descendants(self):
        for child in self.children:
            yield child
            yield from child.descendants()

    def full_text(self) -> str:
        parts = []
        for item in self.content:
            if isinstance(item, str):
                parts.append(item)
            elif item.tag not in ("script", "style"):
                parts.append(item.full_text())
        return re.sub(r"\s+", " ", " ".join(parts)).strip()


class DomBuilder(HTMLParser):
    """Small tolerant DOM: enough to find forms, inputs, ids, scripts and styles."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", {}, None, 0)
        self.stack = [self.root]

    def _add(self, tag, attrs) -> Node:
        node = Node(tag, {k: (v or "") for k, v in attrs}, self.stack[-1], self.getpos()[0])
        self.stack[-1].children.append(node)
        self.stack[-1].content.append(node)
        return node

    def handle_starttag(self, tag, attrs):
        node = self._add(tag, attrs)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self._add(tag, attrs)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        top = self.stack[-1]
        top.text.append(data)
        top.content.append(data)


class Page:
    def __init__(self, rel: str, html: str):
        self.rel, self.html = rel, html
        builder = DomBuilder()
        builder.feed(html)
        builder.close()
        self.root = builder.root
        self.nodes = list(self.root.descendants())
        self.by_id = {}
        for node in self.nodes:
            self.by_id.setdefault(node.attrs.get("id", ""), node)
        self.js = "\n".join("".join(n.text) for n in self.nodes if n.tag == "script"
                            and n.attrs.get("type", "").strip().lower() in JS_TYPES and "src" not in n.attrs)
        self.hidden_classes = hidden_classes("\n".join("".join(n.text) for n in self.nodes if n.tag == "style"))
        self.var_to_id = dict(re.findall(
            r"(?:const|let|var)\s+(\w+)\s*=\s*document\.getElementById\(\s*['\"]([^'\"]+)['\"]\s*\)", self.js))
        for var, sel in re.findall(
                r"(?:const|let|var)\s+(\w+)\s*=\s*document\.querySelector\(\s*['\"]#([\w-]+)['\"]\s*\)", self.js):
            self.var_to_id.setdefault(var, sel)
        self.functions = dict(
            (m.group(1), self.js[m.start():match_close(self.js, self.js.index("{", m.end() - 1), "{", "}")])
            for m in re.finditer(r"function\s+(\w+)\s*\([^)]*\)\s*\{", self.js))


def hidden_classes(css: str) -> set[str]:
    found = set()
    for selectors, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        if re.search(r"display\s*:\s*none", body):
            for sel in selectors.split(","):
                last = sel.strip().split()[-1] if sel.strip() else ""
                found.update(re.findall(r"\.([\w-]+)", last.split(":")[0]))
    return found


def match_close(text: str, start: int, open_ch: str, close_ch: str) -> int:
    """Index after the bracket that closes text[start]; skips JS strings and comments."""
    depth, quote, i = 0, None, start
    while i < len(text):
        ch = text[i]
        if quote:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                quote = None
        elif text.startswith("//", i):
            nl = text.find("\n", i)
            i = len(text) if nl < 0 else nl
            continue
        elif text.startswith("/*", i):
            end = text.find("*/", i + 2)
            i = len(text) if end < 0 else end + 2
            continue
        elif ch in "'\"`":
            quote = ch
        elif ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return len(text)


def hidden_itself(page: Page, el: Node) -> bool:
    style = el.attrs.get("style", "").replace(" ", "").lower()
    if "display:none" in style or "hidden" in el.attrs:
        return True
    return bool(set(el.attrs.get("class", "").split()) & page.hidden_classes)


def is_hidden_on_load(page: Page, node: Node) -> bool:
    return any(hidden_itself(page, el) for el in [node, *node.ancestors()])


def shown_text(page: Page, node: Node) -> str:
    """Text a reveal of `node` would show: skips descendants that stay hidden."""
    parts = []
    for item in node.content:
        if isinstance(item, str):
            parts.append(item)
        elif item.tag not in ("script", "style") and not hidden_itself(page, item):
            parts.append(shown_text(page, item))
    return re.sub(r"\s+", " ", " ".join(parts)).strip()


def file_line(page: Page, snippet: str) -> int:
    pos = page.html.find(snippet[:120])
    return page.html.count("\n", 0, pos) + 1 if pos >= 0 else 0


def real_action(form: Node) -> bool:
    action = form.attrs.get("action", "").strip()
    parsed = urlparse(action)
    return parsed.scheme in ("http", "https") and parsed.netloc.lower() not in SITE_HOSTS


def personal_inputs(nodes) -> list[Node]:
    out = []
    for node in nodes:
        if node.tag not in ("input", "textarea", "select"):
            continue
        kind = node.attrs.get("type", "text").lower()
        if kind in ("hidden", "submit", "button", "checkbox", "radio", "range", "number"):
            continue
        label = " ".join(node.attrs.get(k, "") for k in ("name", "id", "autocomplete"))
        if kind in PERSONAL_TYPES or PERSONAL_FIELD.search(label):
            out.append(node)
    return out


def handlers(page: Page):
    """Yield (line, kind, target_expr, body) for every click/submit handler."""
    js = page.js
    for m in re.finditer(r"([\w$.]+(?:\([^()]*\))?)\s*\.addEventListener\(\s*['\"](click|submit)['\"]", js):
        paren = js.index("(", js.index("addEventListener", m.start()))
        body = js[m.start():match_close(js, paren, "(", ")")]
        yield file_line(page, body), m.group(2), m.group(1), body
    for m in re.finditer(r"([\w$.]+(?:\([^()]*\))?)\s*\.on(click|submit)\s*=\s*(?:function\s*\([^)]*\)|\([^)]*\)\s*=>)\s*\{", js):
        body = js[m.start():match_close(js, m.end() - 1, "{", "}")]
        yield file_line(page, body), m.group(2), m.group(1), body
    for node in page.nodes:
        for kind in ("click", "submit"):
            attr = node.attrs.get("on" + kind)
            if attr:
                yield node.line, "attr-" + kind, node.attrs.get("id", node.tag), attr


def expand_calls(page: Page, body: str, depth: int = 3) -> str:
    seen, text = set(), body
    for _ in range(depth):
        called = set(re.findall(r"\b(\w+)\s*\(", text)) & set(page.functions) - seen
        if not called:
            break
        seen |= called
        text += "\n".join(page.functions[name] for name in called)
    return text


def revealed_ids(page: Page, body: str) -> set[str]:
    ids: set[str] = set()
    ref = r"(?:document\.getElementById\(\s*['\"]([\w-]+)['\"]\s*\)|document\.querySelector\(\s*['\"]#([\w-]+)['\"]\s*\)|(\w+))"
    patterns = (
        ref + r"\.style\.display\s*=\s*['\"](?:block|flex|grid|inline|inline-block|inline-flex|)['\"]",
        ref + r"\.classList\.(?:add|toggle)\(\s*['\"](?:" + REVEAL_CLASSES + r")['\"]",
        ref + r"\.hidden\s*=\s*false",
        ref + r"\.removeAttribute\(\s*['\"]hidden['\"]",
    )
    for pat in patterns:
        for by_id, by_sel, var in re.findall(pat, body):
            ids.add(by_id or by_sel or page.var_to_id.get(var, var))
    return ids


def form_target_ids(page: Page, target: str) -> set[str]:
    ids = set(re.findall(r"getElementById\(\s*['\"]([\w-]+)['\"]", target))
    ids |= set(re.findall(r"querySelector\(\s*['\"]#([\w-]+)['\"]", target))
    if target in page.var_to_id:
        ids.add(page.var_to_id[target])
    return ids


def check_forms(page: Page, findings: list):
    submit_bodies: dict[str, list[str]] = {}
    for _, kind, target, body in handlers(page):
        if kind.endswith("submit"):
            for fid in form_target_ids(page, target) or {target}:
                submit_bodies.setdefault(fid, []).append(expand_calls(page, body))
    for form in (n for n in page.nodes if n.tag == "form"):
        fid = form.attrs.get("id", "")
        js_sends = any(NET.search(b) for b in submit_bodies.get(fid, []))
        js_sends = js_sends or bool(NET.search(form.attrs.get("onsubmit", "")))
        if not (real_action(form) or js_sends):
            findings.append(("F1", page.rel, form.line, f"form#{fid or '?'} has no real submission path"))
        method = form.attrs.get("method", "get").strip().lower()
        if not js_sends and method != "post" and personal_inputs(form.descendants()):
            findings.append(("F2", page.rel, form.line, f"form#{fid or '?'} would send personal fields by GET"))


def check_handlers(page: Page, findings: list):
    for line, kind, target, body in handlers(page):
        full = expand_calls(page, body)
        if NET.search(full):
            continue
        shown = [i for i in revealed_ids(page, full)
                 if i in page.by_id and CONFIRM.search(shown_text(page, page.by_id[i]))]
        written = [s for s in re.findall(r"(['\"`])((?:(?!\1).)*)\1", full) if CONFIRM.search(s[1])]
        if shown or written:
            what = f"reveals #{', #'.join(sorted(shown))}" if shown else "writes confirmation text"
            findings.append(("F3", page.rel, line, f"{kind} handler on {target} {what} without sending anything"))


def page_sends(page: Page) -> bool:
    forms_send = any(real_action(n) for n in page.nodes if n.tag == "form")
    return forms_send or bool(NET.search(page.js))


def check_static_copy(page: Page, findings: list):
    if page_sends(page):
        return
    for node in page.nodes:
        if node.tag in ("script", "style") or not node.text:
            continue
        own = re.sub(r"\s+", " ", " ".join(node.text))
        if CONFIRM.search(own) and is_hidden_on_load(page, node):
            findings.append(("F4", page.rel, node.line, f"hidden confirmation copy: {own.strip()[:70]!r}"))
    for quote, text in re.findall(r"(['\"`])((?:(?!\1).){4,300}?)\1", page.js):
        if CONFIRM.search(text):
            findings.append(("F4", page.rel, file_line(page, text), f"confirmation copy in script: {text[:70]!r}"))


def check_dead_fields(page: Page, findings: list):
    loose = [n for n in personal_inputs(page.nodes) if not any(a.tag == "form" for a in n.ancestors())]
    if loose and not NET.search(page.js):
        ids = ", ".join(n.attrs.get("id") or n.attrs.get("name") or n.tag for n in loose[:6])
        findings.append(("F5", page.rel, loose[0].line, f"personal-data fields outside any form, nothing sends them: {ids}"))


def check_contact_blocks(page: Page, findings: list, targets: dict):
    blocks = [n for n in page.nodes if "data-contact-fallback" in n.attrs]
    if page.rel in REQUIRED_CONTACT_PAGES and not blocks:
        findings.append(("F6", page.rel, 0, "missing honest contact block [data-contact-fallback]"))
    for block in blocks:
        hrefs = [n.attrs.get("href", "") for n in block.descendants() if n.tag == "a"]
        tel = sorted({h for h in hrefs if h.startswith("tel:")})
        mail = sorted({h.split("?")[0] for h in hrefs if h.startswith("mailto:")})
        text = block.full_text() + " " + " ".join(n.attrs.get("aria-label", "") for n in block.descendants())
        if not tel or not mail:
            findings.append(("F6", page.rel, block.line, "contact block lacks a tel: or mailto: link"))
        if RESPONSE_PROMISE.search(text) or CONFIRM.search(text):
            findings.append(("F6", page.rel, block.line, "contact block carries a response-time promise or confirmation copy"))
        for href in tel + mail:
            targets.setdefault(href.split(":")[0], {}).setdefault(href, []).append(page.rel)


def scan(root: Path) -> list:
    findings: list = []
    targets: dict = {}
    for path in sorted(root.rglob("*.html")):
        rel = path.relative_to(root).as_posix()
        if rel.startswith((".git/", "node_modules/")):
            continue
        page = Page(rel, path.read_text(encoding="utf-8", errors="replace"))
        check_forms(page, findings)
        check_handlers(page, findings)
        check_static_copy(page, findings)
        check_dead_fields(page, findings)
        check_contact_blocks(page, findings, targets)
    for scheme, by_href in targets.items():
        if len(by_href) > 1:
            detail = "; ".join(f"{h} on {len(p)} page(s)" for h, p in sorted(by_href.items()))
            findings.append(("F6", "(site)", 0, f"contact blocks disagree on the {scheme} target: {detail}"))
    return findings


def main(argv: list[str]) -> int:
    root = Path(argv[1] if len(argv) > 1 else Path(__file__).resolve().parent.parent)
    if not (root / "index.html").is_file() or not (root / "CNAME").is_file():
        print(f"SETUP ERROR: {root} does not look like the site root (index.html and CNAME required)")
        return 2
    missing = [p for p in REQUIRED_CONTACT_PAGES if not (root / p).is_file()]
    if missing:
        print("SETUP ERROR: required pages missing: " + ", ".join(missing))
        return 2
    findings = scan(root)
    for rule, rel, line, msg in findings:
        print(f"FAIL {rule} {rel}:{line} {msg}")
    counts = {r: sum(1 for f in findings if f[0] == r) for r in ("F1", "F2", "F3", "F4", "F5", "F6")}
    pages = len({f[1] for f in findings})
    print("SUMMARY " + " ".join(f"{k}={v}" for k, v in counts.items()) + f" pages={pages}")
    print("RESULT " + ("FAIL" if findings else "PASS"))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
