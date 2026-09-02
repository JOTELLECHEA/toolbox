#!/usr/bin/env python3
"""
app — serves your toolbox as a searchable page on localhost.

Defaults to the repo app/ sits inside — so as long as it stays as a
subfolder of your toolbox clone, this works with zero setup on any machine:

    python3 server.py                          # from inside app/
    python3 app/server.py                      # from the repo root
    TOOLBOX_ROOT=~/somewhere/else python3 server.py   # override if needed
    TOOLBOX_PORT=9000 python3 server.py
    TOOLBOX_HOST=0.0.0.0 python3 server.py     # bind wider (e.g. inside Docker)
    python3 server.py --lint                    # check for entries that fail to parse

Re-parses your .md files on every request to /api/entries, so editing a
sheet and refreshing the page is enough — no restart needed.

Two entry formats live side by side:

    - `command here` — description here <!-- optional, search, tags -->

    ### snippet title here <!-- optional, search, tags -->
    ```python
    boilerplate code here
    ```

Tags support two prefixes: `tag:name` shows that word as a pill in the UI
(others stay search-only), and `image:file.svg` attaches a preview image,
resolved relative to the .md file's own directory.

Fully offline — the syntax highlighter and all fonts are self-hosted
alongside this file (highlight.min.js, latex.min.js, fonts/), no CDN calls.
"""
import argparse
import http.server
import json
import os
import re
import socketserver
import urllib.parse
from pathlib import Path

STATIC_DIR = Path(__file__).resolve().parent
DEFAULT_ROOT = STATIC_DIR.parent  # app/ is expected to live inside the toolbox repo
ROOT = Path(os.environ.get("TOOLBOX_ROOT", DEFAULT_ROOT)).expanduser()
PORT = int(os.environ.get("TOOLBOX_PORT", 8420))
# Defaults to loopback-only, since this is a personal local tool with no
# auth — binding wider would expose it to anyone else on the network.
# Docker needs 0.0.0.0 here (its port mapping forwards from a different
# network namespace, which 127.0.0.1 can't be reached from) — set via
# TOOLBOX_HOST in the Dockerfile, not by changing this default.
HOST = os.environ.get("TOOLBOX_HOST", "127.0.0.1")

# Preview images are served from anywhere under ROOT, so the /img/ route is
# the one place a URL can name an arbitrary file path. Everything it serves
# must be inside ROOT and must have one of these extensions — checked after
# resolving symlinks and `..`, not before.
IMAGE_TYPES = {
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".webp": "image/webp",
}

ENTRY_RE = re.compile(
    r"^- `(?P<cmd>[^`]+)`"
    r"(?:\s*[—-]\s*(?P<desc>.*?))?"
    r"(?:\s*<!--\s*(?P<tags>.*?)\s*-->)?$"
)
SNIPPET_TITLE_RE = re.compile(
    r"^###\s+(?P<title>.+?)"
    r"(?:\s*<!--\s*(?P<tags>.*?)\s*-->)?$"
)
FENCE_RE = re.compile(r"^```(?P<lang>\w*)\s*$")
HEADER_RE = re.compile(r"^(#{2,6})\s+(.*)$")
# A markdown table: a row of pipe-delimited cells, then a separator row of
# dashes. The separator is what distinguishes a real table from a line that
# merely happens to contain pipes.
TABLE_ROW_RE = re.compile(r"^\|.*\|$")
TABLE_SEP_RE = re.compile(r"^\|[\s:|-]*-[\s:|-]*\|$")


def table_cells(line):
    """Split a markdown table row into cell strings."""
    return [c.strip() for c in line.strip().strip("|").split("|")]


def sheets():
    if not ROOT.exists():
        return []
    # Skip app/'s own files (e.g. its README's format example) when it's
    # sitting inside the scanned root, so the tool never treats its own
    # documentation as a cheatsheet entry.
    return sorted(
        p for p in ROOT.rglob("*.md")
        if not p.resolve().is_relative_to(STATIC_DIR)
    )


def split_tags(raw):
    """Separate display tags, search-only tags, and an optional image.

    `tag:name` is shown as a pill in the UI and stays searchable.
    `image:file.svg` names a preview image and is dropped from the search
    text entirely — a filename isn't something you'd ever type as a query.
    Everything else is search-only. Returns (searchable, display, image).
    """
    parts = [t.strip() for t in (raw or "").split(",") if t.strip()]
    display, searchable, image = [], [], None
    for p in parts:
        low = p.lower()
        if low.startswith("tag:"):
            word = p[4:].strip()
            if word:
                display.append(word)
                searchable.append(word)
        elif low.startswith("image:"):
            name = p[6:].strip()
            if name:
                image = name
        else:
            searchable.append(p)
    return ", ".join(searchable), display, image


def image_url(md_path, name):
    """Build the /img/ URL for an image named relative to its .md file.

    Returns None if the result would land outside ROOT — the same guard the
    /img/ route applies, so a bad path never even reaches the client.
    """
    if not name:
        return None
    try:
        target = (md_path.parent / name).resolve()
        target.relative_to(ROOT.resolve())
    except (ValueError, OSError):
        return None
    if target.suffix.lower() not in IMAGE_TYPES:
        return None
    rel = target.relative_to(ROOT.resolve()).as_posix()
    return "/img/" + urllib.parse.quote(rel)


