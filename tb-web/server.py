#!/usr/bin/env python3
"""
tb-web — serves your toolbox as a searchable page on localhost.

Defaults to the repo tb-web/ sits inside — so as long as it stays as a
subfolder of your toolbox clone, this works with zero setup on any machine:

    python3 server.py                          # from inside tb-web/
    python3 tb-web/server.py                    # from the repo root
    TOOLBOX_ROOT=~/somewhere/else python3 server.py   # override if needed
    TOOLBOX_PORT=9000 python3 server.py
    python3 server.py --lint                    # check for entries that fail to parse

Re-parses your .md files on every request to /api/entries, so editing a
sheet and refreshing the page is enough — no restart needed.

Entry format:
    - `command here` — description here <!-- optional, search, tags -->
"""
import argparse
import http.server
import json
import os
import re
import socketserver
from pathlib import Path

STATIC_DIR = Path(__file__).resolve().parent
DEFAULT_ROOT = STATIC_DIR.parent  # tb-web/ is expected to live inside the toolbox repo
ROOT = Path(os.environ.get("TOOLBOX_ROOT", DEFAULT_ROOT)).expanduser()
PORT = int(os.environ.get("TOOLBOX_PORT", 8420))

ENTRY_RE = re.compile(
    r"^- `(?P<cmd>[^`]+)`"
    r"(?:\s*[—-]\s*(?P<desc>.*?))?"
    r"(?:\s*<!--\s*(?P<tags>.*?)\s*-->)?$"
)
HEADER_RE = re.compile(r"^(#{2,6})\s+(.*)$")


def sheets():
    if not ROOT.exists():
        return []
    # Skip tb-web/'s own files (e.g. its README's format example) when it's
    # sitting inside the scanned root, so the tool never treats its own
    # documentation as a cheatsheet entry.
    return sorted(
        p for p in ROOT.rglob("*.md")
        if not p.resolve().is_relative_to(STATIC_DIR)
    )


def parse_file(path):
    section = None
    for raw in path.read_text().splitlines():
        stripped = raw.strip()
        m = ENTRY_RE.match(stripped)
        if m:
            yield {
                "cmd": m.group("cmd"),
                "desc": (m.group("desc") or "").strip(),
                "tags": m.group("tags") or "",
                "section": section,
            }
            continue
        hm = HEADER_RE.match(stripped)
        if hm:
            section = hm.group(2)


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
        if self.path == "/":
            self.path = "/index.html"
        return super().do_GET()

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

    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        print(f"toolbox running at http://localhost:{PORT}  (root: {ROOT})")
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
