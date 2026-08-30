# toolbox (works: cheat sheets are work in progress)

A personal reference of terminal commands and code snippets — the ones used
often enough to need, but not often enough to remember.

## Structure

Each topic gets its own folder with one `.md` file:

    docker/docker.md
    git/git.md
   
New topic = new folder + `.md` file. Nothing else to register — `app`
(below) finds every sheet under the repo automatically.

## Entry format

Two formats live side by side in the same files.

**A command** is one line:

    - `command here` — description here <!-- optional, extra, search terms -->

- The description is optional — a bare `` - `cmd` `` still parses and shows
  up in search (matched against the command text itself) — but it's worth
  adding anyway. It's what makes a phrase search like "setup a python env"
  actually work, and what shows up in the `app` topic view.
- **One command per bullet.** `` - `cmd1` / `cmd2` `` reads fine on GitHub
  but silently fails to parse as an entry — split it into two lines.
- `<!-- tags -->` are invisible on GitHub but searchable — use them for
  words you'd actually type that the description doesn't happen to contain.

**A snippet** is boilerplate code — an H3 title, optionally tagged, right
before a fenced code block:

    ### snippet title here <!-- optional, extra, search terms -->
    ```python
    boilerplate code here
    ```

An H3 with nothing fenced right after it just becomes a normal section
label — nothing's forced into being a snippet.

Run `python3 app/server.py --lint` after adding entries. It reports any
command line that looks like an entry but doesn't parse, so a typo doesn't
just silently vanish from search — which is exactly how `git clone` went
missing for a while.

## Searching it — app

`appF/` is a small local web app: search bar, live results, copy buttons,
syntax-highlighted snippets. No build step — it re-reads the `.md` files on
every search, so an edit shows up on refresh. Fully offline: the syntax
highlighter and all fonts are self-hosted inside `app/`, no CDN calls.

    alias toolbox="python3 ~/Projects/toolbox/app/server.py"

Then `app` from anywhere starts it at `http://localhost:8420`.

Search scores every entry by how many of the typed words show up anywhere
across its description, tags, topic name, and its content (a command's
text, or a snippet's actual code) — not an exact-phrase match. That's why
"setup python env" still finds something described as "set **up** a new
virtual environment": it doesn't need every word to match exactly, just the
best-scoring entry, ranked highest first.

