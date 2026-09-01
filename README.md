# toolbox

A personal reference of terminal commands and code snippets — the ones used
often enough to need, but not often enough to remember.

## Structure

Folders are grouped by how broad the topic is, not forced into one rigid
pattern:

- A single, standalone tool gets its own folder: `docker/docker.md`,
  `git/git.md`.
- A broad topic with several related files shares one folder instead of
  each file getting its own redundant single-file folder: `python/` holds
  everything Python-related — env tooling, PyTorch, scikit-learn, Keras,
  matplotlib, CUDA/ML notes — as flat files, since almost all of it is
  Python anyway. No separate "ML" category needed.
- Two closely related tools can share a folder too: `archives/` holds both
  `tar.md` and `zip.md`.

New topic = new file, in an existing shared folder if it fits one, or its
own folder if it's a standalone tool. Nothing else to register — `app`
(below) finds every sheet under the repo automatically, however deep it's
nested.

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
  words you'd actually type that the description doesn't happen to contain,
  and skip the topic/library name itself (e.g. no need to tag a `pytorch/`
  entry with "pytorch" — the topic already covers that for free).

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

`app/` is a small local web app: search bar, live results, copy buttons,
syntax-highlighted snippets. No build step — it re-reads the `.md` files on
every search, so an edit shows up on refresh. Fully offline: the syntax
highlighter and all fonts are self-hosted inside `app/`, no CDN calls.

    alias tb="python3 ~/Projects/toolbox/app/server.py"

Then `tb` from anywhere starts it at `http://localhost:8420`. It can also
run in Docker instead — see "Running it in Docker" below.

Search scores every entry by how many of the typed words show up anywhere
across its description, tags, topic name, and its content (a command's
text, or a snippet's actual code) — not an exact-phrase match, and an exact
whole-word match now outranks a word that's merely a coincidental substring
inside something unrelated. That's why "setup python env" still finds
something described as "set **up** a new virtual environment," and why
searching "roc" correctly finds an ROC-curve snippet instead of a `bash`
entry that only matched because "roc" happens to sit inside "p**roc**ess."

## Running it in Docker

An alternative to the alias above — useful on a machine that doesn't
already have Python set up the way you like it, or if you'd rather not
think about that at all. For day-to-day use on your own machine, the `tb`
alias still starts faster, since there's no container to spin up.

`app/Dockerfile` bakes in the static app itself — `server.py`, `index.html`,
the syntax highlighter, the fonts. Those rarely change, so rebuilding the
image on the rare occasion they do is fine. Your actual content never goes
into the image: the root `docker-compose.yml` mounts the whole repo in
live, read-only, so editing a `.md` file and refreshing the page works
exactly like running it directly — the container never has its own stale
copy of your cheatsheets.

Setup is just building the image once:

    cd ~/Projects/toolbox
    docker compose build

Then, to start and stop it:

    docker compose up -d      # starts it in the background
    docker compose down       # stops it

Same address either way: `http://localhost:8420`.

## Status

`latex/` is still a placeholder — empty until there's enough in it to be
worth a file. (Git doesn't track empty directories, so a fresh clone won't
show it until something's added.)