def parse_file(path):
    lines = path.read_text().splitlines()
    section = None
    i, n = 0, len(lines)

    while i < n:
        raw = lines[i]

        # A 4+ space or tab indent is a markdown code block (e.g. a format
        # example inside a README), not a real top-level entry or snippet —
        # skip it, since stripping below would otherwise erase that
        # distinction and let a documentation example parse as fake content.
        if raw.startswith("    ") or raw.startswith("\t"):
            i += 1
            continue

        stripped = raw.strip()

        # Snippet: an H3 title, optionally with a blank line, then a fenced
        # code block. If no fence follows, it's just a normal header — falls
        # through to the HEADER_RE check below instead of being consumed here.
        sm = SNIPPET_TITLE_RE.match(stripped)
        if sm:
            j = i + 1
            while j < n and lines[j].strip() == "":
                j += 1
            fm = FENCE_RE.match(lines[j].strip()) if j < n else None
            if fm:
                code_lines = []
                k = j + 1
                while k < n and lines[k].strip() != "```":
                    code_lines.append(lines[k])
                    k += 1
                searchable, display, img = split_tags(sm.group("tags"))
                yield {
                    "kind": "snippet",
                    "desc": sm.group("title").strip(),
                    "tags": searchable,
                    "pills": display,
                    "image": image_url(path, img),
                    "lang": fm.group("lang"),
                    "code": "\n".join(code_lines),
                    "section": section,
                }
                i = k + 1  # resume after the closing fence
                continue

            # Table: an H3 title, then a pipe row followed by a `|---|`
            # separator. Same lookahead shape as the fence case above.
            if (
                j + 1 < n
                and TABLE_ROW_RE.match(lines[j].strip())
                and TABLE_SEP_RE.match(lines[j + 1].strip())
            ):
                header = table_cells(lines[j])
                rows, k = [], j + 2
                while k < n and TABLE_ROW_RE.match(lines[k].strip()):
                    rows.append(table_cells(lines[k]))
                    k += 1
                searchable, display, img = split_tags(sm.group("tags"))
                yield {
                    "kind": "table",
                    "desc": sm.group("title").strip(),
                    "tags": searchable,
                    "pills": display,
                    "image": image_url(path, img),
                    "header": header,
                    "rows": rows,
                    # Kept so the copy button can hand back the original
                    # markdown rather than a reconstruction.
                    "source": "\n".join(lines[j:k]),
                    "section": section,
                }
                i = k
                continue

        m = ENTRY_RE.match(stripped)
        if m:
            searchable, display, img = split_tags(m.group("tags"))
            yield {
                "kind": "cmd",
                "cmd": m.group("cmd"),
                "desc": (m.group("desc") or "").strip(),
                "tags": searchable,
                "pills": display,
                "image": image_url(path, img),
                "section": section,
            }
            i += 1
            continue

        hm = HEADER_RE.match(stripped)
        if hm:
            section = hm.group(2)

        i += 1


def build_index():
    topics = []
    for path in sheets():
        entries = list(parse_file(path))
        if not entries:
            continue
        topics.append(
            {
                "topic": path.stem,
                "file": str(path.relative_to(ROOT)),
                "entries": entries,
            }
        )
    return topics


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def do_GET(self):
        if self.path == "/api/entries":
            payload = json.dumps(build_index()).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return
        if self.path.startswith("/img/"):
            self.serve_image(self.path[len("/img/"):])
            return
        if self.path == "/":
            self.path = "/index.html"
        return super().do_GET()

    def serve_image(self, raw_rel):
        """Serve a preview image from anywhere under ROOT.

        This is the only route that turns a URL into an arbitrary file path,
        so it validates rather than trusts: the path is resolved first (which
        collapses `..` and follows symlinks), then checked to still be inside
        ROOT, then checked against the extension allowlist. A path that
        escapes ROOT fails the relative_to() check and 404s.

        It matters here because the Docker setup binds 0.0.0.0, so on a shared
        network this route isn't only reachable by the person at the keyboard.
        """
        rel = urllib.parse.unquote(raw_rel.split("?", 1)[0].split("#", 1)[0])
        try:
            target = (ROOT / rel).resolve()
            target.relative_to(ROOT.resolve())
        except (ValueError, OSError):
            self.send_error(404, "Not found")
            return

        ctype = IMAGE_TYPES.get(target.suffix.lower())
        if ctype is None or not target.is_file():
            self.send_error(404, "Not found")
            return

        try:
            data = target.read_bytes()
        except OSError:
            self.send_error(404, "Not found")
            return

        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        # An SVG rendered inside <img> can't run scripts, but these make that
        # true even if the URL is opened directly as a top-level page. The
        # style-src exception is needed because matplotlib emits inline
        # <style> blocks in its SVG output.
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'none'; style-src 'unsafe-inline'; sandbox",
        )
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format, *args):
        pass  # keep the terminal quiet


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lint", action="store_true",
                     help="find entries that silently fail to parse, then exit")
    args = ap.parse_args()

    if not ROOT.exists():
        print(f"warning: TOOLBOX_ROOT does not exist: {ROOT}")
        return

    if args.lint:
        lint()
        return

    with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
        print(f"toolbox running at http://localhost:{PORT}  (root: {ROOT}, bind: {HOST})")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped")


def lint():
    """Report `- `...`` lines that don't parse as entries — they don't
    error, they just silently never show up in search. A line joined with
    `/` (two commands on one bullet) is flagged as a real bug to split. A
    prose note that happens to start with a backtick-quoted term (like a
    Gotchas bullet) will also show up here — that's expected, not a bug."""
    found = 0
    for path in sheets():
        for lineno, raw in enumerate(path.read_text().splitlines(), start=1):
            stripped = raw.strip()
            if not stripped.startswith("- `") or ENTRY_RE.match(stripped):
                continue
            found += 1
            hint = ("multi-command line — split into separate bullets"
                     if re.search(r"`\s*/\s*`", stripped)
                     else "not a recognized entry (or intentional prose)")
            print(f"{path.relative_to(ROOT)}:{lineno}  [{hint}]")
            print(f"    {stripped}")
    if found == 0:
        print("no broken entries found")


if __name__ == "__main__":
    main()
