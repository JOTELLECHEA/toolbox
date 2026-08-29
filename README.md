# toolbox

A personal reference of terminal commands — the ones used often enough to
need, but not often enough to remember.

## Structure

Each topic gets its own folder with one `.md` file:

    docker/docker.md
    git/git.md
    python/python-env.md
    cuda-ml/cuda-ml.md

New topic = new folder + `.md` file. Nothing else to register — `tb-web`
(below) finds every sheet under the repo automatically.

## Entry format

Every command is one line:

    - `command here` — description here <!-- optional, extra, search terms -->

- The description is optional — a bare `` - `cmd` `` still parses and shows
  up in search (matched against the command text itself) — but it's worth
  adding anyway. It's what makes a phrase search like "setup a python env"
  actually work, and what shows up in the `tb-web` topic view.
- **One command per bullet.** `` - `cmd1` / `cmd2` `` reads fine on GitHub
  but silently fails to parse as an entry — split it into two lines.
- `<!-- tags -->` are invisible on GitHub but searchable — use them for
  words you'd actually type that the description doesn't happen to contain.

Run `python3 tb-web/server.py --lint` after adding entries. It reports any
line that looks like an entry but doesn't parse, so a typo doesn't just
silently vanish from search — which is exactly how `git clone` went missing
for a while.

## Searching it — tb-web

`tb-web/` is a small local web app: search bar, live results, copy buttons.
No build step — it re-reads the `.md` files on every search, so an edit
shows up on refresh.

    alias toolbox="python3 ~/Projects/toolbox/tb-web/server.py"

Then `tb-web` from anywhere starts it at `http://localhost:8420`.

## Status

`bash/`, `latex/`, `pytorch/` are placeholders — empty until there's enough
in each to be worth a file. (Git doesn't track empty directories, so a
fresh clone won't show them until something's added.)
