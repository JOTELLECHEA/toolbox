# tb-web

Serves your toolbox `.md` files as a searchable page on localhost, with copy
buttons on every command.

## Run it

    TOOLBOX_ROOT=~/path/to/toolbox python3 server.py

Then open http://localhost:8420 — defaults to `~/toolbox` and port 8420 if
you skip the env vars (`TOOLBOX_PORT` to change the port).

No dependencies beyond the Python standard library.

## How it works

- `server.py` re-parses every `.md` file under `TOOLBOX_ROOT` on each request
  to `/api/entries` — edit a sheet, refresh the page, see the change. No
  restart needed.
- `index.html` fetches that JSON once on load and does all searching/rendering
  client-side. Search uses the same lenient, OR-scored word matching as the
  `tb` CLI (score by how many query words appear anywhere in an entry's
  description, tags, topic name, or the command itself) — so a partial
  phrase like "setup python env" still surfaces "set up a new virtual
  environment" even though "setup" isn't a literal substring.
- Same entry format as `tb`, nothing new to learn:
      - `command here` — description here <!-- optional, search, tags -->

## Known duplication

`server.py` and `tb` both implement the same ENTRY_RE/HEADER_RE parsing
logic independently. Fine for now, but if you add a third consumer, it's
worth factoring both into a shared `toolbox_core.py` that all three import.
